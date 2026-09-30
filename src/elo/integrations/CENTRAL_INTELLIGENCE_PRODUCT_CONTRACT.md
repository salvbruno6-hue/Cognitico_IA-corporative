# Contrato de Produto — Central de Inteligências

## Status

`NORMATIVE / PRODUCT ARCHITECTURE`

## Finalidade

A Central de Inteligências é a área da Casa do ELO onde um especialista autenticado poderá visualizar e utilizar inteligências externas autorizadas, sem abandonar o ambiente, identidade, contexto e governança do ELO.

## Conceito

```text
Casa do ELO
   │
   ├── Usuário / Especialista
   │       ↓
   │   Identidade + Permissão
   │       ↓
   ├── Central de Inteligências
   │       ↓
   │   Intelligence Router / Gateway
   │       ↓
   ├── Provider Adapter
   │       ↓
   │   IA externa
   │       ↓
   ├── Resultado
   │       ↓
   │   Provenance + Experience
   │       ↓
   └── ELO Learning Laboratory
```

## Requisitos mínimos

1. autenticação do usuário;
2. isolamento por tenant;
3. catálogo de inteligências autorizadas;
4. catálogo de providers/modelos/capacidades;
5. controle de permissões por especialista;
6. abertura/invocação através do gateway/adapters existentes;
7. registro de request/correlation id;
8. provenance da execução;
9. registro da experiência produzida;
10. aplicação das políticas de segurança e governança;
11. bloqueio de inteligências não autorizadas;
12. possibilidade futura de incluir novos providers sem alterar o Core.

## Tipos de inteligência

A arquitetura não limita a Central a modelos de texto. Ela deve permitir, por contratos, capacidades como:

- raciocínio e análise;
- geração e análise de documentos;
- imagem;
- vídeo;
- áudio;
- código;
- pesquisa;
- cálculo e simulação;
- ferramentas e plugins;
- modelos especializados;
- modelos locais ou corporativos.

A disponibilidade real de cada capacidade depende de adapter, contrato, política e integração implementados.

## Regra de experiência do usuário

O usuário pode escolher explicitamente uma inteligência quando isso for apropriado. Porém, para missões dirigidas ao ELO, a seleção pode permanecer invisível e ser feita pelo Intelligence Router.

Assim, coexistem:

- **modo ELO:** o ELO escolhe e coordena;
- **modo especialista:** o usuário escolhe uma inteligência autorizada;
- **modo híbrido:** o usuário indica uma preferência e o ELO governa contexto, evidência, execução e avaliação.

## Não objetivos

A Central não deve:

- criar um segundo Core;
- criar uma memória independente;
- armazenar segredos no frontend;
- transformar provider externo em fonte de verdade;
- permitir bypass de políticas;
- substituir o Intelligence Router como autoridade de seleção;
- criar integrações específicas diretamente na interface.

## Critérios de aceite arquitetural

Uma implementação da Central só pode avançar para produção quando demonstrar:

- isolamento de tenant;
- autorização por usuário/especialista;
- chamada através do adapter governado;
- ausência de segredo no cliente;
- provenance;
- registro de experiência;
- tratamento de falhas e bloqueios;
- testes de regressão;
- validação do Evolution Gate quando houver alteração de conhecimento ou comportamento canônico.
