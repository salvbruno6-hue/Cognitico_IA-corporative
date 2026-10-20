# MULTITEINER — GUIAS DE ORIENTAÇÃO PARA ALIMENTAÇÃO DAS TABELAS

## Finalidade

Este documento transforma o fluxo visual em **trabalho orientado de implantação de dados**.

Cada seção abaixo representa uma tabela operacional. O objetivo não é pedir ao especialista que “preencha o banco”, mas fazer o ELO conduzir a coleta do significado operacional, registrar a fonte, validar unidade/periodicidade e somente então orientar a inserção.

## Fluxo mestre

`AF → Planejamento → Almoxarifado/Compras → Produção → Reparo quando necessário → Expedição/Externa → Campo → Evidência → Aprendizado`

## Regra de trabalho com especialistas

1. ELO apresenta o objetivo da tabela no fluxo.
2. ELO identifica o responsável pelo dado.
3. ELO pergunta como o processo realmente ocorre.
4. ELO traduz a resposta para os campos existentes.
5. Especialista confirma significado, unidade, evento e momento de registro.
6. ELO registra a fonte/evidência.
7. Só depois ocorre inserção.
8. Campo sem evidência permanece **NÃO LOCALIZADO**.
9. Não criar relacionamento físico inexistente apenas porque o fluxo conceitual sugere uma relação.
10. Toda diferença entre planejado e realizado deve permanecer visível.

## Contrato mínimo de cada sessão

| Elemento | Obrigatório |
|---|---|
| Tabela | ✓ |
| Operação do fluxo | ✓ |
| Responsável | ✓ |
| Significado do dado | ✓ |
| Fonte | ✓ |
| Unidade | ✓ |
| Momento de registro | ✓ |
| Evidência aceita | ✓ |
| Regra de validação | ✓ |
| Exemplo real | quando disponível |
| Aprovação do especialista | ✓ |

## Regra ELO

`pergunta → resposta do especialista → confronto com schema → validação → inserção autorizada`

O ELO não deve usar valores padrão, completar lacunas por plausibilidade ou transformar descrição verbal em regra permanente sem validação.

---

## 1. `mt_pedidos_venda`

**Operação do fluxo:** 01 Comercial  
**Papel:** Cabeçalho da AF/pedido

### Dados a orientar

número, cliente, tipo, recebimento, entrega solicitada, gate PCP

### Perguntas obrigatórias ao especialista

- Como a AF entra? Quando é considerada recebida? Qual gate libera o PCP?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 2. `mt_pedidos_venda_itens`

**Operação do fluxo:** 01 Comercial  
**Papel:** Demanda por módulo/item

### Dados a orientar

modelo, quantidade, data solicitada, personalização

### Perguntas obrigatórias ao especialista

- Qual módulo foi solicitado? Quantos? É personalizado? Qual prazo?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 3. `mt_contratos_locacao`

**Operação do fluxo:** 01 Comercial / Campo  
**Papel:** Vínculo contratual da locação

### Dados a orientar

contrato, unidade, cliente, vigência e condições conforme schema

### Perguntas obrigatórias ao especialista

- Qual contrato governa a unidade e quais eventos devem ser acompanhados?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 4. `mt_planos_pcp`

**Operação do fluxo:** 02 Planejamento  
**Papel:** Plano agregado de produção

### Dados a orientar

código, versão, horizonte, status, aprovação

### Perguntas obrigatórias ao especialista

- Qual é o horizonte? O que foi aprovado e por quem?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 5. `mt_linhas_plano_pcp`

**Operação do fluxo:** 02 Planejamento  
**Papel:** Demanda transformada em linha planejada

### Dados a orientar

pedido/item, modelo, quantidade, início/fim, prioridade

### Perguntas obrigatórias ao especialista

- Como a demanda virou quantidade e janela de produção?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 6. `mt_versoes_roteiro_personalizado`

**Operação do fluxo:** 02 Planejamento  
**Papel:** Configuração de roteiro para pedido personalizado

### Dados a orientar

pedido/item, modelo base, versão, status, aprovação

### Perguntas obrigatórias ao especialista

- O que mudou em relação ao roteiro padrão e qual aprovação sustenta a mudança?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 7. `mt_operacoes_roteiro_personalizado`

**Operação do fluxo:** 02 Planejamento / Produção  
**Papel:** Etapas do roteiro personalizado

### Dados a orientar

sequência, operação, centro, tempos padrão/setup

### Perguntas obrigatórias ao especialista

- Quais operações foram adicionadas, removidas ou alteradas?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 8. `lista_mae`

**Operação do fluxo:** 02 Planejamento / 03 Almoxarifado  
**Papel:** Identidade canônica do material

### Dados a orientar

