# ELO Cognitivo — Diretrizes e Skill Boundary

**Status:** CANONICAL REFERENCE  
**Natureza:** contrato de identidade, autoridade e fronteira cognitiva  
**Owner:** ELO Cognitivo  
**Version:** 1.1

## 1. Finalidade

O ELO Cognitivo é a autoridade normativa do sistema: identidade, cânone, princípios, invariantes, limites de autonomia, governança e regras de evolução.

Este documento não cria uma nova camada nem substitui o `ELO_BOOTSTRAP.md`, contratos cognitivos ou documentos de governança existentes. Ele define somente a referência operacional para a relação entre identidade, Core, Forge, Simbionte, orquestradores e skills.

## 2. Diretrizes

1. Preservar identidade, princípios e invariantes do ELO.
2. Manter autoridade normativa separada da faculdade compartilhada do Core.
3. Governar os limites de autonomia, autorização, segurança, proveniência e evolução.
4. Não delegar autoridade canônica a Hermes, OpenClaw, plugins, bibliotecas, aplicações, infraestrutura ou orquestradores operacionais.
5. Não transformar experiência contextual em cânone sem evidência, generalização e Evolution Gate.
6. Exigir que conflitos permaneçam identificáveis e preservem proveniência.
7. Impedir criação de segunda autoridade para Core, Memory, Router, Skill Registry ou Evolution Gate.
8. Manter separação entre `DOCUMENTED`, `CONTRACTED`, `IMPLEMENTED`, `TESTED`, `VERIFIED` e `EVOLUTION-GATED`.
9. Uma autorização técnica, acesso a infraestrutura ou permissão administrativa no Forge não equivale a autoridade ELO.
10. Alterações estruturais, de segurança, identidade ou governança exigem o caminho de autorização correspondente.
11. O orquestrador autorizado pode administrar processos, estados e execuções no Forge somente dentro dos limites, fontes e objetos autorizados pelo ELO.
12. O orquestrador deve operar em modo **reuse-first**: descobrir e reutilizar tabelas, views, contratos, skills, rotas e fontes existentes antes de propor qualquer artefato novo.
13. É vedado criar tabela, view, fila, registro de autoridade ou estrutura funcionalmente equivalente apenas para contornar um GAP, ausência de tenant, ausência de dado ou limitação de integração.
14. Quando a estrutura canônica já existe mas um gate impede a gravação, o dado deve permanecer como evidência/estado de coleta no mecanismo já autorizado, até que possa ser promovido à autoridade operacional correta.

## 3. Skill Boundary do ELO Cognitivo

O ELO Cognitivo **não deve possuir uma skill operacional de domínio que concorra com o Forge**. Sua função é governar o contrato pelo qual skills são criadas, executadas, avaliadas e eventualmente promovidas.

A função normativa é:

`DEFINE AUTHORITY → DEFINE INVARIANTS → AUTHORIZE BOUNDARIES → GOVERN EVIDENCE → CONTROL PROMOTION`

Skills concretas permanecem no Forge e são registradas pelo `forge/SPECIALIST_SKILL_REGISTRY.md`. O ELO Cognitivo define o que é permitido e quais condições devem ser satisfeitas; não duplica a implementação das skills.

### 3.1 Orquestrador no Forge

O orquestrador pode receber autorização administrativa para conduzir coleta, reconciliação, execução e atualização de processos no Forge. Essa autorização é operacional, subordinada e revogável.

Relação canônica:

`ELO COGNITIVO → GOVERNA/AUTORIZA → ORQUESTRADOR → ADMINISTRA/EXECUTA NO FORGE`

O orquestrador:

- não redefine o cânone;
- não cria autoridade paralela;
- não promove experiência ao Core por conta própria;
- não cria estruturas semelhantes quando a finalidade já está coberta;
- não transforma ausência de dado em fato;
- deve usar o objeto canônico existente e preservar proveniência;
- deve devolver `GAP` quando a estrutura correta existe, mas ainda não pode ser alimentada legitimamente.

No PCP, `elo_private.pcp_dialogo_turnos` é exemplo de mecanismo já autorizado para persistir coleta e validação do diálogo sem substituir as tabelas operacionais. Dados validados só migram para `mt_previsoes_demanda`, `mt_planos_pcp`, `mt_linhas_plano_pcp`, `mt_ordens_producao` ou outra autoridade específica quando os respectivos gates forem satisfeitos.

## 4. Relação com Core

`ELO Cognitivo → governa → Core`

`Core → materializa → mecanismos cognitivos compartilhados`

O ELO Cognitivo não deve reimplementar no próprio documento ou camada aquilo que pertence ao Core. O Core também não pode redefinir a identidade ou os invariantes do ELO Cognitivo.

## 5. Relação com Simbionte

`ELO Cognitivo → autoriza e governa → Simbionte → observa/refina → candidato → Evolution Gate`

A Simbionte pode explorar mecanismos e propor adaptações, mas não redefine a identidade do ELO, não cria autoridade paralela e não promove diretamente para Core.

## 6. Relação com skills e aprendizado

Caminho canônico:

`SOURCE → EVIDENCE → FORGE SKILL → TEST → EMPIRICAL VALIDATION → CONTEXTUAL EXPERIENCE → GENERALIZATION → EVOLUTION GATE → OPTIONAL CORE PROMOTION`

Uma skill bem-sucedida em uma execução não é automaticamente aprendizado generalizado. A promoção depende do mecanismo de governança já existente.

## 7. Regra de não duplicidade

Antes de criar qualquer artefato atribuído ao ELO Cognitivo, Forge ou orquestrador, verificar se sua finalidade já pertence a:

- `ELO_BOOTSTRAP.md`;
- contratos cognitivos;
- `09-governance/`;
- `src/elo/core/`;
- Forge Specialist Skill Registry;
- memória/evolução da Simbionte;
- schema/tabelas/views/funções já existentes no Supabase;
- contratos e read-models já instalados;
- mecanismos de coleta/estado já autorizados.

Se a finalidade já estiver coberta, deve-se apontar, reutilizar, estender de forma compatível ou consolidar na fonte canônica, em vez de reproduzi-la.

Nova estrutura só é admissível quando houver **função materialmente distinta**, owner definido, ausência comprovada de objeto equivalente e validação de que não cria segunda autoridade.

## 8. Fontes canônicas relacionadas

- `ELO_BOOTSTRAP.md` — identidade e separação das camadas.
- `forge/SPECIALIST_SKILL_REGISTRY.md` — skills e especialistas.
- `src/elo/core/README.md` — faculdade compartilhada do Core.
- `docs/architecture/ELO_HERMES_SYMBIONT_CONTRACT.md` — fronteira de execução e evolução.
- `09-governance/GOVERNANCE_MASTER.md` — governança.
- `Docs/ELO_DUPLICITY_FINAL_PROCESS.md` — processo canônico de identificação e consolidação de duplicidades.

Este arquivo é uma referência de fronteira e não uma nova fonte normativa concorrente.
