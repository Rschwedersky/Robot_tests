*** Settings ***
Resource  ../resources/keywords.robot
Test Setup      Open Application
Test Teardown   Close Application

*** Test Cases ***
Adicionar produto ao carrinho
    [Tags]    smoke    cart    REQ-CART-001
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Should Be On Products Page

    Click    button[data-test="add-to-cart-sauce-labs-backpack"]

    Wait For Elements State    css=.shopping_cart_badge    visible
    ${count}=    Get Text    css=.shopping_cart_badge
    Should Be Equal    ${count}    1

Carrinho exibe produto adicionado
    [Tags]    regression    cart    REQ-CART-001    REQ-CART-003
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}

    Click    button[data-test="add-to-cart-sauce-labs-backpack"]
    Click    a[data-test="shopping-cart-link"]

    Wait For Elements State    css=div.cart_item    visible
    ${items}=    Get Element Count    css=div.cart_item
    Should Be Equal As Integers    ${items}    1


Remover produto do carrinho
    [Tags]    regression    cart    REQ-CART-002
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Click    button[data-test="add-to-cart-sauce-labs-backpack"]
    Click    a[data-test="shopping-cart-link"]
    Click    button[data-test="remove-sauce-labs-backpack"]
    Wait For Elements State    css=div.cart_item    detached

Badge do carrinho reflete quantidade correta
     [Tags]    regression    cart    REQ-CART-003
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}

    Click    button[data-test="add-to-cart-sauce-labs-backpack"]
    Click    button[data-test="add-to-cart-sauce-labs-bike-light"]

    ${badge}=    Get Text    css=.shopping_cart_badge
    Should Be Equal    ${badge}    2

Itens permanecem no carrinho ao navegar
    [Tags]    regression    cart    REQ-CART-004
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}

    Click    button[data-test="add-to-cart-sauce-labs-backpack"]
    Click    a[data-test="shopping-cart-link"]

    Go Back

    ${badge}=    Get Text    css=.shopping_cart_badge
    Should Be Equal    ${badge}    1

Navegar do carrinho para checkout
   [Tags]    smoke    checkout    REQ-CHK-001
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}

    Click    button[data-test="add-to-cart-sauce-labs-backpack"]
    Click    a[data-test="shopping-cart-link"]
    Click    button[data-test="checkout"]

    Wait For Elements State    css=span[data-test="title"]    visible
    ${title}=    Get Text    css=span[data-test="title"]
    Should Be Equal    ${title}    Checkout: Your Information