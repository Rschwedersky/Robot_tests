*** Settings ***
Resource    ../resources/keywords.robot
Library    ../../ai/AIAssistant.py

Test Setup      Open Application
Test Teardown   Close Application

*** Test Cases ***

#POC Login Click
#    [Tags]    REQ-AUTH-001
#    Fill Text  css=input[data-test="username"]  standard_user
#    Fill Text  css=input[data-test="password"]  secret_sauce
#    AI Click    login button

Login com credenciais válidas
    [Tags]    smoke    positive    REQ-AUTH-001
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Should Be On Products Page

Login com usuário inválido
    [Tags]    negative    REQ-AUTH-002
    Login With Credentials    ${INVALID_USER}    ${VALID_PASSWORD}
    Should See Login Error

Login com senha inválida
    [Tags]    negative    REQ-AUTH-002
    Login With Credentials    ${VALID_USER}    ${INVALID_PASS}
    Should See Login Error

Login sem usuário
    [Tags]    negative    validation    REQ-AUTH-002
    Login With Credentials    ${EMPTY}    ${VALID_PASSWORD}
    Should See Login Error

Login sem senha
    [Tags]    negative    validation    REQ-AUTH-002
    Login With Credentials    ${VALID_USER}    ${EMPTY}
    Should See Login Error

