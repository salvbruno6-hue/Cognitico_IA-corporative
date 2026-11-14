# ELO ORÇAR — Aprendizado candidato: busca de itens e emprego da mão de obra — SO 233.26 MLT.M05

**Estado:** CANDIDATO EM TESTE / NÃO APROVADO PELO ANALISTA / NÃO CANONIZAR.
**Owner de execução:** FORGE-BUDGETING-001, subordinado às regras de `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/SKILL.md`.
**Fontes:** tabela de orçamento M05 transcrita pelo Analista na conversa de 11/11/2026; Supabase `lista_mae`, `excedentes`, `excedente_itens`, `excedente_mao_obra` e `rh_mao_obra_custos`; contrato `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/PROMPT.md`.
**Limite de evidência:** texto transcrito mostra seções funcionais 2.2, 2.3 e 2.4, não permite afirmar endereços/intervalos de células Excel exatos.

## Hipótese de aprendizado: busca orientada pelo item identificado
1. Identificar componente e sua função em TR/layout/decisão do orçamento.
2. Pesquisar **antes de criar** na `lista_mae` por descrição, aplicação, `cod_item`, `cod_produt`, unidade e valor unitário. Se item for uma necessidade composta, pesquisar também `excedentes`, `excedente_itens` e `excedente_mao_obra`.
3. Comparar equivalência técnica, insumos, mão de obra embutida, quantidade, preço, data/fonte e escopo. Não converter item parecido em equivalente automático.
4. Inserir na seção **2.2** quantidade × valor numérico, mantendo o vínculo à fonte e sem escrever instruções textuais na coluna de preço (`#VALOR!`).
5. Em caso de preço divergente (ex.: ESQ006 R$ 162,50 na Lista-Mãe e R$ 227,09 na revisão supervisionada), registrar ambas as fontes e o responsável pela escolha; não sobrescrever a origem canônica.
6. Usar `EXC-011` para o ponto de tomada completo (R$ 95,65, `inclui_mao_obra=true`), distinto de `ELE131` peça isolada (R$ 4,85). `EXC-002` ponto hidrossanitário R$ 105,86 não possui M.O. embutida. Evitar somar mão de obra de EXC novamente.
7. Documentar alternativas descartadas, lacunas de conformidade e orçamento em análise.

## Exemplo observado na composição 2.2 do M05
| Linha | Código | Quantidade | Preço adotado | Origem e ressalva |
|---|---|---:|---:|---|
| 2.2.1 | ESQ006 | 2 | R$ 227,09 | preço dado pelo Analista; Lista-Mãe R$ 162,50: conflito a reconciliar |
| 2.2.2 | HID043 | 1 | R$ 133,72 | Lista-Mãe, modelo marcado PNE: equivalência pendente |
| 2.2.3 | EXC-011 | 3 | R$ 95,65 | EXC completo; inclui M.O.; composição demanda conciliação |
| 2.2.4 | ELE032 | 1 | R$ 39,33 | decisão explícita do Analista |
| 2.2.5 | EXC-002 | 1 | R$ 105,86 | referência de ponto hidrossanitário; sem M.O. |
| 2.2.6 | ELE069 | 1 | R$ 91,68 | decisão explícita do Analista |

## Intervalos funcionais e emprego da mão de obra
- **2.3 MÃO DE OBRA INTERNA:** reservado às pessoas/dias efetivamente empregados na fabricação/adaptação interna. Colunas da tabela transcrita: `Item | Função | Dias trabalhados | Colaboradores | Unid. | Valor diário | Valor parcial`. Regra de cálculo: `dias × colaboradores × custo_dia`.
- **2.4 MÃO DE OBRA EXTERNA:** intervalo separado da planilha, **não utilizado no M05 demonstrado**. Permanecer sem dias/quantidades/custos quando não houver trabalho externo demonstrado.
- As tarifas do M05 foram confirmadas por `rh_mao_obra_custos` com `cargo`, `custo_dia_22`, `ano_referencia=2026`, `ativo=true`: Encarregado/Supervisor R$ 448,21; Profissional R$ 275,82; Ajudantes R$ 235,92.
- Eletricista e Bombeiro hidráulico na demonstração usam **por decisão do Analista** o custo de Profissional R$ 275,82; não se deve inferir que exista linha específica para esses cargos na tabela RH.
- Distribuição observada: Encarregado 0,1 dia × 1 → R$ 44,82; Profissional 0 × 1 → R$ 0,00; Eletricista 0,2 × 1 → R$ 55,16; Bombeiro hidráulico 0,3 × 1 → R$ 82,75; Ajudante 1 × 1 → R$ 235,92. Subtotal **R$ 418,65**.
- **Risco de duplicidade:** `EXC-011` já contém mão de obra de profissional e ajudante; verificar o escopo real do eletricista e do ajudante da seção 2.3 e conciliar tempos/valores.
- O texto transcrito não identifica endereços exatos da planilha Excel; não inventar coordenadas.
- Não inferir que serviços auxiliares tenham de ser lançados automaticamente em 2.1. Consultar `elo_orcamento_servicos_auxiliares` e associação em `elo_orcamento_composicao_itens`, respeitando estado `EM_ANALISE`.

## Testes supervisionados exigidos antes do Evolution Gate
1. Buscar item simples e recuperar `cod_item`, preço, aplicação, unidade e fonte da Lista-Mãe.
2. Buscar item composto no EXC, abrir os componentes e identificar com/sem M.O. embutida.
3. Aplicar as escolhas ELE032 e ELE069 sem trocar códigos.
4. Apontar e preservar a divergência ESQ006; não substituir R$ 227,09 sem autorização.
5. Preencher e recalcular 2.2, evitando `#VALOR!`.
6. Distinguir emprego da seção 2.3 da disponibilidade da seção 2.4.
7. Demonstrar valor por cargo × dias × colaboradores e subtotal R$ 418,65.
8. Sinalizar possível duplicidade com EXC-011 antes de fechamento.
9. Consultar os 10 serviços auxiliares persistidos e não lançá-los sem aplicação confirmada.
10. Validar com o Analista, corrigir divergências e só então submeter à governança/Evolution Gate.

**Regra de governança:** este documento é um caso supervisionado Forge, não substitui a diretriz mestre nem define regra universal de Core. Mantê-lo em branch/PR **não merged** até aprovação explícita do Analista.
