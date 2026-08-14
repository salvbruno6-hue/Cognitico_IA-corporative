# ELO Core — Maturity Baseline

## Purpose

Estabelecer o que já é suficientemente estável para servir como base durante a fase de experimentação comportamental, sem congelar capacidades ainda imaturas.

## Baseline congelável agora

### 1. Source Discovery
Responsabilidade: transformar pergunta e contexto temporal em um plano de busca orientado por fontes, sem exigir caminhos do usuário.

Critério: o planejador pode sugerir ELO_MEMORY, CHATGPT_PROJECTS, GITHUB, DOCUMENTS, WEB e AI_PROVIDER conforme intenção. A execução da busca continua pertencendo a adapters autorizados.

Status: BASE SUFICIENTE.

### 2. Context Resolution
Responsabilidade: resolver entidade, escopo, fontes e evidências antes do handoff especializado.

Critério: respeitar escopo; não promover evidência a conhecimento; não habilitar especialista sem descoberta e evidência suficiente.

Status: BASE SUFICIENTE, com evolução pendente em scoped evidence obrigatório para diagnósticos locais.

### 3. GPT Decision Handoff
Responsabilidade: usar GPT como especialista, nunca como autoridade canônica ou decisor final.

Critério: handoff exige discovery; SPECIALIST_VALIDATION exige evidência contextualizada; retorno deve ser tratado como evidência externa/temporal.

Status: BASE SUFICIENTE.

### 4. Maturity Engine
Responsabilidade: decidir se o ELO está em DISCOVERY_ASSIST ou SPECIALIST_VALIDATION.

Critério: dimensões explícitas e limiar configurável; falta de maturidade impede modo especialista.

Status: BASE SUFICIENTE.

### 5. Diagnostic Scenario Engine
Responsabilidade: observar o mesmo problema por múltiplas lentes e comparar hipóteses sem transformar hipótese em fato.

Critério: cada cenário carrega evidências, incertezas, dependências e conflitos; comparação identifica evidência compartilhada e necessidade de decisão humana.

Status: BASE SUFICIENTE COMO CAPACIDADE EXPERIMENTAL; não congelar como diagnóstico causal completo.

## Não congelar ainda

- ProductionFlow como domínio definitivo;
- resolução física de adapters externos;
- enforcement completo de tenant/unidade em evidência;
- memória de evolução como armazenamento permanente;
- causal_reasoning como motor causal definitivo;
- decisão autônoma sem validação humana;
- qualquer nova camada que duplique contratos existentes.

## Regra de congelamento

Uma capacidade só passa de experimental para baseline quando possuir:

1. contrato explícito;
2. testes comportamentais;
3. teste de erro/insuficiência;
4. teste de conflito quando aplicável;
5. evidência de integração com contratos canônicos;
6. nenhuma violação conhecida de governança;
7. documentação do limite da capacidade.

Congelar significa preservar o contrato e os invariantes. Não significa impedir evolução futura. Qualquer alteração posterior deve ser comparada com o baseline e classificada como compatível, adaptação ou mudança arquitetural.

## Ciclo de maturidade

hipótese → implementação experimental → cenário normal → cenário ambíguo → cenário adversarial → integração → evidência → avaliação → baseline ou evolução.
