# ELO — Template Canônico de Orçamento

**Status:** modelo operacional  
**Domínio:** Orçamento  
**Uso:** registro rastreável de uma execução de orçamento

> Este documento registra a execução. Não substitui o Prompt do Especialista, a Metodologia V2, a PTS Técnica ou a PTS Pós-Orçamento.

## 1. Identificação

- SO:
- Cliente/contratante:
- Objeto:
- Local:
- Tipo: `VENDA | LOCAÇÃO | OUTRO`
- Regime/condição comercial:
- Prazo:
- Responsável:
- Data da análise:
- Versão do orçamento:

## 2. Fontes utilizadas

| Fonte | Identificação/versão | Evidência | Vigência |
|---|---|---|---|
| TR/documentação | | | |
| Projeto/layout | | | |
| PTS Técnica | | | |
| Conhecimento corporativo | | | |
| Histórico | | | |
| Cotação | | | |

## 3. Escopo

### Incluído
- 

### Excluído
- 

### Pendências
- 

## 4. Modelo/base e classificação

| Necessidade | Padrão/base | Categoria | Desvio | Evidência |
|---|---|---|---|---|
| | | `PRODUTO_PADRAO / EXCEDENTE / CUSTOMIZACAO / SERVICO / MATERIAL / MO_INTERNA / MO_EXTERNA / PENDENCIA` | | |

## 5. Quantitativos

| Item | Descrição | Unidade | Quantidade | Fonte | Conferência |
|---|---|---:|---:|---|---|
| | | | | | |

## 6. Excedentes e customizações

| Requisito | Padrão | Alteração | Quantidade | Material | Mão de obra | Impacto | Preço | Evidência |
|---|---|---|---:|---|---|---|---:|---|
| | | | | | | | | |

## 7. Composição de custos

Para cada item relevante preservar a cadeia:

`REQUISITO → SOLUÇÃO → QUANTITATIVO → COMPOSIÇÃO → PREÇO UNITÁRIO → PARCIAL → PREMISSA`

| Item | Material | Fabricação | MO interna | MO externa | Fornecedor | Transporte | Mobilização | Outros | Parcial |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| | | | | | | | | | |

## 8. Memórias de cálculo

### Cálculo [ID]

- Objetivo:
- Entradas:
- Unidades:
- Fórmula:
- Parâmetros:
- Substituição:
- Resultado:
- Arredondamento:
- Premissa:
- Evidência:
- Validação:

## 9. Mão de obra

| Especialidade | Equipe | Produtividade | Duração | Unidade de custo | Custo |
|---|---:|---:|---:|---|---:|
| | | | | | |

## 10. Logística e mobilização

| Componente | Premissa | Quantidade/dias | Unidade | Valor | Evidência |
|---|---|---:|---|---:|---|
| Mobilização | | | | | |
| Desmobilização | | | | | |
| Transporte | | | | | |
| Hospedagem | | | | | |
| Alimentação | | | | | |
| Combustível | | | | | |
| Deslocamento local | | | | | |
| Veículo de apoio | | | | | |
| Içamento/Munck | | | | | |

## 11. Projetos e documentação

- Projeto:
- ART/RRT:
- Ensaios:
- As built:
- Comissionamento:
- Outros:

## 12. Premissas

| Premissa | Classe | Impacto | Evidência | Status |
|---|---|---|---|---|
| | `DOCUMENTAL / CORPORATIVA / TÉCNICA / ORÇAMENTÁRIA / COMERCIAL / CLIENTE / NÃO CONFIRMADA` | | | |

## 13. Questionamentos e vistoria

| Item | Lacuna | Vistoria resolve? | Pergunta necessária | Impacto | Status |
|---|---|---|---|---|---|
| | | | | | |

## 14. PTS Técnica × Orçamento

| Item | Previsto na PTS | Orçado | Diferença | Motivo | Impacto | Ação |
|---|---|---|---|---|---|---|
| | | | | | | |

## 15. PTS Pós-Orçamento

### Checklist

- [ ] requisito sem item orçado
- [ ] item orçado sem requisito identificado
- [ ] divergência de quantidade
- [ ] divergência de unidade
- [ ] divergência de valor
- [ ] verba sem composição suficiente
- [ ] premissa não registrada
- [ ] exclusão não justificada
- [ ] responsabilidade indefinida
- [ ] logística ausente
- [ ] projeto/documentação ausente
- [ ] item dependente de confirmação

### Divergências

| Divergência | Evidência | Causa | Correção | Validação |
|---|---|---|---|---|
| | | | | |

## 16. Fechamento comercial

- Custo direto:
- Custos indiretos:
- BDI:
- Taxa de administração:
- Preço final:
- Condição comercial:
- Validade:
- Observações:

## 17. Evidências e rastreabilidade

| ID | Tipo | Referência | O que comprova | Resultado |
|---|---|---|---|---|
| | `DOCUMENTO / CLIENTE / TÉCNICA / PADRÃO / PREMISSA / DECISÃO / VISTORIA / COTAÇÃO` | | | |

## 18. Resultado

### Situação
`FECHADO | PENDENTE | CONTESTADO | REVISÃO | NÃO ORÇADO`

### Riscos
- 

### Pendências para fechamento
- 

## 19. Aprendizado pós-orçamento

Somente após conferência e validação:

| Aprendizado | Contexto | Aplicação | Exceção | Evidência | Risco | Status |
|---|---|---|---|---|---|---|
| | | | | | | `OBSERVADO / CANDIDATO / VALIDADO / REJEITADO / SUPERADO` |

## 20. Potencialização para o ELO

Registrar o que este orçamento acrescentou à capacidade do ELO:

- nova relação requisito ↔ solução:
- nova memória de cálculo:
- novo padrão de material/composição:
- novo parâmetro de produtividade:
- novo padrão logístico:
- novo risco identificado:
- correção de aprendizado anterior:
- evidência que sustenta a mudança:

## 21. Regra de encerramento

Um orçamento somente deve ser considerado cognitivamente aproveitável quando sua cadeia estiver rastreável:

`DOCUMENTO → REQUISITO → SOLUÇÃO → QUANTITATIVO → CÁLCULO → CUSTO → PREMISSA → EVIDÊNCIA → PTS PÓS → VALIDAÇÃO → APRENDIZADO`
