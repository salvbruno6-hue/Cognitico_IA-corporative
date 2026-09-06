# ELO APRENDER — REGRA DEFINITIVA DE MEMÓRIA POR SO

**Status:** REGRA OFICIAL DE GOVERNANÇA

## 1. Regra absoluta

Sempre que o usuário acionar o gatilho **`ELO APRENDER`** no contexto de uma Solicitação de Orçamento, o ELO deve interpretar o comando como:

> **APRENDER E ARMAZENAR OS DADOS DO ORÇAMENTO DA SO PROCESSADA.**

O aprendizado de uma SO **NUNCA estará completo** se somente regras, diretrizes ou conceitos forem armazenados.

O mesmo acionamento deve obrigatoriamente procurar e persistir também a **memória quantitativa e de cálculo específica daquela SO**.

## 2. Dupla persistência obrigatória

Cada acionamento deve processar simultaneamente:

### Camada 1 — Conhecimento

Persistir no Git: regras, diretrizes, decisões, precedentes, padrões, critérios, aprendizados de governança e melhorias identificadas.

### Camada 2 — Memória do orçamento

Persistir na camada de memória de cálculo/Supabase: SO, cliente, objeto, modalidade, produtos/modelos, quantitativos, dimensões, áreas, unidades, parâmetros, premissas, fórmulas, subcálculos, resultados, composições, valores unitários, custos, mão de obra, produtividade, logística, transporte, hospedagem, alimentação, manutenção, excedentes, customizações, interligações, projetos, percentuais, BDI, taxas, exclusões, decisões do orçamento, referências históricas efetivamente utilizadas, evidências e fontes.

## 3. O que significa “armazenar os dados de cada orçamento”

O ELO deve preservar o **raciocínio de formação do orçamento**, não apenas o preço final.

Para cada item relevante, buscar:

`SO → FONTE → REQUISITO → DADO → PARÂMETRO → PREMISSA → FÓRMULA → SUBCÁLCULO → QUANTITATIVO → COMPOSIÇÃO → CUSTO → VALIDAÇÃO`

Exemplo: não registrar somente `Rede lógica = R$ 12.000,00`. Registrar também, quando disponível, o contexto, dimensões, quantidade de pontos, distribuição, rack e acessórios, infraestrutura passiva, certificação, exclusões, premissas, fonte do quantitativo, composição e validação.

## 4. Memória por SO e memória reutilizável

Cada SO deve possuir seus próprios registros de aplicação.

Quando uma lógica já existir em memória corporativa:

`MEMÓRIA CORPORATIVA → RECUPERAR → ASSOCIAR À NOVA SO → REGISTRAR NOVAS ENTRADAS → RECALCULAR → VALIDAR`

Não copiar automaticamente o resultado histórico. O que deve ser reutilizado prioritariamente é a **lógica de cálculo**.

## 5. Cálculos ocultos

O ELO deve investigar também cálculos implícitos utilizados para formar o orçamento, como quantidade de módulos, ambientes, áreas, pontos de dados, visitas de manutenção, equipe × dias, produtividade, distância × custo, percentual × base, quantidade × preço unitário e excedentes sobre o padrão.

Se não houver informação suficiente para reconstruir o cálculo, registrar como **NÃO RECONSTRUÍVEL**, sem inventar a fórmula.

## 6. Classificação obrigatória

Cada memória deve indicar: `CONFIRMADO`, `PREMISSA`, `EXPERIÊNCIA`, `HIPÓTESE` ou `NÃO_RECONSTRUÍVEL`.

## 7. Identificadores

O ID persistente deve ser gerado/controlado pelo banco. O modelo não deve fabricar IDs para simular persistência.

A memória deve manter vínculo entre:

`SO → ID MEMÓRIA → CÁLCULOS → EVIDÊNCIAS`

## 8. Resultado obrigatório do gatilho

Ao finalizar `ELO APRENDER`, retornar sempre:

### CONHECIMENTO — GIT

O que foi aprendido como regra, diretriz, decisão ou precedente.

### MEMÓRIA DO ORÇAMENTO — SUPABASE

Os dados/cálculos da SO que foram criados, recuperados, agregados ou que não puderam ser reconstruídos.

### STATUS

Informar explicitamente: `PERSISTIDA`, `RECUPERADA`, `AGREGADA`, `PENDENTE_VALIDACAO`, `PENDENTE_PERSISTENCIA` ou `NÃO_RECONSTRUÍVEL`.

## 9. Regra contra falso aprendizado

É proibido responder **“ELO APRENDER concluído”** quando somente o conhecimento textual tiver sido salvo.

Se a memória quantitativa não tiver sido persistida, o retorno deve declarar a pendência.

## 10. Regra de governança

> **TODO `ELO APRENDER` DE UMA SO = CONHECIMENTO + DADOS DO ORÇAMENTO + MEMÓRIA DE CÁLCULO + EVIDÊNCIAS + STATUS DE PERSISTÊNCIA.**

O ELO deve cobrar esse comportamento do Especialista de Orçamento e não aceitar aprendizado incompleto.