código, descrição, aplicação, unidade, valor, modelos

### Perguntas obrigatórias ao especialista

- Qual item é este? Qual código canônico deve ser usado?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 9. `kits`

**Operação do fluxo:** 02 Planejamento / 03 Almoxarifado  
**Papel:** Agrupador de materiais para instalação/função

### Dados a orientar

código, nome, modelo, versão, tipo

### Perguntas obrigatórias ao especialista

- O que compõe o kit e em qual etapa ele é usado?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 10. `kit_itens`

**Operação do fluxo:** 02 Planejamento / 03 Almoxarifado  
**Papel:** Composição do kit

### Dados a orientar

material, quantidade, instalação, fase, obrigatoriedade, fonte

### Perguntas obrigatórias ao especialista

- Qual material entra, em que quantidade e com qual condição de uso?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 11. `excedentes`

**Operação do fluxo:** 02 Planejamento / 04 Compras  
**Papel:** Cabeçalho da exceção/excedente

### Dados a orientar

código, tipo instalação, descrição, unidade, origem, custo

### Perguntas obrigatórias ao especialista

- Por que o excedente existe e qual é sua origem documental?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 12. `excedente_itens`

**Operação do fluxo:** 02 Planejamento / 04 Compras  
**Papel:** Materiais do excedente

### Dados a orientar

item, descrição, quantidade, unidade, tipo de componente

### Perguntas obrigatórias ao especialista

- Qual material adicional foi realmente solicitado?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 13. `excedente_mao_obra`

**Operação do fluxo:** 02 Planejamento / Orçamento  
**Papel:** Mão de obra prevista no excedente

### Dados a orientar

função, quantidade, tempo, unidade, valor

### Perguntas obrigatórias ao especialista

- Qual atividade de mão de obra está prevista e como foi definida?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 14. `mt_locais`

**Operação do fluxo:** 03 Almoxarifado / 07 Expedição  
**Papel:** Cadastro físico de locais

### Dados a orientar

local e função operacional conforme schema

### Perguntas obrigatórias ao especialista

- O local representa CD, picking, pátio, base, expedição ou outro?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 15. `mt_lotes_estoque`

**Operação do fluxo:** 03 Almoxarifado  
**Papel:** Saldo físico por lote/serial/local

### Dados a orientar

item, lote/serial, local, disponível, reservado, status

### Perguntas obrigatórias ao especialista

- Qual saldo está fisicamente disponível, reservado ou bloqueado?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 16. `mt_movimentacoes_estoque`

**Operação do fluxo:** 03 Almoxarifado  
**Papel:** Histórico de movimentação física

### Dados a orientar

item/lote, origem, destino, quantidade, tipo, referência, data

### Perguntas obrigatórias ao especialista

- O que foi movimentado, de onde, para onde e por qual evento?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 17. `mt_ordens_compra`

**Operação do fluxo:** 04 Compras  
**Papel:** Cabeçalho da ordem de compra

### Dados a orientar

fornecedor, número, status, pedido, previsão

### Perguntas obrigatórias ao especialista

- Quando a compra foi autorizada e qual previsão foi assumida?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 18. `mt_ordens_compra_itens`

**Operação do fluxo:** 04 Compras  
**Papel:** Item da ordem de compra

### Dados a orientar

material, quantidade pedida/recebida, custo, necessidade

### Perguntas obrigatórias ao especialista

- Quanto foi pedido, quanto chegou e para quando era necessário?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 19. `compras_fornecedor`

**Operação do fluxo:** 04 Compras  
**Papel:** Registro comercial da compra

### Dados a orientar

fornecedor, número, data, origem, documento, status

### Perguntas obrigatórias ao especialista

- Qual documento comercial comprova a compra?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 20. `compras_fornecedor_itens`

**Operação do fluxo:** 04 Compras  
**Papel:** Itens da compra do fornecedor

### Dados a orientar

material, quantidade, valor, entrega prevista/real

### Perguntas obrigatórias ao especialista

- Qual item foi contratado e qual foi a data real de entrega?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 21. `fluxo_produtivo_modular`

**Operação do fluxo:** 05 Produção  
**Papel:** Definição do fluxo produtivo

### Dados a orientar

código, nome, modelo/taxonomia, versão, lead time, capacidade referência

### Perguntas obrigatórias ao especialista

- Qual fluxo se aplica ao modelo e qual é a finalidade de cada fluxo?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 22. `fluxo_produtivo_modular_etapas`

**Operação do fluxo:** 05 Produção  
**Papel:** Decomposição do fluxo

### Dados a orientar

ordem, processo, recurso, tempos, capacidade, dependências, materiais, qualidade

### Perguntas obrigatórias ao especialista

