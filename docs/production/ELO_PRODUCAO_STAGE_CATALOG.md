# ELO — Catálogo Governado de Etapas de Produção

**ID:** ELO-PROD-STAGE-001  
**Status:** PROPOSTA CONTROLADA — levantamento e validação  
**Versão:** 1.0  
**Data:** 2026-09-16  
**Autoridade canônica:** ELO Cognitivo / GitHub  
**Domínio:** PRODUÇÃO  
**Dependência:** `ELO_PRODUCAO_FOUNDATION_CONTRACT.md`

## 1. Finalidade

Estabelecer o primeiro catálogo estruturado das etapas de produção já documentadas no fluxo operacional da Multiteiner, preparando sua futura implementação no Core, persistência e ELO Web sem transformar uma referência de processo em regra física definitiva.

Este catálogo é uma estrutura de levantamento. Ele não define tempos padrão, capacidade, produtividade, quantidade de operadores, custos ou metas.

## 2. Fonte operacional

O fluxo de referência atualmente documentado apresenta a seguinte sequência para Produção Modular:

```text
Triagem
→ Chassi
→ Escovação
→ Pintura de tratamento
→ Acabamento branco
→ Estoque de estruturas
→ Movimentação
→ Piso
→ Teto
→ Colunas
→ Trilho
→ Pintura modular
→ Paredes
→ Instalações
→ Acabamento
→ Testes
→ Liberação
```

A própria fonte classifica essa sequência como **referência operacional**, determinando que tempos, capacidade e critérios de passagem sejam obtidos de dados e documentos validados.

## 3. Modelo de registro

Cada etapa deve evoluir para um registro com, no mínimo:

| Campo | Finalidade | Estado inicial |
|---|---|---|
| `stage_id` | Identificador estável da etapa | A definir |
| `stage_code` | Código operacional | A definir |
| `stage_name` | Nome da etapa | Documentado |
| `flow_type` | Linha modular/customizada/reparo | A validar |
| `sequence_reference` | Posição na sequência documentada | Documentado para linha modular |
| `input_reference` | Entrada esperada | A validar |
| `output_reference` | Saída esperada | A validar |
| `dependency_reference` | Dependências | A validar |
| `resource_reference` | Recurso/centro envolvido | A validar |
| `evidence_reference` | Evidência de execução | A validar |
| `quality_gate_reference` | Critério/gate de qualidade | A validar |
| `status` | Estado do cadastro | PROPOSTA |
| `source_reference` | Origem da informação | Obrigatório |
| `validation_status` | Validação do registro | A VALIDAR |

## 4. Catálogo inicial

| Seq. | Etapa | Fluxo | Entrada | Saída | Dependência | Status |
|---:|---|---|---|---|---|---|
| 01 | Triagem | Modular | A validar | A validar | A validar | A VALIDAR |
| 02 | Chassi | Modular | A validar | A validar | Triagem | A VALIDAR |
| 03 | Escovação | Modular | A validar | A validar | Chassi | A VALIDAR |
| 04 | Pintura de tratamento | Modular | A validar | A validar | Escovação | A VALIDAR |
| 05 | Acabamento branco | Modular | A validar | A validar | Pintura de tratamento | A VALIDAR |
| 06 | Estoque de estruturas | Modular | Estrutura acabada | A validar | Acabamento branco | A VALIDAR |
| 07 | Movimentação | Modular | Estrutura disponível | A validar | Estoque de estruturas | A VALIDAR |
| 08 | Piso | Modular | A validar | A validar | Movimentação | A VALIDAR |
| 09 | Teto | Modular | A validar | A validar | Piso | A VALIDAR |
| 10 | Colunas | Modular | A validar | A validar | Teto | A VALIDAR |
| 11 | Trilho | Modular | A validar | A validar | Colunas | A VALIDAR |
| 12 | Pintura modular | Modular | A validar | A validar | Trilho | A VALIDAR |
| 13 | Paredes | Modular | A validar | A validar | Pintura modular | A VALIDAR |
| 14 | Instalações | Modular | A validar | A validar | Paredes | A VALIDAR |
| 15 | Acabamento | Modular | A validar | A validar | Instalações | A VALIDAR |
| 16 | Testes | Modular | Produto em acabamento final | Resultado de teste | Acabamento | A VALIDAR |
| 17 | Liberação | Modular | Produto testado | Produto liberado ou retenção | Testes | A VALIDAR |

