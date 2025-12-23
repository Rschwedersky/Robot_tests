# PROC-005 — Resiliência de sessão e navegação

## Objetivo
Validar comportamento do sistema em cenários de interrupção de sessão.

## Requisitos cobertos
- REQ-AUTH-001
- REQ-CART-004
- REQ-CHK-001

## Procedimento
1. Login no sistema
2. Adicionar itens ao carrinho
3. Atualizar a página (refresh)
4. Navegar usando botão voltar do navegador
5. Abrir aplicação em nova aba

## Validações
- Sessão permanece válida
- Carrinho mantém estado esperado
- Sistema não entra em estado inconsistente

## Possíveis novos requisitos
- Timeout de sessão configurável
- Mensagem clara em expiração de sessão
