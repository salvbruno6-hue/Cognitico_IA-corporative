# ELO APRENDER — Regra de Três Composta para Dimensionamento por Precedentes

## Classificação
- Domínio: ORÇAMENTO
- Tipo: REGRA REUTILIZÁVEL / PRECEDENTE METODOLÓGICO
- Origem: aplicação prática na SO 155.26 e análise de manutenção corretiva
- Destino: conhecimento cognitivo consolidado no Git
- Supabase: não aplicável a esta regra genérica

## Regra aprendida
Quando uma nova SO possuir escala diferente de uma SO anterior e houver múltiplas variáveis que influenciam o dimensionamento, o ELO deve avaliar a aplicação de **regra de três composta** antes de copiar quantitativos do precedente.

Considerar, conforme aplicável: quantidade de equipamentos/módulos/unidades; período contratual; frequência/periodicidade; produtividade; composição da equipe; duração do atendimento; logística por atendimento; veículo de apoio e demais recursos associados.

## Fluxo operacional
```text
PRECEDENTE
↓
IDENTIFICAR VARIÁVEIS DIMENSIONADORAS
↓
COMPARAR PRECEDENTE × NOVO CENÁRIO
↓
APLICAR REGRA DE TRÊS COMPOSTA
↓
OBTER QUANTITATIVO PROPORCIONAL
↓
ARREDONDAR PARA QUANTIDADE EXECUTÁVEL, QUANDO NECESSÁRIO
↓
VALIDAR CONTRA TR, SLA, HISTÓRICO E CARACTERÍSTICAS DO NOVO OBJETO
↓
DEFINIR PREMISSA ORÇAMENTÁRIA
```

## Exemplo derivado da SO 155.26
Precedente: 6 equipamentos/escopo corretivo, 6 meses e 6 visitas.
Novo cenário: 3 equipamentos e 3 meses.

```text
X = 6 × (3/6) × (3/6)
X = 1,5 atendimento
```

Como atendimento não é fracionável, o resultado matemático deve ser convertido em quantidade executável e validado. No exemplo, **2 atendimentos no período** é a hipótese proporcional ao precedente.

## Não automatização cega
A regra de três composta não determina sozinha o quantitativo final. O ELO deve verificar se o TR exige frequência mínima, SLA, disponibilidade mensal, histórico de falhas ou outro requisito que altere o resultado matemático.

Exemplo:
```text
Resultado proporcional = 1,5 → aproximadamente 2 atendimentos
SE TR exigir 1 atendimento/mês → 3 atendimentos no contrato
SE não houver frequência mínima e o precedente for equivalente → 2 atendimentos podem ser adotados como premissa
```

## Manutenção corretiva
O ELO não deve interpretar automaticamente que número de equipamentos = número de visitas por mês. Deve estimar a média de atendimentos considerando precedente, quantidade, período e demais variáveis relevantes.

Quando houver veículo de apoio por atendimento:
```text
atendimentos × 1 carro/atendimento = utilizações do veículo
```

## Precedente não é cópia
```text
PRECEDENTE ≠ CÓPIA
PRECEDENTE = BASE PARA RECÁLCULO
```

O ELO deve reconstruir o cálculo, verificar equivalência e substituir as variáveis do cenário anterior pelas variáveis da nova SO.

## Critério reutilizável
Em futuras SOs, perguntar: quais variáveis determinaram o quantitativo anterior; quais mudaram; se a relação é proporcional, inversamente proporcional ou composta; se a produtividade permanece equivalente; se a equipe permanece equivalente; se a logística acompanha o novo quantitativo; se há requisito contratual que altere o resultado; e se o resultado é coerente com TR e realidade operacional.

## Regra de persistência
Esta regra é conhecimento cognitivo reutilizável e deve ser recuperada pelo ELO em futuras análises. Quando houver cálculo específico de uma nova SO, a memória quantitativa correspondente deve seguir o fluxo existente de persistência no Supabase.
