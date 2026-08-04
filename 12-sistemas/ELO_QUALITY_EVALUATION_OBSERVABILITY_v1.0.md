# ELO Quality, Evaluation & Observability v1.0

**Status:** Normativo
**Baseline:** ELO Core Architecture Baseline v1.0

## 1. Objetivo
Definir requisitos mínimos para verificar qualidade, comportamento e operação dos componentes do ELO sem acoplar a arquitetura a uma ferramenta específica.

## 2. Dimensões
### Testing
Testes unitários, de contrato, integração, isolamento de tenant, autorização, regressão, resiliência e end-to-end conforme criticidade.

### Evaluation
Avaliação de Reasoning, recuperação de conhecimento, agentes e recomendações com datasets/versionamento, critérios explícitos, métricas, thresholds e evidências reproduzíveis.

### Observability
Logs estruturados, métricas, traces e eventos correlacionados por `tenant_id`, `correlation_id` e identificadores operacionais adequados.

## 3. Regras para IA
Saídas probabilísticas não devem ser avaliadas apenas por execução sem erro. Devem existir critérios de correção, groundedness/evidência, relevância, segurança, consistência e confiança calibrada conforme caso de uso.

## 4. Quality Gates
Mudanças críticas devem possuir critérios objetivos de aceite. Falha em isolamento, autorização, provenance ou integridade é bloqueante. Regressões cognitivas relevantes exigem avaliação antes de promoção.

## 5. Observabilidade mínima
Medir latência, taxa de erro, volume, disponibilidade, uso de recursos, chamadas externas, decisões, recusas de policy, falhas de ferramentas, custo quando mensurável e qualidade de resultados quando aplicável.

## 6. Segurança de telemetria
Logs e traces obedecem classificação da informação. Segredos, credenciais e dados sensíveis não devem ser registrados sem necessidade e proteção explícitas.

## 7. Auditabilidade
Resultados de testes e avaliações relevantes devem ser versionáveis e relacionáveis a versão de código/configuração/modelo/dataset quando aplicável.

## 8. Sinais de produção
A arquitetura deve suportar SLI/SLO progressivamente. Alertas devem ser acionáveis e vinculados a runbooks conforme maturidade operacional.
