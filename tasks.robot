*** Settings ***
Library           resources/driver_manager.py
Library           resources/open_browser.py
Library           resources/sign_in.py 
Library           resources/product_filter.py
Library           resources/get_product.py
Library           resources/cart_process.py
Library           resources/checkout.py
Library           resources/save_data.py
Library           resources/input_validation.py
Library           DateTime
Library           DOP.RPA.ProcessArgument
Library           DOP.RPA.Asset
Library           Collections
Library           BuiltIn

*** Variables ***
${PRODUCT_URL}          https://magento.softwaretestingboard.com/
&{CATEGORY_IDS}         Jackets=ui-id-19    Hoodies & Sweatshirts=ui-id-20    Tees=ui-id-21    Tank=ui-id-22
${QUANTITY}             10
${AVAILABLE_SIZE}       [XS, S, M, L, XL]
${AVAILABLE_COLOR}      [BLACK, BLUE, GRAY, GREEN, ORANGE, PURPLE, RED, WHITE, YELLOW]
*** Tasks ***
Run All Tasks 
    ${email} =    Get Asset Or Fail    login    email
    ${password} =    Get Asset Or Fail    login    password

    ${category_name} =    Get In Arg Or Fail    category
    ${size} =    Get In Arg Or Fail    size
    ${color} =    Get In Arg Or Fail    color
    ${min_price} =    Get In Arg Or Fail    min_price
    ${max_price} =    Get In Arg Or Fail    max_price
    ${shipping_option} =    Get Asset     shipping_address
    ${shipping_option_value} =    Set Variable    ${shipping_option}[value]
    ${valid_size} =     Check Valid Size Input    ${size}    ${AVAILABLE_SIZE}
    ${valid_color} =    Check Valid Color Input    ${color}    ${AVAILABLE_COLOR}

    Initialize Driver
    Open Browser    ${PRODUCT_URL}
    Sign In    ${email}    ${password}
    
    ${category_ui_id} =    Get Category ID    ${category_name}
    Product Filter   ${category_ui_id}    ${valid_size}    ${valid_color}
    

    ${product_list} =     Get Product List    ${min_price}    ${max_price}    ${QUANTITY}    ${valid_size}    ${valid_color}
    Process Cart        ${QUANTITY}
    ${order_number} =    Process Checkout    ${shipping_option_value}

    ${output_file} =    Save Order Info    ${email}    ${size}    ${color}    ${QUANTITY}    ${product_list}    ${order_number}
    
    Set Out Arg    output_file    ${output_file}
*** Keywords ***
Get Category ID
    [Arguments]    ${category_name}
    ${ui_id}=    Get From Dictionary    ${CATEGORY_IDS}    ${category_name}
    [Return]    ${ui_id}

Get Asset Or Fail
    [Arguments]    ${asset_name}    ${value_name}
    ${asset} =    Get Asset    ${asset_name}
    ${value} =    Set Variable    ${asset}[value][${value_name}]
    Run Keyword If    '${value}' == ''    Fail    Could not retrieve asset '${value_name}'.
    [Return]    ${value}

Get In Arg Or Fail
    [Arguments]    ${arg_name}
    ${arg} =    Get In Arg    ${arg_name}
    [Return]    ${arg}[value]