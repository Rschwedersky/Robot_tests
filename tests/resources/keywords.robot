*** Settings ***
Library  Browser
Resource  variables.robot


*** Keywords ***
Open Application
    New Browser   ${BROWSER}   headless=false
    New Context
    New Page  ${BASE_URL}

Close Application
    Close Browser
    

Login With Credentials
    [Arguments]  ${user}  ${password}
    Fill Text  css=input[data-test="username"]  ${user}
    Fill Text  css=input[data-test="password"]  ${password}
    Click  css=input[data-test="login-button"]


Should See Login Error
    Wait For Elements State    css=h3[data-test="error"]    visible
    ${msg}=    Get Text    css=h3[data-test="error"]
    Should Contain    ${msg}    Epic sadface



Should Be On Products Page
    Wait For Elements State    css=span[data-test="title"]    visible
    ${title}=    Get Text    css=span[data-test="title"]
    Should Be Equal    ${title}    Products



Logout
    Click  css=button#react-burger-menu-btn
    Click  css=a[data-test="logout-sidebar-link"]
    Click  id=react-burger-menu-btn
    Click  id=logout_sidebar_link