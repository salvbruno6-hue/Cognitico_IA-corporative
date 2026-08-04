# ELO Provenance, Evidence & Audit Contract v1.0

**Status:** Normativo
**Baseline:** ELO Core Architecture Baseline v1.0

## 1. Objetivo
Estabelecer rastreabilidade transversal para dados, conhecimento, memória, raciocínio, recomendações, decisões, agentes e integrações.

## 2. Separação conceitual
- **Provenance:** origem e cadeia de transformações/uso.
- **Evidence:** elemento verificável usado para sustentar inferência ou decisão.
- **AuditEvent:** fato de auditoria sobre acesso, mudança, decisão ou execução.

Nenhum desses conceitos substitui os demais.

## 3. ProvenanceRecord
Campos conceituais mínimos: `provenance_id`, `tenant_id`, `domain`, `subject_type`, `subject_id`, `source_type`, `source_id`, `operation`, `actor_principal_id`, `parent_provenance_ids`, `created_at`, `correlation_id` e metadados de integridade quando aplicáveis.

## 4. EvidenceRecord
Deve referenciar origem, conteúdo ou localização verificável, classificação, timestamp, provenance e contexto de utilização. Evidência derivada deve preservar ligação com evidências/fontes antecedentes.

## 5. AuditEvent
Eventos mínimos incluem autenticação relevante, autorização/negação, acesso sensível, alteração de política, ingestão, transformação, criação/uso de memória, execução de agente, decisão, aprovação, integração externa e incidente.

## 6. Invariantes
- Registros de auditoria não podem ser silenciosamente sobrescritos.
- Toda cadeia deve preservar `tenant_id`.
- Cross-tenant provenance é proibida salvo mecanismo administrativo explicitamente governado.
- Identificadores de correlação devem permitir reconstrução ponta a ponta.
- Dados sensíveis não devem ser replicados integralmente em logs apenas para auditoria.

## 7. Integridade e retenção
Retenção segue classificação, política e requisitos legais. Mecanismos de hash, assinatura, WORM ou equivalentes podem ser aplicados conforme criticidade, sem tornar tecnologia específica parte do domínio.

## 8. Relação com componentes
Context, Knowledge, Memory, Reasoning, Decision e Agent devem emitir ou referenciar provenance/audit conforme a operação. Provenance é transversal e não um estágio final do pipeline.

## 9. Consultabilidade
A plataforma deve permitir responder: qual fonte sustentou este resultado; quais transformações ocorreram; qual principal executou a ação; qual política foi aplicada; quais evidências sustentaram a decisão; qual outcome decorreu dela.
