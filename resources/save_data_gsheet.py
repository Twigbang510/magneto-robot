from robocorp.tasks import task
import logging
from helper import *
import openpyxl
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

import time
logger = logging.getLogger(__name__)

@task
def save_to_gsheet(email, quantity, product_list, order_num, spreadsheet_id, credentials_file, token_file):
    try:
        service = authenticate_gsheet(credentials_file, token_file)
        date_now = datetime.now().strftime("%Y-%m-%d")

        save_sales_order(service, spreadsheet_id, "Sales Order", date_now, email, order_num, quantity)
        save_purchasing(service, spreadsheet_id, "Purchasing", product_list, quantity, order_num, date_now)
        save_inventory(service, spreadsheet_id, "Inventory", product_list, quantity, date_now)

        logger.info("Order information successfully saved to Google Sheets.")

    except Exception as e:
        logger.error(f"Failed to save order information to Google Sheets: {str(e)}")
        raise

def authenticate_gsheet(credentials_file, token_file):
    logger.info("Authenticating with Google Sheets API...")
    creds = None
    try:
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    except (FileNotFoundError, ValueError):
        flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    return build("sheets", "v4", credentials=creds)

def save_sales_order(service, spreadsheet_id, sheet_name, date, email, order_number, quantity):
    row = get_next_row(service, spreadsheet_id, sheet_name)
    if row:
        update_cell(service, spreadsheet_id, f"{sheet_name}!C{row}", email)
        update_cell(service, spreadsheet_id, f"{sheet_name}!J{row}", 'Bought')
        update_cell(service, spreadsheet_id, f"{sheet_name}!K{row}", order_number)
        logger.info("Sales order updated in Sales Order sheet.")
        
def get_row_by_date(service, spreadsheet_id, sheet_name, target_date):
    """
    Find row where the date matches the target date.
    """
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A:A"
    ).execute()
    values = result.get('values', [])
    for idx, row in enumerate(values, start=1):
        if row and row[0] == target_date:
            return idx
    return None

def save_purchasing(service, spreadsheet_id, sheet_name, product_list, quantity, order_number, date):
    for product in product_list:
        data = [
            [
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
        ]
        append_data(service, spreadsheet_id, f"{sheet_name}!A:I", data)
    logger.info("Product data saved to Purchasing sheet.")

def save_inventory(service, spreadsheet_id, sheet_name, product_list, quantity, date):
    for product in product_list:
        if product['status'] == 'Added to cart':
            row = get_product_row(service, spreadsheet_id, sheet_name, product['name'])
            if row:
                cell_range = f"{sheet_name}!B{row}"
                current_qty = get_cell_value(service, spreadsheet_id, cell_range)
                new_qty = int(current_qty) + int(quantity)
                update_cell(service, spreadsheet_id, cell_range, new_qty)
            else:
                data = [[product['name'], quantity]]
                append_data(service, spreadsheet_id, f"{sheet_name}!A:C", data)
    logger.info("Inventory updated in Inventory sheet.")

def get_next_row(service, spreadsheet_id, sheet_name):
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A:A"
    ).execute()
    values = result.get('values', [])
    return len(values) + 1

def get_product_row(service, spreadsheet_id, sheet_name, product_name):
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A:A"
    ).execute()
    values = result.get('values', [])
    for idx, row in enumerate(values, start=1):
        if row and row[0] == product_name:
            return idx
    return None

def get_cell_value(service, spreadsheet_id, cell_range):
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=cell_range
    ).execute()
    values = result.get('values', [])
    return values[0][0] if values else 0

def update_cell(service, spreadsheet_id, cell_range, value):
    body = {
        'values': [[value]]
    }
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=cell_range,
        valueInputOption="RAW",
        body=body
    ).execute()

def append_data(service, spreadsheet_id, range_name, data):
    try:
        body = {"values": data}
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body,
        ).execute()
        logger.info(f"Appended {result.get('updates').get('updatedRows')} rows to {range_name}")
    except HttpError as e:
        logger.error(f"Failed to append data to Google Sheets: {e}")
        raise