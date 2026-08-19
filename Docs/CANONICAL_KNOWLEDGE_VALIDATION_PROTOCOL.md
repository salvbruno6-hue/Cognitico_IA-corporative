# ELO — Protocolo de Validação da Consolidação Canônica

## Objetivo
Transformar a consolidação PT/EN em uma mudança verificável antes do merge.

## 1. Identidade
Cada artefato consolidado deve possuir `artifact_id` estável e `concept_id` semanticamente coerente. O ID não pode depender do caminho físico.

## 2. Localização
Cada registro deve possuir `canonical_path`. Caminhos anteriores devem ser registrados em `legacy_paths` somente quando forem comprovadamente referências ao mesmo artefato.

## 3. Integridade
Quando a migração for apenas de localização, o conteúdo deve permanecer semanticamente equivalente. Alterações de conteúdo devem ser classificadas separadamente como `COMPLEMENTAR`, `CONFLITANTE` ou `EVOLUÇÃO`.

## 4. Proveniência
Toda migração deve preservar origem, decisão, histórico e versão. O novo caminho não pode substituir a origem histórica.

## 5. Consumidores
Pesquisar referências aos caminhos antigos e classificar cada ocorrência como:

- documental;
- executável;
- teste;
- índice;
- CI;
- histórico;
- integração externa.

Referências executáveis não podem permanecer hard-coded no caminho histórico após a migração.

## 6. SourceResolver
O `SourceResolver` existente permanece a fronteira runtime. O índice canônico fornece identidade e localização; não é criado um segundo mecanismo de resolução concorrente.

## 7. RAG / Memory / Evidence
Indexação, memória e evidência devem apontar para `artifact_id`/versão/proveniência, não usar `canonical_path` como identidade primária.

## 8. Execução paralela por núcleos virtuais

A validação pode ser particionada em núcleos virtuais para acelerar a análise de múltiplos arquivos:

```text
A estrutura/famílias
B equivalência/duplicidade
C referências/consumidores
D relações/proveniência
E testes/CI/gates
          ↓
   reconciliação central
```

Cada núcleo pode analisar vários arquivos independentes na mesma rodada. Nenhum núcleo pode promover sozinho um artefato a autoridade canônica ou executar remoção.

## 9. Testes mínimos

```text
T01: artifact_id único
T02: concept_id coerente
T03: canonical_path existe
T04: legacy_path resolve para o mesmo artifact_id
T05: conteúdo preservado quando a mudança é somente física
T06: provenance preservada
T07: nenhuma referência executável órfã
T08: SourceResolver continua sendo a autoridade runtime
T09: índices/documentação atualizados
T10: CI sem falhas introduzidas pela consolidação
```

## 10. Gate

```text
T01–T10 PASS
     ↓
MERGE CANDIDATE
```

Qualquer falha bloqueia depreciação e remoção física.

## 11. Ordem de execução

1. validar os masters já registrados;
2. registrar evidência por artefato;
3. mapear referências reais;
4. adaptar consumidores quando necessário;
5. executar testes/CI;
6. corrigir falhas;
7. repetir até gate verde;
8. somente então marcar a árvore histórica como `DEPRECATED`.

## 12. Regra de lote

Quando vários artefatos independentes forem analisados, consolidar as alterações coerentes em lote e preservar um único registro de decisão por rodada. Conflitos entre núcleos devem retornar à reconciliação central antes do commit.

## 13. Escopo protegido

Este protocolo não autoriza alterações em `src/elo/`, Cognitive Core, contratos executáveis ou runtime apenas para resolver nomenclatura documental.
