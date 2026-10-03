# Fluxo — demanda de crescimento e referência comparável

```text
COMERCIAL
   ↓
Modelo / Taxonomia
   ↓
Previsão futura por produto
   ↓
Natureza da demanda
   ├── EVENTO
   ├── SAZONALIDADE
   └── SPOT
   ↓
Identificar estrutura da previsão
   ↓
Reconstruir histórico equivalente
set/2025 → fev/2026
   ↓
Validar comparabilidade
   ├── comparável → calcular fator
   └── não comparável → registrar GAP
   ↓
Fator por dimensão comparável
   ↓
Carga projetada
   ↓
[ETAPA POSTERIOR]
Composição operacional por modelo/natureza
   ↓
Produtividade validada por função
   ↓
Demanda humana por função
   ↓
RH
   ↓
Demanda PCP × fornecimento RH
```

## Regra de parada da etapa atual

O fluxo deve ser interrompido após a validação da referência histórica comparável.

Não avançar para composição funcional ou produtividade enquanto não houver evidência suficiente.

## Dimensões que devem permanecer separadas

| Dimensão | Tratamento |
|---|---|
| Modelo/Taxonomia | Identifica o produto da demanda Comercial |
| Natureza | EVENTO, SAZONALIDADE, SPOT ou outra classificação comprovada |
| Período | Mantém a janela histórica/futura comparável |
| Quantidade | Volume da demanda |
| Chave de comparabilidade | Identifica equivalência entre histórico e previsão |
| Lista-mãe | Fora do cálculo de crescimento, salvo necessidade operacional comprovada |
| Chassi | Fora do caminho atual |
| Função | Etapa posterior |
| Produtividade | Etapa posterior |
| RH | Etapa posterior |

## Critério de comparabilidade

Uma base histórica só deve ser usada para calcular crescimento quando representar a mesma dimensão que será prevista.

Comparações válidas devem preservar, quando aplicável:

- mesma natureza da demanda;
- mesmo modelo/taxonomia ou agrupamento equivalente;
- mesma unidade de medida;
- período comparável;
- evento ou chave de comparabilidade equivalente;
- escopo operacional equivalente.

Se qualquer dimensão crítica não puder ser comprovada, o resultado deve ser marcado como GAP.

## Princípio

> **Comparar primeiro. Calcular depois. Converter em pessoas somente quando a composição e a produtividade estiverem comprovadas.**