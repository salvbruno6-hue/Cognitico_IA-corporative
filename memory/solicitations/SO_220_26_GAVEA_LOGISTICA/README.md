# SO 220.26 — GÁVEA LOGÍSTICA — Revisão de Aprendizado

## Contexto

Fechamento da revisão de aprendizado do ciclo `ELO ANALISAR` da SO 220.26.

Produto-base: `MLT.C06 — Contêiner Depósito 20 pés`.
Soluções analisadas: bancada Multiteiner, prateleiras `EXC-031` e instalação elétrica com referência de modelo marítimo de escritório.

## Respostas do owner e classificação

| Q | Decisão do owner | Classificação | Tratamento |
|---|---|---|---|
| 1 | Prateleira deve ser avaliada por módulo. | LEARNING_CANDIDATE | Aplicar avaliação modular preservando a memória física/econômica do EXC; não reduzir a um rateio sem reconstruir a composição quando necessário. |
| 2 | Para a SO 220.26, 2 módulos de 1.375 mm são definitivos. | CASE | Quantitativo definitivo desta SO: 2 módulos = 2.750 mm lineares. |
| 3 | O EXC-031 já serve como consulta para projetos que aplicam prateleira com largura menor que o padrão do almoxarifado. | PRECEDENT | Preservar o EXC-031 como referência consultiva modular para larguras menores; a aplicação deve testar a geometria do projeto. |
| 4 | Instalação derivada deve manter referência do modelo usado como origem. | LEARNING_CANDIDATE | Toda composição derivada deve registrar explicitamente o modelo de referência, sem confundir origem com produto entregue. |
| 5 | Itens específicos do modelo de origem devem ser sinalizados para decisão, não removidos automaticamente. | LEARNING_CANDIDATE | Itens potencialmente não aplicáveis viram alerta/decisão explícita; sem exclusão silenciosa. |
| 6 | Padrão elétrico informado: 3 iluminações + 3 tomadas TUG + 1 TUE para ar-condicionado. | LEARNING_CANDIDATE | Não promover ainda como padrão corporativo; requer confronto com evidência técnica/catálogo/memória existente. |
| 7 | Códigos `PEND-*` permanecem provisórios até consolidação taxonômica. | GOVERNANÇA/CANDIDATO | Não converter `PEND-C13-*` em `ELE*` sem reconciliação da Lista-Mãe e governança. |
| 8 | Mão de obra deve trazer decomposição por atividade. | LEARNING_CANDIDATE | Exigir memória de produtividade por atividade: elétrica, mobiliário/prateleira, testes/acabamento e supervisão quando aplicável. |
| 9 | MLT.B09 é padrão Multiteiner para a bancada desta aplicação. | CASE + GAP TAXONÔMICO | Usar MLT.B09 nesta SO; não generalizar enquanto o conflito B09 × B01 não for reconciliado. |
| 10 | B09 e B01 podem ser itens diferentes; primeiro entender a distinção. | GAP | Proibido normalizar B09 para B01 por similaridade textual. Investigar identidade, dimensões, função e cadastro. |
| 11 | Valores de MLT.C06 e MLT.B09 podem estar em camada comercial separada. | CASE/PROCESSO | Na SO 220.26, o orçamento de adequação pode permanecer separado do preço comercial de locação dos produtos-base, desde que a separação seja explícita. |
| 12 | Arredondamento: aplicar BDI e arredondar somente no fechamento final. | LEARNING_CANDIDATE | Regra candidata: preservar precisão intermediária e arredondar o total final; para SO 220.26 o fechamento matemático é R$ 3.026,97. |

## Decisões definitivas da SO 220.26

1. Prateleira: 2 módulos de 1.375 mm, totalizando 2.750 mm lineares.
2. EXC-031 permanece como origem técnica da solução de prateleiras.
3. MLT.B09 permanece como bancada padrão adotada nesta SO.
4. A instalação elétrica derivada deve registrar o modelo usado como referência.
5. Itens específicos do modelo de referência devem ser sinalizados para decisão; não excluir automaticamente.
6. Valores comerciais de MLT.C06/MLT.B09 podem permanecer em camada comercial separada da adequação.
7. O arredondamento do orçamento deve ocorrer no fechamento final.

## Candidatos reutilizáveis

- avaliação de prateleira por módulo, preservando geometria e composição;
- EXC-031 como referência consultiva para projetos com larguras menores que o padrão completo do almoxarifado;
- obrigação de registrar o modelo de origem quando uma composição é derivada de outro produto;
- sinalização explícita de itens potencialmente não aplicáveis em vez de exclusão automática;
- decomposição da mão de obra por atividade/produtividade;
- arredondamento somente no fechamento final do orçamento.

## GAPs preservados

### GAP-TAX-MLT-B09-B01

`MLT.B09` não deve ser convertido para `MLT.B01` por semelhança de descrição. Os dois códigos podem representar itens distintos. Investigar identidade cadastral, dimensões, aplicação e histórico antes de consolidar taxonomia.

### GAP-ELETRICA-PADRAO-CONTÊINER

O owner informou como padrão elétrico: **3 pontos de iluminação + 3 tomadas TUG + 1 TUE para ar-condicionado**. Esta informação permanece `LEARNING_CANDIDATE` até confronto com documentação técnica, Lista-Mãe, kits existentes e precedentes suficientes.

## Governança

- As respostas do owner encerram a revisão de aprendizado desta SO, mas não promovem automaticamente regra ao Core.
- `CASE` permanece específico da SO.
- `PRECEDENT` é referência consultiva.
- `LEARNING_CANDIDATE` exige evidência/recorrência antes de `VALIDATED_LEARNING`.
- GAPs permanecem abertos até reconciliação explícita.
- Não criar segunda taxonomia, segundo kit elétrico ou nova autoridade de memória.
