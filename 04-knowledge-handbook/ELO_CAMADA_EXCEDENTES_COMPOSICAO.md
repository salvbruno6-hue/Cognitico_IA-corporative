# ELO — CAMADA DE EXCEDENTES E COMPOSIÇÃO

**Camada:** `04-knowledge-handbook`  
**Função:** núcleo especializado para identificar, classificar, quantificar, compor e reutilizar excedentes de fabricação, adaptação, instalação e implantação.

## 1. Finalidade

Esta camada existe para que o ELO não trate excedente como simples descrição textual. Todo excedente deve poder ser convertido em uma composição orçamentária rastreável.

Fluxo obrigatório:

`REQUISITO → BASE PADRÃO → ALTERAÇÃO → EXCEDENTE → QUANTITATIVO → INSUMOS → RECURSOS → MÃO DE OBRA → IMPACTOS → VALOR`

## 2. Separação entre padrão e excedente

Antes de classificar um item como excedente, identificar o que já pertence à solução-base.

Categorias mínimas:

- **PAD** — componente padrão da base;
- **EXC** — alteração ou acréscimo além da base;
- **REM** — remoção/demolição de componente existente;
- **ADP** — adaptação necessária para compatibilização;
- **ESP** — item especial solicitado pela SO;
- **CLI** — item dependente de definição/validação do cliente.

Não classificar como excedente aquilo que já estiver incorporado ao modelo/base adotado.

## 3. Matriz de composição do excedente

Para cada excedente registrar:

| Campo | Conteúdo |
|---|---|
| ID | identificador único |
| SO | solicitação de origem |
| Requisito | origem documental |
| Base | modelo/produto de referência |
| Tipo | PAD/EXC/REM/ADP/ESP/CLI |
| Descrição | alteração objetiva |
| Quantidade | quantitativo calculado |
| Unidade | m, m², m³, un, kg, h, diária etc. |
| Material | insumos principais |
| Componentes | itens auxiliares |
| Mão de obra | função e quantidade de horas/dias |
| Equipamentos | máquinas/ferramentas/recursos |
| Logística | transporte/mobilização aplicável |
| Perdas | percentual ou quantidade justificada |
| Custo direto | composição antes de indiretos |
| Indiretos | custos aplicáveis |
| Valor | resultado da composição |
| Premissa | hipótese utilizada |
| Evidência | documento, histórico ou validação |
| Confiança | confirmada/estimada/pendente |

## 4. Regras de cálculo

Nunca atribuir valor global ao excedente sem identificar sua lógica de formação.

Quando possível:

`VALOR EXCEDENTE = Σ(QUANTIDADE × CUSTO UNITÁRIO) + MÃO DE OBRA + EQUIPAMENTOS + LOGÍSTICA + OUTROS IMPACTOS APLICÁVEIS`

Quando o preço for obtido por referência histórica ou fornecedor, registrar a fonte e a data/base da referência.

## 5. Reutilização

Excedentes validados podem alimentar uma biblioteca de composições reutilizáveis. A reutilização deve preservar contexto, unidade, escopo, base tecnológica e data da referência.

Um histórico não deve ser aplicado automaticamente quando houver mudança relevante de modelo, material, local, escala, norma ou condição de execução.

## 6. Interface com o Especialista

O Especialista consulta esta camada para descobrir composições recorrentes. O ELO utiliza o resultado para comparar cenários.

`ELO → IDENTIFICA NECESSIDADE → CAMADA EXCEDENTES → COMPOSIÇÃO → ESPECIALISTA → ORÇAMENTO`

## 7. Interface com aprendizado

Somente excedentes conferidos e tecnicamente explicados podem virar padrão reutilizável.

`EXCEDENTE REAL → CONFERÊNCIA → VALIDAÇÃO → COMPOSIÇÃO PADRONIZADA → BIBLIOTECA → NOVA SO`

## 8. Controle de qualidade

A camada deve detectar:

- duplicidade entre base e excedente;
- unidade incompatível;
- quantitativo sem origem;
- preço sem referência;
- composição incompleta;
- mão de obra omitida;
- logística omitida;
- perdas sem justificativa;
- excedente classificado sem evidência;
- reutilização fora do contexto original.
