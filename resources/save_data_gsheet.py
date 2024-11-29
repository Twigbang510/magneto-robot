import gspread
from robocorp.tasks import task
import logging
from helper import *
import openpyxl
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth import exceptions
from google.auth.transport.requests import Request
import os

# Define Google Sheets API scope
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Set up logging
logger = logging.getLogger(__name__)

@task
def save_to_gsheet(email, quantity, product_list, order_num, spreadsheet_id, order_info, credentials_file, token_file):
    """
    Save order data to Google Sheets.
    """
    try:
        service = authenticate_gsheet(credentials_file, token_file)
        date_now = datetime.now().strftime("%Y-%m-%d")

        save_sales_order(service, spreadsheet_id, "Sales Order", date_now, email, order_info, order_num, quantity)
        save_purchasing(service, spreadsheet_id, "Purchasing", product_list, quantity, order_num, date_now)
        save_inventory(service, spreadsheet_id, "Inventory", product_list, quantity, date_now)

        logger.info("Order information successfully saved to Google Sheets.")
    except Exception as e:
        logger.error(f"Failed to save order information to Google Sheets: {str(e)}")
        raise

def authenticate_gsheet(credentials_file, token_file):
    """
    Authenticate and get Google Sheets service client.
    """
    logger.info("Authenticating with Google Sheets API...")
    creds = None

    if os.path.exists(token_file):
        try:
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        except exceptions.GoogleAuthError as e:
            logger.warning(f"Error loading credentials: {e}")
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            logger.info("Token refreshed successfully.")
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
            logger.info("OAuth2 flow completed successfully.")
        
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
            logger.info(f"New credentials saved to {token_file}")

    client = gspread.authorize(creds)
    return client

def save_sales_order(service, spreadsheet_id, sheet_name, date, email, order_info, order_number, quantity):
    """
    Save sales order data to the "Sales Order" sheet.
    """
    logger.info(f"Saving sales order: {order_info}")
    sheet = service.open_by_key(spreadsheet_id).worksheet(sheet_name)
    
    data = [
        [
            date,
            '',
            email,
            order_info.get('Category', ''),
            order_info.get('Size', ''),
            order_info.get('Color', ''),
            order_info.get('Min Price', ''),
            order_info.get('Max Price', ''),
            quantity,
            'Bought',
            order_number
        ]
    ]
    sheet.append_rows(data, value_input_option='RAW')
    logger.info("Sales order updated.")

def save_purchasing(service, spreadsheet_id, sheet_name, product_list, quantity, order_number, date):
    """
    Save product purchase data to the "Purchasing" sheet.
    """
    logger.info("Saving product data to Purchasing sheet.")
    sheet = service.open_by_key(spreadsheet_id).worksheet(sheet_name)

    data = []
    for product in product_list:
        product_data = [
            'Magneto',
            product['name'],
            product['size'],
            product['color'],
            quantity,
            product['status'],
            product['price'],
            date,
            order_number
        ]
        data.append(product_data)
    
    sheet.append_rows(data, value_input_option='RAW')
    logger.info("Product data saved.")

def save_inventory(service, spreadsheet_id, sheet_name, product_list, quantity, date):
    """
    Update inventory data in the "Inventory" sheet.
    """
    logger.info("Updating inventory in Inventory sheet.")
    sheet = service.open_by_key(spreadsheet_id).worksheet(sheet_name)

    for product in product_list:
        if product['status'] == 'Added to cart':
            try:
                cell = sheet.find(product['name'])
                if cell:
                    current_qty = int(sheet.cell(cell.row, 2).value)
                    new_qty = current_qty + int(quantity)
                    sheet.update_cell(cell.row, 2, new_qty)
                    logger.info(f"Updated inventory for '{product['name']}' (new qty: {new_qty}).")
                else:
                    sheet.append_row([product['name'], quantity, date])
                    logger.info(f"Added new product '{product['name']}' to inventory.")
            except Exception as e:
                logger.error(f"Error updating inventory for '{product['name']}': {e}")

    logger.info("Inventory updated.")
