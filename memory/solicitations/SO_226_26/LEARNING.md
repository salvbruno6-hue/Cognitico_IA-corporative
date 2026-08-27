# SO 226.26 — Aprendizado Estruturado

## Escopo

Aprendizado contextual derivado da análise da documentação da SO 226.26 — ZONA OESTE MAIS, a partir do arquivo `SO-001.25-ZONA_OESTE-001-REV00-ARQ.M.pdf`.

## 1. Identidade

- Solicitação canônica: `SO 226.26`
- Cliente: `ZONA OESTE MAIS`
- Tipo documental analisado: layout arquitetônico/modular.
- Fonte principal: `SO-001.25-ZONA_OESTE-001-REV00-ARQ.M.pdf`
- Emissão inicial indicada no documento: 09/01/2026.

## 2. Características do módulo

- Dimensões externas: `6000 x 2440 x 3010 mm (C x L x A)`.
- Dimensões internas: `5872 x 2322 x 2583 mm (C x L x A)`.
- Área interna indicada: `13,63 m²`.
- Carga máxima indicada: `150 kgf/m²`.
- Alimentação elétrica indicada: `2Ø - 220 V`.

## 3. Instalações e pontos representados

O documento apresenta referências de:

- alimentação de água fria;
- descarte de esgoto;
- entrada elétrica;
- luminárias de sobrepor 36 W;
- luminárias de sobrepor 18 W;
- tomadas baixa a 300 mm do piso;
- tomadas a meia altura a 1200 mm do piso;
- tomadas altas a 2000 mm do piso;
- interruptor de uma seção;
- interruptor paralelo/three-way;
- quadro geral de luz e força aparente;
- ponto TIC à 250 mm do piso, RJ45 duplo com tubulação aparente;
- cabo PP embutido;
- exaustor elétrico;
- luminária LED de emergência.

## 4. Cargas representadas

O layout contém referências textuais de `5500 W 220 V` associadas aos pontos/equipamentos representados.

### Regra aprendida

Quando uma carga nominal estiver explicitamente indicada no layout, utilizar esse dado como evidência de projeto para dimensionamento e comparação com a capacidade da alimentação. Não substituir a carga indicada por um valor genérico sem justificativa.

## 5. Leitura de cotas e elementos gráficos

O documento evidencia que cotas podem ser complementadas por vistas A/B e pela própria planta baixa. A interpretação deve considerar a combinação de planta, vistas e legenda, evitando atribuir automaticamente uma cota de uma vista a outro elemento sem confirmar sua posição gráfica.

### Regra reutilizável

Para esquadrias, portas e painéis, confirmar sempre:

`planta baixa + vista correspondente + posição do elemento + cota associada`.

Não inferir que toda cota próxima ao elemento corresponde ao vão, folha ou painel sem verificar a representação.

## 6. RJ45 e infraestrutura aparente

O padrão documental analisado explicita `RJ45 Duplo` e `Tubulação Aparente`.

### Regra reutilizável

Quando o layout indicar RJ45 duplo com tubulação aparente, tratar como infraestrutura passiva de dados, mantendo separado de equipamentos ativos de rede. Não assumir modem, roteador, switch ou internet como fornecimento sem atribuição específica.

## 7. Água, esgoto e exaustão

O desenho apresenta graficamente pontos de alimentação de água fria, descarte de esgoto e exaustor elétrico.

### Regra reutilizável

Quando o layout apenas indicar pontos de interface, o orçamento deve separar:

1. ponto/infraestrutura interna;
2. interligação externa, quando aplicável;
3. equipamento, somente se expressamente fornecido.

## 8. Evidência x interpretação

### FATO
- Dimensões do módulo e área interna conforme desenho.
- Alimentação elétrica 2Ø - 220 V.
- Pontos e alturas elétricas descritos na legenda.
- RJ45 duplo com tubulação aparente.
- Água fria, esgoto e exaustor elétrico representados.
- Cargas textuais de 5500 W / 220 V presentes no layout.

### REGRA_APRENDIDA
- Confirmar cotas de esquadrias/aberturas entre planta e vistas antes de precificar.
- Separar infraestrutura passiva de equipamentos ativos.
- Utilizar cargas explicitamente indicadas como evidência de dimensionamento.

## 9. Controle de evidência

Este aprendizado é contextual à SO 226.26 e não deve ser promovido automaticamente ao Core do ELO. A promoção de qualquer padrão permanente deve seguir evidência, generalização, testes e Evolution Gate, conforme governança do repositório.
