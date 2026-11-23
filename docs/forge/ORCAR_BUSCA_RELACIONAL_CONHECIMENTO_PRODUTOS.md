# Forge / ORÇAR — Roteiro de consulta relacional ao conhecimento de produtos

**Status:** PROPOSTA PARA GOVERNANÇA (não implementado como automação)
**Domínio:** Forge — Especialista de Orçamento / pesquisa técnica de materiais
**Autoridade operacional:** GitHub (contratos); **persistência:** Supabase Elo-forge
**Escopo:** consultas de leitura para SO, TR, PTS técnica, equivalência, composição e excedentes.

## 1. Objetivo
Ao pesquisar um produto ou material para orçamento, consultar as fontes relacionadas, sem encerrar a pesquisa na primeira tabela encontrada. Recuperar características técnicas detalhadas, evidências, aplicações, modelos e lacunas, com proveniência. Não inventar vínculos, parâmetros ou preços.

## 2. Inventário de tabelas existentes no Supabase

| Tabela `public` | Papel na busca |
|---|---|
| `elo_produtos_conhecimento` | Cadastro técnico central de produtos |
| `elo_produtos_atributos` | Atributos individuais dos produtos |
| `elo_produtos_evidencias` | Evidências e documentação associadas |
| `elo_produtos_modelos` | Relacionamento de produtos com modelos |
| `elo_aprendizado_produtos` | Aprendizados relacionados a produtos |
| `elo_conhecimento_itens` | Itens de conhecimento corporativo, incluindo fichas técnicas |
| `elo_conhecimento_fontes` | Fontes e proveniência |
| `elo_conhecimento_vinculos` | Relacionamentos entre itens de conhecimento |
| `elo_conhecimento_nucleos` | Organização dos núcleos de conhecimento |
| `lista_mae` | Cadastro de materiais e componentes |

**Observação:** as cinco views `elo_knowledge.vw_conhecimento_*` são interfaces de consulta relacionadas. Confirmar sua definição, permissões e cobertura antes de utilizá-las como fonte de execução.

## 3. Relações verificadas e lacunas
- `elo_produtos_atributos.produto_id` → `elo_produtos_conhecimento.id` (FK existente).
- `elo_produtos_evidencias.produto_id` → `elo_produtos_conhecimento.id` (FK existente).
- `elo_produtos_modelos.produto_id` → `elo_produtos_conhecimento.id` (FK existente).
- `elo_produtos_modelos.modelo_id` → `modelos.id` (FK existente).
- `elo_conhecimento_vinculos.item_origem_id` e `item_destino_id` → `elo_conhecimento_itens.id` (FKs existentes).
- **GAP:** não foi identificada FK direta entre `elo_produtos_conhecimento` e `elo_conhecimento_itens`. Investigar relações genéricas já existentes antes de propor nova associação. Chaves primárias próprias devem ser preservadas.
- A existência de tabelas não implica dados preenchidos ou relacionamento validado; não fazer JOIN por nome semelhante sem evidência.

## 4. Procedimento de busca obrigatório para o Forge ORÇAR
1. Identificar requisito, material, sinônimos, código, fabricante, modelo, contexto e versão da SO/TR.
2. Consultar `lista_mae`, `elo_produtos_conhecimento` e taxonomia/modelos existentes.
3. Para identidade comprovada, percorrer `elo_produtos_atributos`, `elo_produtos_evidencias`, `elo_produtos_modelos` e `elo_aprendizado_produtos`.
4. Consultar `elo_conhecimento_itens` por chave, título, conteúdo e termos técnicos; verificar `elo_conhecimento_nucleos`, `elo_conhecimento_fontes` e `elo_conhecimento_vinculos`. Distinguir associação explícita de candidato textual não vinculado.
5. Recuperar fichas técnicas e propriedades específicas (espessura, material, desempenho térmico, resistência mecânica, reação ao fogo, instalação, durabilidade, aplicação, limitações), **somente quando presentes**.
6. Confrontar documentos oficiais do modelo e TR; separar característica geral de aplicação comprovada ao modelo da SO.
7. Emitir resultado com `REQUISITO | PRODUTO | CARACTERÍSTICA | VALOR/UNIDADE | FONTE/REVISÃO | IDENTIDADE/VÍNCULO | CONFIANÇA | STATUS | GAP | IMPACTO NO ORÇAMENTO`.
8. Não duplicar materiais ou custos já incorporados ao modelo-base; não preencher planilha sem comando explícito.
9. Quando não houver evidência, declarar `NÃO LOCALIZADO`; quando houver divergência, registrar `GAP` e solicitar validação técnica.
10. O especialista Forge não promove experiências específicas ao Core; alterações estruturais passam por testes, governança e Evolution Gate.

## 5. Exemplo real que motivou a regra
Uma busca apenas em `elo_produtos_conhecimento` não recuperou fichas técnicas de materiais. A consulta ampliada em `elo_conhecimento_itens` identificou:
- `MATERIAL_PISO_LVT_PERSONNALITE_2MM` — ficha técnica do piso LVT Personnalité 2 mm, incluindo capa de uso, PUR, classe de reação ao fogo e estabilidade dimensional.
- `MATERIAL_PAINEL_WALL_DECORLIT` — aplicações do painel Wall DECORLIT; não contém valores certificados de resistência estrutural ou absorção de água.

Esses registros não comprovam automaticamente equivalência ao TR nem aplicação aos modelos M14/M06.

## 6. Integração com contratos já existentes
Esta especificação **complementa**, sem substituir:
- `elo-virtual-core/configuracoes/ELO_SUPABASE_AUTOROUTER_PROMPT.md` — consulta corporativa, autorroteamento e cruzamento de relacionamentos;
- `prompts/ELO_ORCAMENTO_PROMPT_PIPELINE.md` — P00, P02, P03, P05, P07 e P08.

**Próxima implementação:** localizar o owner executável do roteamento do Forge, acrescentar busca relacional com critérios de proveniência e testes de recuperação. Não considerar a automação entregue pela mera publicação deste documento.

## 7. Critérios de aceite para implementação futura
- Consulta `piso LVT` recupera a ficha `MATERIAL_PISO_LVT_PERSONNALITE_2MM`, inclusive propriedades detalhadas, com fonte.
- Consulta `painel Wall` recupera o conhecimento DECORLIT, sinalizando ausência de laudo de carga.
- Resultado separa associação por FK de candidato identificado por texto.
- Respeita a autoridade documental, não cria preço, não presume equivalência e registra GAPs.
- Testes e Evolution Gate precedem merge/ativação de automação.

**Governança:** proposta documental para revisão; não representa migração SQL nem alteração dos dados persistidos.
