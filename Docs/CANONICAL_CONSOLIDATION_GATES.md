# ELO — Gates de Consolidação Canônica

## Objetivo
Impedir que a consolidação PT/EN seja considerada concluída apenas porque os arquivos foram movidos ou copiados.

## Gate 1 — Identidade
- [ ] Todo artefato consolidável possui `artifact_id` estável.
- [ ] `concept_id` é definido quando aplicável.
- [ ] O ID não depende do caminho físico.

## Gate 2 — Autoridade
- [ ] Existe um único proprietário canônico por conceito.
- [ ] Conteúdo complementar não foi descartado.
- [ ] Conflitos estão registrados e não foram resolvidos por renomeação.

## Gate 3 — Localização
- [ ] `canonical_path` definido.
- [ ] `legacy_paths[]` registrados quando necessários.
- [ ] Nenhum consumidor novo depende de caminho histórico.

## Gate 4 — Proveniência
- [ ] Origem histórica preservada.
- [ ] Versão/hash preservados quando aplicável.
- [ ] Evidências continuam rastreáveis.

## Gate 5 — Consumidores
- [ ] SourceResolver permanece autoridade runtime.
- [ ] SourceDiscovery não perdeu capacidade de resolução.
- [ ] Knowledge Engineering identificado.
- [ ] RAG/Memory identificados.
- [ ] Agentes identificados.
- [ ] Scripts/CI/documentação pesquisados.

## Gate 6 — Integridade
- [ ] Links internos válidos.
- [ ] Referências antigas resolvem por alias quando necessário.
- [ ] Nenhuma referência órfã conhecida.
- [ ] Conteúdo canônico corresponde ao conteúdo aprovado.

## Gate 7 — Testes
- [ ] Resolução por `artifact_id`.
- [ ] Resolução por `legacy_path`.
- [ ] Integridade de proveniência.
- [ ] Regressão do SourceResolver.
- [ ] Regressão dos consumidores afetados.
- [ ] CI verde.

## Gate 8 — Depreciação
Somente após Gates 1–7:
- [ ] caminho histórico marcado como `DEPRECATED`;
- [ ] dependências remanescentes justificadas;
- [ ] janela de compatibilidade definida.

## Gate 9 — Remoção
Somente após evidência de ausência de dependências e preservação integral de conteúdo/proveniência.

## Regra de bloqueio
Qualquer falha nos Gates 1–7 bloqueia depreciação e remoção. `mergeable=false` deve ser tratado como bloqueio, não como aprovação implícita.

## Estado inicial do PR #267
A consolidação está em auditoria/migração controlada. A remoção física permanece bloqueada. O limite de revisão automática do Codex não é evidência de aprovação.
