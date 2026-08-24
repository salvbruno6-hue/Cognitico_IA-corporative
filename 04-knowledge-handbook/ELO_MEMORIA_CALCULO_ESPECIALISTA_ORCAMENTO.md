# ELO — MEMÓRIA DE CÁLCULO DO ESPECIALISTA DE ORÇAMENTO

**Camada:** `04-knowledge-handbook`  
**Função:** registrar não apenas o valor final, mas o raciocínio, as variáveis, premissas e sequência de cálculo que produziram o valor.

## 1. Finalidade

A memória de cálculo transforma um orçamento em conhecimento reutilizável. O ELO deve conseguir entender **como** um valor foi obtido e reaplicar a lógica em outro cenário quando as condições forem comparáveis.

Regra:

`VALOR FINAL ≠ CONHECIMENTO`

O conhecimento está na cadeia:

`ENTRADA → PREMISSA → FÓRMULA → CÁLCULO → RESULTADO → VALIDAÇÃO`

## 2. Estrutura mínima

Cada cálculo relevante deve registrar:

| Campo | Função |
|---|---|
| ID | identificação da memória |
| SO | origem |
| Item | item orçamentário |
| Objetivo | o que está sendo calculado |
| Entradas | dados utilizados |
| Unidade | unidade de cada entrada |
| Fonte | origem de cada dado |
| Premissas | hipóteses adotadas |
| Fórmula | lógica matemática |
| Etapas | sequência do cálculo |
| Resultado intermediário | resultados por etapa |
| Resultado final | valor/quantidade obtida |
| Sensibilidade | variáveis que mais alteram o resultado |
| Validação | conferência realizada |
| Confiança | alta/média/baixa |
| Contexto | condições de aplicabilidade |

## 3. Forma de raciocínio

Toda memória deve ser escrita de maneira reproduzível:

```text
DADO
↓
UNIDADE
↓
PREMISSA
↓
FÓRMULA
↓
SUBCÁLCULO
↓
RESULTADO
↓
ARREDONDAMENTO, SE HOUVER
↓
VALOR FINAL
```

Não registrar apenas: `valor = R$ X`.

Registrar: `valor = quantidade × referência unitária`, identificando de onde vieram quantidade e referência.

## 4. Exemplos de lógica reutilizável

### 4.1 Hospedagem

```text
DIAS DE HOSPEDAGEM = DIAS DE EXECUÇÃO COM PERNOITE
```

Se o último dia for dia de retorno para casa e não houver pernoite:

```text
HOSPEDAGEM = DIAS DE EXECUÇÃO - 1
```

A regra só deve ser aplicada quando o cenário documental/logístico confirmar retorno no último dia.

### 4.2 Composição de excedente

```text
CUSTO DO EXCEDENTE
= MATERIAL
+ MÃO DE OBRA
+ EQUIPAMENTOS
+ LOGÍSTICA
+ OUTROS IMPACTOS APLICÁVEIS
```

### 4.3 Mobilização

A lógica deve separar os componentes que dependem de distância, duração, quantidade de colaboradores e meio de transporte.

```text
CUSTO LOGÍSTICO
= TRANSPORTE
+ DESLOCAMENTOS LOCAIS
+ HOSPEDAGEM
+ ALIMENTAÇÃO
+ CARRO DE APOIO
+ OUTROS CUSTOS APLICÁVEIS
```

A referência de mais de 6 horas é um parâmetro operacional para avaliar alternativa aérea versus terrestre, e não uma regra contratual universal.

## 5. Memória como padrão transferível

Quando uma nova SO possuir estrutura semelhante, o ELO pode reutilizar a **lógica**, não necessariamente os números.

Processo:

`MEMÓRIA EXISTENTE → COMPARAR CONTEXTO → IDENTIFICAR VARIÁVEIS → SUBSTITUIR ENTRADAS → RECALCULAR → VALIDAR`

Nunca copiar automaticamente o valor final de outra SO.

## 6. Sensibilidade

Sempre que relevante, identificar quais variáveis alteram mais o resultado, por exemplo:

- distância;
- quantidade de colaboradores;
- duração da obra;
- número de módulos;
- quantidade de excedentes;
- preço unitário;
- quantidade de viagens;
- quantidade de diárias;
- produtividade.

## 7. Rastreamento

Cada memória deve poder apontar para:

`REQUISITO → ITEM DO ORÇAMENTO → DADO DE ENTRADA → FÓRMULA → RESULTADO`

Isso permite à PTS Pós verificar o raciocínio e ao ELO reutilizar a metodologia.

## 8. Aprendizado

Uma memória de cálculo só se torna conhecimento reutilizável quando o resultado é conferido ou validado.

Classificação:

- **CONFIRMADA** — cálculo conferido;
- **REFERÊNCIA** — lógica útil, mas contexto histórico;
- **ESTIMADA** — possui premissas não confirmadas;
- **PENDENTE** — depende de informação/validação;
- **OBSOLETA** — não deve ser reutilizada como parâmetro vigente.

## 9. Interface com o ELO

O Especialista fornece a memória; o ELO interpreta a aplicabilidade.

`ESPECIALISTA → MEMÓRIA DE CÁLCULO → ELO → NOVO CENÁRIO → RECÁLCULO`

A memória deve explicar o raciocínio sem depender de conhecimento tácito do autor original.
