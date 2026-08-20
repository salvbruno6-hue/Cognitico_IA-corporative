# ELO — Mapa de Impacto e Referências da Migração Canônica

## Regra
A mudança física de endereço deve ser tratada como migração de localização, nunca como criação de um novo conceito.

## Camadas afetadas

| Camada/consumidor | Dependência | Estratégia |
|---|---|---|
| Cognitive Core | identidade/resolução | não duplicar autoridade; usar resolver existente |
| Knowledge Engineering | aquisição/normalização | resolver por identidade canônica |
| Memory | proveniência/contexto | manter artifact_id e histórico |
| RAG | recuperação | indexar identidade + caminho atual + proveniência |
| Reasoning | contexto | consumir evidência resolvida |
| Evidence/Governance | rastreabilidade | registrar origem e versão |
| Agentes | consulta | nunca assumir caminho físico novo |
| Testes | contratos | validar canonical + legacy alias |
| CI | gates | bloquear remoção prematura |
| Documentação | navegação | atualizar links e índices |
| Scripts | automação | substituir caminhos hard-coded por resolução |

## Relação com o runtime existente

O repositório já possui `src/elo/core/source_resolver.py` e `source_discovery.py`. A consolidação deve integrar o índice canônico a essa fronteira, não criar um segundo resolver. O SourceResolver atual já valida tenant, domínio, principal, sessão, request, correlação, conversa e escopo de autorização antes de resolver fontes.

## Evidência transversal — 2026-08-20

Os cinco `legacy_path` atualmente registrados no `CANONICAL_KNOWLEDGE_ARTIFACT_ID_REGISTRY_2026-08-19.json` foram pesquisados no repositório. As ocorrências localizadas ficaram restritas ao próprio registro, auditorias e documentação de migração; não foi localizado consumidor operacional textual dependente dos cinco caminhos antigos.

Isso é evidência de **ausência de referência textual operacional identificada**, não autorização de remoção física.

## Sequência segura

1. atribuir identidade;
2. registrar canonical_path;
3. registrar legacy_path;
4. mapear consumidores;
5. migrar referências;
6. migrar conteúdo;
7. validar resolução;
8. validar proveniência;
9. validar CI;
10. deprecar endereço antigo;
11. remover somente após gate final.

## Critério de impacto

### Baixo
Arquivo documental isolado, sem referências externas e sem autoridade normativa.

### Médio
Documento referenciado por índices, navegação ou documentação operacional.

### Alto
Contrato, regra normativa, schema, modelo consumido, evidência, teste, agente ou componente de runtime.

### Crítico
Qualquer artefato que possa alterar identidade, autoridade, autorização, execução, memória, evidência ou interpretação do Core.

## Regra para conflito

Se duas versões afirmarem coisas diferentes sobre o mesmo conceito:

`não sobrescrever → registrar conflito → identificar autoridade → decidir por ADR/revisão → só então consolidar`.

## Estado desta etapa

- consumidores textuais dos cinco legacy paths: **nenhum identificado**;
- referências/aliases: **ainda não validados pelo runtime**;
- testes de resolução antiga/nova: **pendentes**;
- CI: **pendente**;
- depreciação: **bloqueada**;
- remoção física: **bloqueada**.
