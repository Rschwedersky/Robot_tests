*** Settings ***
Resource    ../resources/keywords.robot
Library     Collections
Test Setup      Open Application
Test Teardown   Close Application


*** Test Cases ***
Checkout completo com um produto
    [Tags]    smoke    checkout    REQ-CHK-001    REQ-CHK-004

    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}

    Click    button[data-test="add-to-cart-sauce-labs-backpack"]
    Click    a[data-test="shopping-cart-link"]
    Click    button[data-test="checkout"]

    Wait For Elements State    css=input[data-test="firstName"]    visible
    Fill Text    input[data-test="firstName"]    Rodrigo
    Fill Text    input[data-test="lastName"]     QA
    Fill Text    input[data-test="postalCode"]   88000

    Click    input[data-test="continue"]

    Wait For Elements State    css=span[data-test="title"]    visible
    ${title}=    Get Text    css=span[data-test="title"]
    Should Be Equal    ${title}    Checkout: Overview

    Click    button[data-test="finish"]

    Wait For Elements State    css=h2[data-test="complete-header"]    visible
    ${msg}=    Get Text    css=h2[data-test="complete-header"]
    Should Be Equal    ${msg}    Thank you for your order!

    Click    button[data-test="back-to-products"]

Checkout com multiplos produtos
    [Tags]    regression    checkout    REQ-CHK-002    REQ-CHK-004
    
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Click    button[data-test="add-to-cart-sauce-labs-backpack"]
    Click    button[data-test="add-to-cart-sauce-labs-bike-light"]
    Click    button[data-test="add-to-cart-sauce-labs-bolt-t-shirt"]
    Click    a[data-test="shopping-cart-link"]
    Click    button[data-test="checkout"]
    Fill Text    input[data-test="firstName"]    Maria
    Fill Text    input[data-test="lastName"]     Jesus
    Fill Text    input[data-test="postalCode"]   12345
    Click    input[data-test="continue"]
    ${items}=    Get Element Count    css=div.cart_item
    Should Be Equal As Integers    ${items}    3
    Click    button[data-test="finish"]
    Wait For Elements State    css=h2[data-test="complete-header"]    visible


Checkout falha sem dados obrigatorios
    [Tags]    negative    checkout    REQ-CHK-003

    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Click    button[data-test="add-to-cart-sauce-labs-backpack"]
    Click    a[data-test="shopping-cart-link"]
    Click    button[data-test="checkout"]
    Click    input[data-test="continue"]
    Wait For Elements State    css=h3[data-test="error"]    visible
    ${error}=    Get Text    css=h3[data-test="error"]
    Should Contain    ${error}    Error:

Checkout valida soma, tax e total
    [Tags]    regression    checkout    financial    REQ-FIN-001    REQ-FIN-002    REQ-FIN-003
    
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Click    button[data-test="add-to-cart-sauce-labs-backpack"]
    Click    button[data-test="add-to-cart-sauce-labs-bike-light"]
    Click    a[data-test="shopping-cart-link"]
    Click    button[data-test="checkout"]
    Fill Text    input[data-test="firstName"]    QA
    Fill Text    input[data-test="lastName"]     Robot
    Fill Text    input[data-test="postalCode"]   99999
    Click    input[data-test="continue"]
    Wait For Elements State    css=span[data-test="title"]    visible
    ${title}=    Get Text    css=span[data-test="title"]
    Should Be Equal    ${title}    Checkout: Overview
        ${elements}=    Get Elements    css=div.inventory_item_price
    ${prices}=    Create List
    FOR    ${el}    IN    @{elements}
        ${text}=    Get Text    ${el}
        ${value}=   Evaluate    float($text.replace('$',''))
        Append To List    ${prices}    ${value}
    END
    ${calculated_sum}=    Evaluate    round(sum($prices), 2)
    ${ui_subtotal}=    Get Text    css=div[data-test="subtotal-label"]
    ${ui_subtotal}=    Evaluate    float($ui_subtotal.replace('Item total: $',''))
    Should Be Equal As Numbers    ${ui_subtotal}    ${calculated_sum}
    ${ui_tax}=    Get Text    css=div[data-test="tax-label"]
    ${ui_tax}=    Evaluate    float($ui_tax.replace('Tax: $',''))
    ${expected_tax}=    Evaluate    round($calculated_sum * 0.08, 2)
    Should Be Equal As Numbers    ${ui_tax}    ${expected_tax}
    ${ui_total}=    Get Text    css=div[data-test="total-label"]
    ${ui_total}=    Evaluate    float($ui_total.replace('Total: $',''))
    ${expected_total}=    Evaluate    round($calculated_sum + $ui_tax, 2)
    Should Be Equal As Numbers    ${ui_total}    ${expected_total}
