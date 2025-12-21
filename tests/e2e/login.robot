*** Settings ***
Resource    ../resources/keywords.robot

Test Setup      Open Application
Test Teardown   Close Application

*** Test Cases ***
Login com credenciais válidas
    [Tags]    smoke    positive
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Should Be On Products Page

Login com usuário inválido
    [Tags]    negative
    Login With Credentials    ${INVALID_USER}    ${VALID_PASSWORD}
    Should See Login Error

Login com senha inválida
    [Tags]    negative
    Login With Credentials    ${VALID_USER}    ${INVALID_PASS}
    Should See Login Error

Login sem usuário
    [Tags]    negative    validation
    Login With Credentials    ${EMPTY}    ${VALID_PASSWORD}
    Should See Login Error

Login sem senha
    [Tags]    negative    validation
    Login With Credentials    ${VALID_USER}    ${EMPTY}
    Should See Login Error