- O que acontece em cada etapa, o que depende dela e como se confirma conclusão?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 23. `mt_ordens_producao`

**Operação do fluxo:** 05 Produção  
**Papel:** Ordem formal de produção

### Dados a orientar

modelo, quantidade planejada/produzida, datas planejadas/reais, status

### Perguntas obrigatórias ao especialista

- Qual OP foi aberta e qual é o realizado comprovado?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 24. `mt_operacoes_roteiro`

**Operação do fluxo:** 05 Produção  
**Papel:** Roteiro padrão do modelo

### Dados a orientar

sequência, operação, centro, minutos padrão/setup, paralelismo

### Perguntas obrigatórias ao especialista

- Qual operação pertence ao roteiro padrão e qual centro a executa?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 25. `mt_operacoes_ordem_producao`

**Operação do fluxo:** 05 Produção  
**Papel:** Execução planejada/realizada por operação

### Dados a orientar

quantidades, sequência, status, datas planejadas/reais

### Perguntas obrigatórias ao especialista

- Quanto deveria ocorrer e quanto foi efetivamente concluído em cada operação?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 26. `mt_capacidade_diaria`

**Operação do fluxo:** 05 Produção  
**Papel:** Capacidade por centro e dia

### Dados a orientar

data, padrão, recuperação, bloqueada, disponível

### Perguntas obrigatórias ao especialista

- Qual capacidade existia naquela data e o que a reduziu?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 27. `mt_eventos_fluxo_modular`

**Operação do fluxo:** 05 Produção  
**Papel:** Apontamento real do fluxo

### Dados a orientar

unidade, centro, operação, evento, início/fim, quantidade, operador

### Perguntas obrigatórias ao especialista

- Qual evento comprova que a operação aconteceu?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 28. `mt_ordens_montagem`

**Operação do fluxo:** 05 Produção  
**Papel:** Ordem de montagem ligada à fabricação

### Dados a orientar

OP, data, quantidade planejada/realizada, status, recuperação

### Perguntas obrigatórias ao especialista

- Qual montagem foi planejada, realizada e se foi recuperação?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 29. `mt_inspecoes`

**Operação do fluxo:** 05 Produção / Qualidade  
**Papel:** Inspeção/teste de qualidade

### Dados a orientar

objeto inspecionado, resultado e evidência conforme schema

### Perguntas obrigatórias ao especialista

- Qual inspeção comprova OK ou reprovação?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 30. `mt_nao_conformidades`

**Operação do fluxo:** 05 Produção / 06 Reparo  
**Papel:** Registro de desvio

### Dados a orientar

não conformidade, tipo, status, evidência e vínculo operacional conforme schema

### Perguntas obrigatórias ao especialista

- Qual desvio ocorreu e qual evidência o sustenta?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 31. `mt_ordens_reparo`

**Operação do fluxo:** 06 Reparo  
**Papel:** Ordem de recuperação do módulo

### Dados a orientar

unidade, não conformidade, tipo, diagnóstico, início/fim, aprovação

### Perguntas obrigatórias ao especialista

- Por que o reparo foi aberto? Qual diagnóstico foi registrado? Quando foi liberado?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 32. `mt_eventos_reparo`

**Operação do fluxo:** 06 Reparo  
**Papel:** Execução real do reparo

### Dados a orientar

ordem, disciplina, evento, início/fim, horas, custo material

### Perguntas obrigatórias ao especialista

- Qual oficina executou, quanto tempo consumiu e qual material foi registrado?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 33. `mt_unidades_modulares`

**Operação do fluxo:** 05 Produção / 06 Reparo / 07 Expedição  
**Papel:** Identidade operacional do módulo

### Dados a orientar

código da unidade, modelo, OP/pedido, local, qualidade, disponibilidade

### Perguntas obrigatórias ao especialista

- Qual unidade física está sendo acompanhada e qual é seu estado atual?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 34. `mt_ordens_montagem_externa`

**Operação do fluxo:** 07 Externa  
**Papel:** Ordem de montagem no cliente/local

### Dados a orientar

pedido, localização, tipo, status, datas planejadas/reais, horas

### Perguntas obrigatórias ao especialista

- Qual serviço externo foi planejado e qual foi realizado?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 35. `mt_montagem_externa_modulos`

**Operação do fluxo:** 07 Externa  
**Papel:** Vínculo da unidade à montagem externa

### Dados a orientar

ordem, módulo e contexto da montagem

### Perguntas obrigatórias ao especialista

- Qual unidade foi instalada nessa ordem externa?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 36. `mt_eventos_montagem_externa`

**Operação do fluxo:** 07 Externa  
**Papel:** Eventos reais da montagem externa

### Dados a orientar

