# ELO — Loop de Execução de Orçamento

## Princípio

Nenhum item canônico é alterado silenciosamente. O ELO identifica o modelo, preserva sua configuração-base, detecta excedentes, audita relações e decide entre execução automática e consulta ao especialista.

## Loop

```text
ENTRADA
  ↓
CLASSIFICAR SOLICITAÇÃO
  ↓
IDENTIFICAR TAXONOMIA / FAMÍLIA / MODELO
  ↓
CARREGAR DADOS CANÔNICOS
  ↓
COMPARAR CONFIGURAÇÃO SOLICITADA × PADRÃO
  ↓
SEPARAR PADRÃO E EXCEDENTES
  ↓
AUDITAR RELAÇÕES E COMPOSIÇÕES
  ↓
VALIDAR DIMENSÕES / UNIDADES / QUANTIDADES
  ↓
VERIFICAR PREÇO DISPONÍVEL
  ├── SIM → utilizar preço canônico
  └── NÃO → não inventar preço; escalar
  ↓
DECISÃO
  ├── AUTO → gerar estrutura orçamentária
  └── ESPECIALISTA → formular pergunta contextualizada
  ↓
APROVAÇÃO / REJEIÇÃO / AJUSTE
  ↓
EVOLUTION GATE
  ↓
EXPERIÊNCIA TEMPORAL OU REGRA CANÔNICA
```

## Gatilhos mínimos

- `ORCAR`: iniciar composição orçamentária.
- `COMPARAR_VALORES`: comparar somente fontes/preços disponíveis.
- `NOVO_ITEM`: verificar aderência à taxonomia e à lista-mãe.
- `EXCEDENTE_DETECTADO`: auditar relações antes de adicionar.
- `RELACAO_PENDENTE`: exigir auditoria especializada.
- `PRECO_AUSENTE`: solicitar fonte ou decisão; nunca estimar silenciosamente.
- `NOVA_LISTA_MAE`: executar auditoria antes de admissão.
- `APROVACAO_ESPECIALISTA`: registrar decisão e avaliar evolução.

## Regra de aprendizagem

Uma experiência não se torna regra canônica apenas porque funcionou uma vez. Deve ser avaliada, rastreável e admitida pelo Evolution Gate. Experiências úteis podem permanecer como memória temporal até demonstrarem estabilidade suficiente para promoção.
