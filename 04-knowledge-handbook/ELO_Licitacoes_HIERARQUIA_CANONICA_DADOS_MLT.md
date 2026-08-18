# ELO — Hierarquia Canônica de Dados MLT

## Objetivo
Impedir que o GPT misture padrões gerais, fichas específicas, composições e regras de negócio.

## Ordem de precedência
1. **Ficha técnica específica do modelo** — prevalece para atributos daquele modelo.
2. **Composição do modelo** — prevalece para quantitativos, materiais e itens de orçamento daquela composição.
3. **Regra corporativa de produto/orçamento** — prevalece para classificação de padrão, excedente e regra de negócio.
4. **Catálogo construtivo geral MLT** — usado somente para atributos gerais não sobrescritos.
5. **Informação externa ou inferência** — não utilizar como fato interno sem validação.

## Regras canônicas já normalizadas

### Dimensões e áreas
- Área nominal externa de um módulo 20 pés de 6000 × 2440 mm: **14,64 m²**.
- Área útil oficial de referência para módulo 20 pés: **13,62 m²**.
- Portanto, **14,64 m² nunca deve ser descrito como área útil interna**.
- Altura de 3010 mm é uma dimensão de referência da família.
- MLT.M01 possui altura externa específica de **2985 mm** e esta prevalece para o M01.

### Isolamento
- Paredes: **PIR 40 mm** como padrão cadastrado.
- Forro: **PIR 32 mm**.
- PIR 50 mm: somente mediante análise técnica específica.

### Estrutura e pintura
- Estrutura principal: galvanizada.
- Não aplicar Shop Primer como revestimento geral sobre galvanização íntegra.
- Regiões de solda/corte/arestas com perda da proteção devem receber tratamento de recuperação apropriado.
- PU W-Thane PDA 514 é acabamento quando previsto no sistema do modelo/composição.

### Elétrica
- O padrão geral da família é referência **127/220 V – 60 Hz – 2F + N + T**, quando aplicável.
- MLT.M01 possui configuração específica de **220 V monofásico**; esta informação prevalece para M01.
- DR/DPS não são padrão do MLT.M01.
- DR/DPS estão associados aos módulos sanitários/áreas molhadas conforme configuração/projeto aplicável.

### Climatização
- Abertura 410 × 690 mm significa infraestrutura para equipamento de janela.
- A existência da abertura não significa que o equipamento de ar-condicionado esteja incluído no produto padrão.
- Split é tratado como excedente conforme regra de orçamento.

### Piso
- Painel Wall 30 mm: sistema estrutural cadastrado para os módulos aplicáveis.
- Piso cimentício 20 mm: alternativa conforme modelo/projeto.
- LVT 2 mm: acabamento quando previsto.

## Regra de resposta
Se uma pergunta envolver dois valores diferentes, o GPT deve explicar a diferença por categoria ou precedência. Não escolher um valor apenas porque parece mais provável.

Se não houver fonte suficiente para decidir, responder **"Informação não definida na base técnica atual"** e direcionar ao **Setor de Planejamento**.
