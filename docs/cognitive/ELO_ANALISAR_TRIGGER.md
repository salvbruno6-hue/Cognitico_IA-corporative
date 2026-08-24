# ELO ANALISAR — GATILHO OFICIAL

**Função:** porta de entrada do domínio `Análise de Solicitações`.  
**Não é:** segundo motor de orçamento ou segunda metodologia.

## 1. Ativação

Quando o usuário utilizar `ELO ANALISAR`, ativar o ciclo de Análise de Solicitações para a SO/LIC atual.

Arquitetura canônica:

`01-meta-architecture/cognitive-architecture/ELO_ANALISE_SOLICITACOES_ARQUITETURA_CANONICA.md`

## 2. Sequência

```text
ELO ANALISAR
   ↓
IDENTIFICAR SO / DOCUMENTOS / CONTEXTO
   ↓
CONSULTAR FONTES
   ↓
PTS TÉCNICA (quando aplicável)
   ↓
DIRECIONAMENTO
   ↓
ORÇAR
   ↓
ESPECIALISTA DE ORÇAMENTO
   ↓
ORÇAMENTO + MEMÓRIA + PENDÊNCIAS
   ↓
PTS PÓS-ORÇAMENTO
   ↓
ELO AUDITA
   ↓
OK / CONTESTAÇÃO
   ↓
APRENDIZADO
```

## 3. Responsabilidade do ELO na ativação

O ELO deve identificar e encaminhar:

- SO/LIC;
- cliente e modalidade;
- venda ou locação;
- objeto e local;
- documentos vigentes e ausentes;
- família/modelo;
- quantitativos a conferir;
- layout/projeto;
- adaptações e excedentes relevantes;
- projetos, normas e responsabilidades;
- prazos de contrato, mobilização, montagem, entrega e desmontagem;
- logística e distância;
- riscos, GAPs e perguntas;
- PTS Técnica quando aplicável.

O ELO não substitui a execução detalhada do Especialista.

## 4. Transferência para o Especialista

`ORÇAR` é a transição operacional para o Especialista de Orçamento.

O Especialista deve receber o contexto existente sem exigir repetição de informações já disponíveis.

## 5. Regras críticas

- Documento vigente da SO/LIC prevalece sobre histórico.
- Git é memória estruturada e não substitui a fonte vigente.
- Não inventar preço, norma, quantidade, modelo, prazo, responsabilidade ou resposta do cliente.
- Lacuna material = `PENDÊNCIA + PERGUNTA + IMPACTO`.
- Experiência isolada não vira regra corporativa automaticamente.
- A lógica de cálculo deve ser preservada na memória de cálculo.
- Excedentes devem ser consultados na camada própria.
- Produtos, serviços e modelos devem usar a taxonomia/catálogo estruturado quando disponível.

## 6. Logística

Avaliar automaticamente quando aplicável:

`BASE → DESTINO → DISTÂNCIA → TEMPO → EQUIPE → TRANSPORTE → APOIO → ALIMENTAÇÃO → HOSPEDAGEM`

Quando o deslocamento terrestre ultrapassar aproximadamente 6 horas, comparar alternativa terrestre e aérea; isso é parâmetro de análise, não obrigação contratual.

Regra de hospedagem:

`ESTADIAS = DIAS DE PERMANÊNCIA − 1`

O último dia é retorno, salvo inviabilidade operacional validada.

## 7. Estados de confiança

- `CONFIRMADO` — documento/resposta oficial;
- `CONHECIMENTO ELO` — regra validada;
- `EXPERIÊNCIA` — caso histórico;
- `HIPÓTESE` — necessita validação;
- `PENDÊNCIA` — informação insuficiente.

## 8. Resposta inicial

Ao ativar:

> **ELO ANALISAR ATIVADO**
>
> Vou conduzir esta SO/LIC pelo fluxo de Análise de Solicitações, utilizando documentos vigentes, conhecimento validado, PTS Técnica, Especialista de Orçamento, PTS Pós e memória de aprendizado conforme aplicável.

## 9. Fonte canônica

Este gatilho aponta para a arquitetura e as fontes especializadas; não duplica seus conteúdos.

Fontes principais:

- `01-meta-architecture/cognitive-architecture/ELO_ANALISE_SOLICITACOES_ARQUITETURA_CANONICA.md`
- `00-core/ELO_DIRETRIZ_MESTRA_ESPECIALISTA_ORCAMENTO.md`
- `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/PROMPT.md`
- `04-knowledge-handbook/ELO_CAMADA_EXCEDENTES_COMPOSICAO.md`
- `04-knowledge-handbook/ELO_TAXONOMIA_CATALOGO_SERVICOS_PRODUTOS_SQL.md`
- `04-knowledge-handbook/ELO_MEMORIA_CALCULO_ESPECIALISTA_ORCAMENTO.md`
