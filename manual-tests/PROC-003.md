# PROC-003 — Recuperação de erro e estado

## Objetivo
Avaliar como o sistema se comporta após erros e ações interrompidas.

## Requisitos cobertos
- REQ-AUTH-002
- REQ-CHK-002
- REQ-CART-004

## Procedimento
1. Tentar login com credenciais inválidas
2. Corrigir credenciais e realizar login válido
3. Adicionar produto ao carrinho
4. Iniciar checkout
5. Submeter formulário sem preencher campos obrigatórios
6. Corrigir dados e prosseguir

## Validações
- Mensagens de erro são claras e recuperáveis
- Estado do carrinho não é perdido após erro
- Usuário consegue prosseguir sem reiniciar fluxo

## Possíveis novos requisitos
- Preservação de dados após erro
- Padronização de mensagens de erro
