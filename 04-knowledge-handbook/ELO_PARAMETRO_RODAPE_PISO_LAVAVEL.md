# ELO — PARÂMETRO DE RODAPÉ SANITÁRIO/LAVÁVEL

**Camada:** `04-knowledge-handbook`  
**Função:** registrar como parâmetro de referência a composição de rodapé lavável/sanitário utilizado em análises de orçamento, preservando método, unidade, premissas e necessidade de validação de preço.

## 1. Parâmetro de referência

Solução de referência: **rodapé sanitário lavável em PVC, tipo meia-cana, instalado**.

Parâmetro preliminar adotado na análise: **R$ 45,00/m instalado**.

### Composição conceitual

O parâmetro deve considerar, conforme aplicabilidade:

- rodapé/perfil sanitário lavável;
- peças de acabamento e cantos;
- emendas;
- adesivo/cola e consumíveis;
- corte e ajustes;
- instalação;
- acabamento e vedação necessários.

O valor de R$ 45,00/m é uma **referência preliminar de orçamento**, não um preço universal nem uma composição validada por fornecedor específica para toda SO.

## 2. Memória de cálculo

### Fórmula básica

```text
QUANTIDADE DE RODAPÉ (m)
= COMPRIMENTO TOTAL DAS PAREDES A RECEBER RODAPÉ
- TRECHOS SEM RODAPÉ
+ ABATIMENTOS/COMPLEMENTOS CONFORME LAYOUT
```

Quando aplicável, acrescentar perdas de corte e ajustes:

```text
QUANTIDADE COM PERDA
= QUANTIDADE BASE × (1 + % DE PERDA)
```

Custo:

```text
CUSTO DO RODAPÉ
= QUANTIDADE (m) × R$ 45,00/m
```

## 3. Método de levantamento

Para ambientes retangulares sem interferências:

```text
PERÍMETRO = 2 × (COMPRIMENTO + LARGURA)
```

Depois retirar portas, passagens ou outros trechos que não receberão rodapé.

Para múltiplos ambientes:

```text
RODAPÉ TOTAL = Σ (PERÍMETRO DE CADA AMBIENTE - TRECHOS NÃO REVESTIDOS)
```

Não utilizar a área do piso para calcular diretamente o rodapé. O rodapé é uma grandeza **linear (m)** e deve ser derivado do perímetro/trechos de parede efetivamente aplicáveis.

## 4. Exemplo de desenvolvimento

Ambiente de 6,00 m × 4,00 m:

```text
Perímetro = 2 × (6 + 4)
Perímetro = 20,00 m
```

Considerando uma porta de 0,90 m sem rodapé:

```text
Quantidade líquida = 20,00 - 0,90
Quantidade líquida = 19,10 m
```

Sem perda:

```text
Custo = 19,10 × R$ 45,00
Custo = R$ 859,50
```

Se for adotada perda de 5%:

```text
Quantidade de compra = 19,10 × 1,05
Quantidade de compra = 20,055 m
```

O orçamento deve então decidir se compra por metro inteiro, barra ou rolo conforme a forma de fornecimento.

## 5. Variáveis críticas

O parâmetro é sensível a:

- tipo de rodapé;
- altura do perfil;
- raio/meia-cana;
- material;
- padrão sanitário;
- quantidade de cantos;
- quantidade de emendas;
- comprimento das barras/rolos;
- perdas;
- estado e regularidade das paredes;
- necessidade de preparação da superfície;
- mão de obra;
- distância/logística;
- fornecedor e região.

## 6. Cuidados técnicos

O termo “rodapé lavável” não define sozinho a solução. Em ambientes sanitários, hospitalares ou de limpeza frequente, verificar no TR/layout se há exigência de:

- meia-cana/canto abaulado;
- continuidade piso-parede;
- material específico;
- solda térmica;
- compatibilidade com o revestimento do piso;
- vedação;
- cantos internos/externos.

Quando o documento exigir uma solução específica, o parâmetro genérico de R$ 45,00/m **não deve ser aplicado automaticamente**.

## 7. Distinção entre parâmetro e memória confirmada

### PARÂMETRO DE REFERÊNCIA

R$ 45,00/m instalado.

Classificação atual: **REFERÊNCIA**.

### NÃO CONFIRMADO

A análise atual não contém uma cotação formal de fornecedor, composição SINAPI/TCPO ou memória de custo detalhada que valide o R$ 45,00/m.

Portanto, o ELO deve tratá-lo como referência preliminar até que exista fonte de preço específica.

## 8. Regra de reutilização

Ao encontrar outro orçamento com rodapé lavável/sanitário:

```text
IDENTIFICAR SOLUÇÃO
↓
VERIFICAR ESPECIFICAÇÃO DO TR
↓
LEVANTAR METRAGEM LINEAR
↓
VERIFICAR CANTOS/EMENDAS/PERDAS
↓
COMPARAR CONTEXTO
↓
APLICAR OU NÃO O PARÂMETRO R$ 45,00/m
↓
RECALCULAR
↓
VALIDAR
```

Nunca copiar o valor final de uma SO sem verificar contexto.

## 9. Aprendizado associado

Regra aprendida:

> Rodapé lavável/sanitário deve ser orçado por **metro linear**, derivado do perímetro dos ambientes e ajustado por trechos sem rodapé, cantos, emendas e perdas. O valor unitário deve ser tratado como dependente do tipo de solução e do mercado local.

## 10. Integração com PTS

Na PTS Técnica:

`TR/layout → exigência de rodapé → solução técnica → metragem`

Na PTS Pós-Orçamento:

`metragem prevista → metragem orçada → R$/m → valor total → conferência`

Na memória de cálculo:

`entrada → premissa → fórmula → cálculo → resultado → validação`.