ordem, módulo, pessoa, tipo, data/hora, localização

### Perguntas obrigatórias ao especialista

- Que evento ocorreu, com quem, quando e onde?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 37. `mt_mao_obra_montagem_externa`

**Operação do fluxo:** 07 Externa  
**Papel:** Apontamento de mão de obra externa

### Dados a orientar

ordem, módulo, pessoa, função, atividade, início/fim, horas

### Perguntas obrigatórias ao especialista

- Quem executou qual atividade e quantas horas foram apontadas?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 38. `mt_expedicoes`

**Operação do fluxo:** 07 Expedição  
**Papel:** Cabeçalho da saída

### Dados a orientar

expedição, destino, status e datas conforme schema

### Perguntas obrigatórias ao especialista

- Qual gate liberou a saída e qual documento comprova a expedição?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 39. `mt_expedicao_itens`

**Operação do fluxo:** 07 Expedição  
**Papel:** Itens efetivamente expedidos

### Dados a orientar

unidade/item, quantidade e vínculo com expedição conforme schema

### Perguntas obrigatórias ao especialista

- Quais unidades e kits saíram? Em que quantidade?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 40. `mt_eventos_campo`

**Operação do fluxo:** 07 Campo  
**Papel:** Ocorrências após saída/locação

### Dados a orientar

contrato, unidade, evento, data, localização, descrição

### Perguntas obrigatórias ao especialista

- O que ocorreu no campo e qual unidade/contrato foi afetado?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 41. `rh_mao_obra_custos`

**Operação do fluxo:** 06 Reparo / 07 Externa / Custos  
**Papel:** Base de custo de mão de obra

### Dados a orientar

cargo, referência, custo mensal/dia, fonte, vigência

### Perguntas obrigatórias ao especialista

- Qual fonte e período sustentam o custo usado?
- Qual é a fonte original desse dado?
- Em que momento ele deve ser registrado?
- Qual unidade/período deve ser utilizado?
- O que significa “concluído”, “disponível”, “realizado” ou equivalente nessa operação?
- Que evidência comprova o registro?

### Regra de inserção pelo ELO

O ELO deve orientar o preenchimento somente depois de confirmar o significado operacional com o responsável. Valores de exemplo ou estimativas não devem ser inseridos como dados reais.

### Validação cruzada

Antes de considerar a informação válida, o ELO deve verificar se ela é compatível com as tabelas anteriores/posteriores do fluxo. Se a relação física não existir no schema, registrar a relação como **conceitual** até que seja formalmente criada e validada.

### Saída da orientação

`DADO VALIDADO | DADO INCOMPLETO | DIVERGÊNCIA DE FONTES | NÃO LOCALIZADO`

---

## 42. Regra especial para tabelas de execução

As tabelas de execução — especialmente `mt_eventos_fluxo_modular`, `mt_eventos_reparo`, `mt_eventos_montagem_externa`, `mt_mao_obra_montagem_externa` e `mt_movimentacoes_estoque` — devem ser tratadas como **evidência do realizado**.

Não derivar realizado apenas de datas planejadas.

## 43. Regra especial para planejamento

`mt_planos_pcp`, `mt_linhas_plano_pcp`, `mt_ordens_producao` e roteiros representam intenção/programação. Seus campos reais só podem ser preenchidos por evidência operacional.

## 44. Regra especial para reparo

Reparo deve manter a cadeia:

`não conformidade/ocorrência → ordem de reparo → eventos → materiais/mão de obra → inspeção/liberação`

Quando algum elo não estiver registrado, o ELO deve apontar o gap em vez de reconstruí-lo por inferência.

## 45. Regra especial para montagem externa

Montagem externa deve manter separadas:

- ordem planejada;
- execução real;
- eventos;
- pessoa/função/atividade;
- horas;
- localização.

Isso permite obter posteriormente produtividade, custo e desvios sem transformar estimativa em realizado.

## 46. Estado atual verificado no Supabase

As tabelas operacionais principais do PCP/execução consultadas estão atualmente sem registros operacionais, enquanto `fluxo_produtivo_modular` possui 1 fluxo e `fluxo_produtivo_modular_etapas` possui 17 etapas. `excedente_mao_obra` possui 29 registros e `rh_mao_obra_custos` possui 3 registros.

Portanto, esta documentação é uma **estrutura de implantação/orientação**, não uma declaração de que a operação já esteja alimentada.

## 47. Relação com Symbiont

As tabelas são fontes de evidência operacional. O domínio PCP/Operações interpreta os dados; o Symbiont recebe evidência pelo contrato canônico para observação, aprendizado/adaptação e Evolution Gate.

Não criar memória, router, lifecycle ou autoridade de aprendizado dentro destes guias.
