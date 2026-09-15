# ELO — Memória Cognitiva de Orçamentos

**Versão:** 1.0  
**Status:** Estrutura canônica de memória — registros somente após validação  
**Domínio:** Orçamento  
**Autoridade:** ELO Cognitivo/Governance

## 1. Finalidade

Esta memória consolida conhecimento reutilizável derivado de orçamentos, sem substituir a documentação vigente de uma SO, a memória de cálculo estruturada ou as tabelas persistentes do ELO.

Ela deve responder ao próximo orçamento com contexto, precedentes, relações e riscos, mantendo a origem de cada aprendizado.

## 2. Regra fundamental

```text
ORÇAMENTO EXECUTADO
→ evidências
→ conferência
→ PTS Pós-Orçamento
→ aprendizado candidato
→ validação
→ memória cognitiva
```

Uma SO isolada não cria automaticamente uma regra geral.

## 3. O que pode ser aprendido

### 3.1 Soluções e materiais
- padrões de fabricação;
- equivalências técnicas validadas;
- materiais recorrentes;
- excedentes recorrentes;
- customizações recorrentes;
- relações entre requisito e solução.

### 3.2 Cálculos
- fórmulas;
- parâmetros;
- fatores de consumo;
- produtividade;
- composição de mão de obra;
- relações quantitativas;
- condições de aplicação.

### 3.3 Custos
- estruturas de composição;
- fontes de preço;
- comportamentos históricos;
- diferenças entre estimativa e resultado;
- fatores de custo relevantes.

Preço histórico nunca deve ser aplicado como preço atual sem validação vigente.

### 3.4 Logística
- relações entre local, prazo e mobilização;
- necessidades recorrentes de transporte;
- hospedagem e deslocamento;
- condições de acesso;
- padrões de mobilização/desmobilização.

### 3.5 Riscos e divergências
- requisitos frequentemente ambíguos;
- conflitos documentais;
- omissões recorrentes;
- itens frequentemente esquecidos;
- diferenças entre PTS Técnica e orçamento;
- causas de contestação e correção.

## 4. Estrutura de um aprendizado

Cada aprendizado deve preservar:

| Campo | Conteúdo |
|---|---|
| ID | identificador único |
| Tipo | cálculo, material, solução, logística, risco, processo etc. |
| Regra | conhecimento resumido |
| Contexto | quando se aplica |
| Variáveis | parâmetros necessários |
| Aplicação | como reutilizar |
| Exceções | quando não aplicar |
| Evidências | referências verificáveis |
| SOs de origem | precedentes utilizados |
| Confiança | nível justificado pela evidência |
| Risco | consequência de aplicação incorreta |
| Status | OBSERVADO/CANDIDATO/VALIDADO/REJEITADO/SUPERADO |
| Data | registro/validação |

## 5. Memória de cálculo

Memória de cálculo deve preservar, no mínimo:

```text
OBJETIVO
ENTRADAS
UNIDADES
FÓRMULA
PARÂMETROS
SUBSTITUIÇÃO
RESULTADO
ARREDONDAMENTO
PREMISSA
EVIDÊNCIA
VALIDAÇÃO
```

O resultado numérico sem a cadeia de cálculo não constitui memória de cálculo suficiente.

## 6. Relação com as estruturas persistentes

Esta memória textual é índice/contexto cognitivo. A persistência estruturada deve continuar nas estruturas canônicas de orçamento, incluindo:

- `elo_orcamento_memoria`
- `elo_orcamento_calculos_aprendidos`
- `elo_orcamento_calculo_varreduras`
- `elo_orcamento_calculo_evidencias`
- `elo_orcamento_decisoes`
- `elo_orcamento_associacoes`

Não criar outra tabela, registro mestre ou mecanismo de memória apenas para suportar este Markdown.

## 7. Recuperação para um novo orçamento

Ao encontrar novo requisito:

```text
NOVO REQUISITO
→ localizar precedentes
→ comparar contexto
→ verificar equivalência
→ verificar validade da evidência
→ identificar diferenças
→ substituir variáveis
→ recalcular
→ validar
→ sugerir aplicação
```

O ELO deve apresentar o precedente como referência, não como verdade automática.

## 8. Relações cognitivas

Os aprendizados devem poder ser associados por:

`REQUISITO ↔ SOLUÇÃO ↔ MATERIAL ↔ QUANTITATIVO ↔ CÁLCULO ↔ CUSTO ↔ LOGÍSTICA ↔ RISCO ↔ RESULTADO`

Uma associação só deve ser promovida quando houver evidência suficiente para justificar a relação.

## 9. Aprendizado pós-orçamento

Após cada orçamento, avaliar:

1. o que foi previsto corretamente;
2. o que foi corrigido;
3. o que foi omitido;
4. o que foi contestado;
5. qual premissa causou impacto;
6. quais cálculos foram reutilizáveis;
7. quais padrões se repetiram;
8. quais hipóteses devem ser descartadas;
9. quais relações merecem nova validação.

## 10. Controle de validade

Um aprendizado deve ser marcado como `SUPERADO` quando uma regra mais recente e melhor evidenciada substituir sua aplicação.

Conflitos entre aprendizados não devem ser resolvidos por preferência textual. Devem considerar contexto, vigência, evidência, recorrência e autoridade da fonte.

## 11. Segurança cognitiva

Nunca registrar como conhecimento:

- credenciais;
- tokens;
- chaves privadas;
- segredos de fornecedores;
- dados sensíveis desnecessários;
- informação sem origem identificável apresentada como fato.

## 12. Potencialização para o ELO

Esta memória permite que o ELO deixe de tratar cada orçamento como evento isolado e passe a reconhecer relações entre experiências, cálculos, soluções, custos e resultados, mantendo evidência, contexto, validade e possibilidade de correção.
