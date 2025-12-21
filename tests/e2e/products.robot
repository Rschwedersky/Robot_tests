*** Settings ***
Resource    ../resources/keywords.robot
Test Setup      Open Application
Test Teardown   Close Application
Library     Collections

*** Test Cases ***
Visualizar lista de produtos
    [Tags]    smoke    products    REQ-PROD-001
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Should Be On Products Page
    Wait For Elements State    css=div[data-test="inventory-list"]    visible
    ${count}=    Get Element Count    css=div[data-test="inventory-item"]
    Should Be Equal As Integers    ${count}    6


Quantidade correta de produtos exibidos
    [Tags]    regression    products    REQ-PROD-002
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Should Be On Products Page
    ${count}=    Get Element Count    css=div[data-test="inventory-item"]
    Should Be Equal As Integers    ${count}    6

Abrir detalhes de um produto
    [Tags]    regression    products    REQ-PROD-003
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Should Be On Products Page
    Click    css=a[data-test="item-4-title-link"]
    Wait For Elements State    css=div[data-test="inventory-item-name"]    visible

Ordenar produtos por preço (low to high)
    [Tags]    regression    products    REQ-PROD-005
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Should Be On Products Page
    Wait For Elements State    css=div[data-test="inventory-list"]    visible
    Select Options By    css=select[data-test="product-sort-container"]    value    lohi
    ${elements}=    Get Elements    css=div[data-test="inventory-item-price"]

    ${prices}=    Create List
    FOR    ${el}    IN    @{elements}
        ${text}=    Get Text    ${el}
        ${value}=   Evaluate    float($text.replace('$',''))
        Append To List    ${prices}    ${value}
    END
    ${sorted}=    Copy List    ${prices}
    Sort List    ${sorted}
    Lists Should Be Equal    ${prices}    ${sorted}

Ordenar produtos por preço (hi-lo vs lo-hi)
    [Tags]    regression    products    REQ-PROD-005
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Should Be On Products Page
    Wait For Elements State    css=div[data-test="inventory-list"]    visible
    Select Options By    css=select[data-test="product-sort-container"]    value    hilo

    ${elements}=    Get Elements    css=div[data-test="inventory-item-price"]
    ${hi_to_lo}=    Create List

    FOR    ${el}    IN    @{elements}
        ${text}=    Get Text    ${el}
        ${value}=   Evaluate    float($text.replace('$',''))
        Append To List    ${hi_to_lo}    ${value}
    END

    ${expected_lo_to_hi}=    Copy List    ${hi_to_lo}
    Reverse List    ${expected_lo_to_hi}
    Select Options By    css=select[data-test="product-sort-container"]    value    lohi
    ${elements}=    Get Elements    css=div[data-test="inventory-item-price"]
    ${lo_to_hi}=    Create List
    FOR    ${el}    IN    @{elements}
        ${text}=    Get Text    ${el}
        ${value}=   Evaluate    float($text.replace('$',''))
        Append To List    ${lo_to_hi}    ${value}
    END
    Lists Should Be Equal    ${lo_to_hi}    ${expected_lo_to_hi}

Ordenar produtos por nome (Z-A vs A-Z)
    [Tags]    regression    products    REQ-PROD-004
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Should Be On Products Page
    Wait For Elements State    css=div[data-test="inventory-list"]    visible
    Select Options By    css=select[data-test="product-sort-container"]    value    za
    ${elements}=    Get Elements    css=div[data-test="inventory-item-name"]
    ${z_to_a}=    Create List
    FOR    ${el}    IN    @{elements}
        ${text}=    Get Text    ${el}
        Append To List    ${z_to_a}    ${text}
    END
    ${expected_a_to_z}=    Copy List    ${z_to_a}
    Reverse List    ${expected_a_to_z}
    Select Options By    css=select[data-test="product-sort-container"]    value    az
    ${elements}=    Get Elements    css=div[data-test="inventory-item-name"]
    ${a_to_z}=    Create List
    FOR    ${el}    IN    @{elements}
        ${text}=    Get Text    ${el}
        Append To List    ${a_to_z}    ${text}
    END
    Lists Should Be Equal    ${a_to_z}    ${expected_a_to_z}
