*** Settings ***
Library           resources/driver_manager.py
Library           resources/open_browser.py
Library           resources/sign_in.py 
Library           resources/product_filter.py
Library           resources/get_product.py
Library           resources/cart_process.py
Library           resources/checkout.py
Library           resources/save_data.py
Library           DateTime
Library           DOP.RPA.ProcessArgument
Library           DOP.RPA.Asset
Library           Collections
Library           BuiltIn

*** Variables ***
${PRODUCT_URL}          https://magento.softwaretestingboard.com/
${EMAIL_HARD}           truong.nguyen5102002@gmail.com
${PASSWORD_HARD}        Nguyen5102002!
&{CATEGORY_IDS}         Jackets=ui-id-19    Hoodies & Sweatshirts=ui-id-20    Tees=ui-id-21    Tank=ui-id-22
${MAX_PRICE_THRESHOLD}  50
${QUANTITY}             10

*** Tasks ***
Run All Tasks 
    # ${email} =    Get Asset Or Fail    email
    # ${password} =    Get Asset Or Fail    password
    ${category_name} =    Get In Arg Or Fail    category
    ${size} =    Get In Arg Or Fail    size
    ${color} =    Get In Arg Or Fail    color
    ${min_price} =    Get In Arg Or Fail    min_price
    ${max_price} =    Get In Arg Or Fail    max_price

    Initialize Driver
    Open Browser    ${PRODUCT_URL}
    Sign In    ${EMAIL_HARD}    ${PASSWORD_HARD}
    
    ${category_ui_id} =    Get Category ID    ${category_name}
    Product Filter   ${category_ui_id}    ${size}    ${color}
    
    ${product_list} =    Get Product List    ${min_price}    ${max_price}    ${QUANTITY}    ${size}    ${color}
    Process Cart        ${QUANTITY}
    ${order_number} =    Process Checkout    

    ${date_now} =    Get Current Date    result_format='%Y-%m-%d'
    Save Order Info    ${date_now}    ${EMAIL_HARD}    ${size}    ${color}    ${QUANTITY}    ${product_list}    ${order_number}

*** Keywords ***
Get Category ID
    [Arguments]    ${category_name}
    ${ui_id}=    Get From Dictionary    ${CATEGORY_IDS}    ${category_name}
    [Return]    ${ui_id}

Get Asset Or Fail
    [Arguments]    ${asset_name}
    ${asset} =    Get Asset    ${asset_name}
    Run Keyword If    ${asset} is None    Fail    Could not retrieve asset '${asset_name}'.
    [Return]    ${asset}[value]

Get In Arg Or Fail
    [Arguments]    ${arg_name}
    ${arg} =    Get In Arg    ${arg_name}
    Run Keyword If    ${arg} is None    Fail    Could not retrieve argument '${arg_name}'.
    [Return]    ${arg}[value]