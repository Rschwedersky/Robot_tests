# PROC-001 — Compra completa end-to-end

## Objetivo
Validar o fluxo completo de compra de um usuário, do login à confirmação do pedido.

## Requisitos cobertos
- REQ-AUTH-001
- REQ-PROD-001
- REQ-CART-001
- REQ-CART-004
- REQ-CHK-001
- REQ-CHK-006

## Pré-condições
- Usuário válido existente
- Sistema operacional

## Procedimento
1. Acessar a aplicação
2. Realizar login com credenciais válidas
3. Confirmar exibição da página Products
4. Adicionar pelo menos um produto ao carrinho
5. Navegar para o carrinho
6. Iniciar checkout
7. Preencher dados obrigatórios
8. Finalizar o pedido
9. Retornar à página de produtos

## Validações
- Navegação ocorre sem erros
- Itens permanecem consistentes ao longo do fluxo
- Confirmação de pedido é exibida ao final

## Possíveis novos requisitos
- Persistência do carrinho após refresh
- Histórico de pedidos do usuário
