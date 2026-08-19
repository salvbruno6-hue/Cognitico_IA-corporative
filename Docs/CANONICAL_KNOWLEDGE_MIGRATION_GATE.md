# ELO — Gate de Migração Canônica

## Objetivo
Impedir que a consolidação PT/EN avance para exclusão física enquanto identidade, conteúdo, referências e testes não estiverem comprovados.

## Gates

- [x] ADR aprovado para consolidação controlada
- [x] mapa de propriedade canônica existente
- [x] ponto primário de modificação definido
- [x] índice/registro de migração inicial criado
- [x] auditoria arquivo-a-arquivo iniciada
- [x] mapa de impactos definido
- [ ] 100% das famílias auditadas
- [ ] 100% dos arquivos classificados
- [ ] artifact_id atribuído aos artefatos migráveis
- [ ] referências físicas catalogadas
- [ ] aliases registrados
- [ ] migração dos conteúdos aprovados
- [ ] testes de resolução canônica
- [ ] testes de alias legado
- [ ] testes de proveniência
- [ ] CI verde após lote
- [ ] caminhos históricos marcados DEPRECATED/SUPERSEDED
- [ ] remoção física autorizada

## Condição de bloqueio
Qualquer falha em identidade, conteúdo exclusivo, referência, proveniência ou teste interrompe a remoção física.

## Regra de merge
Merge só é considerado seguro quando os gates aplicáveis estiverem satisfeitos. Aprovação humana ou automação não substitui evidência técnica.

## Estado atual
`MIGRATION_AUDIT_IN_PROGRESS`

A etapa atual ainda não está autorizada a remover árvores históricas.