**Observação:** as dependências acima representam a ordem de referência documentada e não devem ser interpretadas como sequência física definitiva até validação operacional.

## 5. Estados da etapa

O estado operacional futuro deverá ser definido a partir do modelo existente de `ordem_producao_etapa`. Este documento não cria uma nova máquina de estados.

Como requisito mínimo, uma etapa precisa permitir distinguir entre:

- não iniciada;
- em execução;
- concluída;
- bloqueada;
- retida por qualidade;
- retrabalho, quando aplicável.

Os valores definitivos devem ser reconciliados com o modelo físico existente antes da implementação.

## 6. Evidência mínima

Para permitir rastreabilidade, a execução de uma etapa deverá futuramente poder apontar para evidência compatível com o processo, como:

- apontamento de execução;
- quantidade produzida;
- data/hora;
- ordem de produção;
- operador/equipe, quando aplicável;
- inspeção ou teste;
- ocorrência/desvio;
- retrabalho;
- evento de processo.

A lista acima é requisito de informação, não autorização para criar novos campos ou tabelas sem verificar as estruturas existentes.

## 7. Relação com Qualidade

A fundação do domínio determina que a qualidade possa apontar para a etapa em que a evidência foi produzida.

Portanto, a futura implementação deve preservar a relação:

```text
ORDEM_PRODUÇÃO
      ↓
ETAPA
      ↓
EVIDÊNCIA DE EXECUÇÃO
      ↓
INSPEÇÃO / TESTE
      ↓
LIBERAÇÃO ou NÃO CONFORMIDADE
```

Falhas devem permanecer vinculadas ao módulo/produto, etapa, causa, intervenção e resultado, conforme o fluxo operacional documentado.

## 8. Relação com materiais

A etapa não deve inventar materiais. A necessidade de material deve derivar das estruturas governadas de Lista-Material e seus itens, conforme a fundação do domínio PRODUÇÃO.

```text
ORDEM PCP
   ↓
LISTA-MATERIAL
   ↓
LISTA-MATERIAL_ITEM
   ↓
ABASTECIMENTO
   ↓
ETAPA DE PRODUÇÃO
```

## 9. Relação com Produção Customizada

A documentação existente diferencia Produção Modular e Produção Customizada. O catálogo deve permitir que uma mesma etapa seja reutilizada quando aplicável, sem presumir que toda customização siga exatamente a mesma sequência.

A implementação deverá preservar a distinção entre:

- modelo padrão;
- variação;
- excedente;
- customização.

## 10. Regras de governança

1. Este catálogo não é autoridade sobre o processo físico enquanto estiver em `A VALIDAR`.
2. Toda etapa precisa possuir origem rastreável.
3. Não criar uma tabela nova de etapas se `ordem_producao_etapa` puder atender ao contrato após fortalecimento.
4. Não duplicar catálogo em Core, Supabase ou ELO Web com autoridade própria.
5. Código futuro deve consumir o contrato canônico, não redefini-lo silenciosamente.
6. Alterações de sequência devem preservar histórico e origem.
7. Tempos, capacidades, equipes e produtividade somente entram após evidência validada.
8. Uma customização específica não altera automaticamente o padrão de produção.
9. Qualquer conflito entre documentação e operação observada deve ser registrado para validação, não resolvido por inferência.
10. Promoção de uma estrutura para regra canônica exige o ciclo de evolução governado.

## 11. Critério para implementação física

Antes de criar ou alterar tabelas, APIs ou componentes, executar:

```text
CATÁLOGO
→ MAPA CONTRA MODELO EXISTENTE
→ IDENTIFICAÇÃO DE LACUNAS
→ REUSE
→ STRENGTHEN
→ REFACTOR, se necessário
→ EVIDÊNCIA
→ VALIDAÇÃO
→ EVOLUTION GATE
→ IMPLEMENTAÇÃO
```

## 12. Próxima etapa

A próxima etapa é produzir o **mapa de compatibilidade entre este catálogo e `ordem_producao_etapa`**, incluindo identificação das estruturas físicas existentes, campos reaproveitáveis, campos ausentes e possíveis lacunas.

Somente depois desse mapa deve ser definido se haverá alteração de banco, código do Core ou componente do ELO Web.
