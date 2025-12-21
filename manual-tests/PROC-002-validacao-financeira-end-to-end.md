# PROC-002 — Validação financeira end-to-end

## Objetivo
Garantir a consistência financeira dos valores exibidos durante o checkout.

## Requisitos cobertos
- REQ-PROD-005
- REQ-CART-003
- REQ-CHK-003
- REQ-CHK-004
- REQ-CHK-005

## Pré-condições
- Produtos com preços distintos disponíveis

## Procedimento
1. Login no sistema
2. Adicionar múltiplos produtos ao carrinho
3. Acessar o carrinho
4. Iniciar checkout
5. Avançar até a tela de overview

## Validações
- Subtotal corresponde à soma dos preços individuais
- Tax é calculada conforme regra de negócio
- Total corresponde a Subtotal + Tax
- Valores permanecem consistentes ao navegar entre telas

## Possíveis novos requisitos
- Regra de arredondamento explícita
- Tax variável por localização
- Moeda configurável
