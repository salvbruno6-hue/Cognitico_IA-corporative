# ELO — Matriz de Relações entre Domínios

| Origem | Relação | Destino | Exemplo de leitura |
|---|---|---|---|
| COMERCIAL | gera/condiciona | ORÇAMENTO | condição comercial impacta margem |
| LICITAÇÕES | exige | ORÇAMENTO | requisito do edital precisa de cobertura |
| LICITAÇÕES | restringe | COMERCIAL | obrigação contratual limita proposta |
| ORÇAMENTO | especifica impacto em | PROJETOS | adaptação gera custo técnico |
| PROJETOS | determina | PRODUÇÃO | solução técnica define execução |
| ORÇAMENTO | demanda | COMPRAS | item orçado exige aquisição |
| COMPRAS | restringe | PRODUÇÃO | lead time cria restrição |
| PCP | programa | PRODUÇÃO | capacidade e sequência |
| PRODUÇÃO | condiciona | LOGÍSTICA | conclusão libera expedição |
| LOGÍSTICA | realiza | ENTREGA/RESULTADO | mobilização e entrega |
| RESULTADO | retroalimenta | ORÇAMENTO | desvio de custo atualiza análise |
| RESULTADO | retroalimenta | PROJETO | falha recorrente gera revisão |
| RESULTADO | retroalimenta | COMERCIAL | desempenho influencia decisão futura |

## Invariante

A relação conecta domínios, mas não elimina a origem do dado. Toda leitura cross-domain deve preservar `source_domain`, `target_domain`, `provenance`, `validity` e `tenant_id`.

## Regra de uso

Esta matriz é uma referência de governança. Ela não autoriza por si só uma implementação de persistência ou um novo engine. A implementação deve reutilizar os contratos canônicos do ELO e passar pelos gates existentes.
