# ELO — TAXONOMIA, CATÁLOGO E CONSULTA SQL

**Camada:** `04-knowledge-handbook`  
**Função:** padronizar a consulta estruturada de produtos, serviços, módulos, contêineres, características, composições e histórico de orçamento.

## 1. Finalidade

Esta camada cria uma linguagem de consulta para o Especialista e o ELO encontrarem rapidamente conhecimento reutilizável sem confundir categorias, produtos, serviços ou composições.

Ela deve ser alimentada por dados corporativos validados. Não cria dados inexistentes.

## 2. Taxonomia mínima

`FAMÍLIA → CATEGORIA → TIPO → MODELO → VARIANTE → COMPONENTE → SERVIÇO → EXCEDENTE → COMPOSIÇÃO`

Categorias corporativas mínimas: **MLT-M — módulos** e **MLT-C — contêineres**, além de produtos/componentes, serviços de fabricação, instalação, mobilização, manutenção, excedentes e composições de custo.

MLT-M e MLT-C são categorias distintas e nunca devem ser tratados como sinônimos.

## 3. Estrutura lógica de dados

```text
produto
  ├── categoria
  ├── modelo
  ├── características
  ├── dimensões
  ├── aplicações
  └── componentes

serviço
  ├── categoria
  ├── unidade
  ├── recursos
  ├── mão de obra
  └── composição

excedente
  ├── tipo
  ├── base
  ├── quantitativo
  ├── composição
  └── memória de cálculo

referência
  ├── fonte
  ├── data
  ├── local
  ├── SO
  └── confiabilidade
```

## 4. Padrão de consulta SQL

A consulta deve identificar a entidade antes de filtrar características.

```sql
SELECT id, codigo, nome, categoria, modelo, unidade, status
FROM produtos
WHERE status = 'ATIVO'
  AND categoria = :categoria
  AND (:modelo IS NULL OR modelo = :modelo);
```

Consulta por características:

```sql
SELECT p.*
FROM produtos p
JOIN produto_caracteristicas pc ON pc.produto_id = p.id
WHERE pc.caracteristica = :caracteristica
  AND pc.valor = :valor
  AND p.status = 'ATIVO';
```

Consulta de serviços:

```sql
SELECT id, codigo, descricao, unidade, status
FROM servicos
WHERE status = 'ATIVO'
  AND categoria = :categoria;
```

Consulta de excedentes validados:

```sql
SELECT id, tipo, descricao, unidade, base_modelo, composicao_id, data_referencia
FROM excedentes
WHERE status = 'VALIDADO'
  AND base_modelo = :base_modelo
  AND tipo = :tipo;
```

## 5. Regras de consulta

1. Identificar categoria antes do produto.
2. Aplicar status e validade.
3. Preferir referências mais recentes quando tecnicamente equivalentes.
4. Não substituir automaticamente uma referência específica apenas por menor preço.
5. Registrar fonte quando o resultado influenciar o orçamento.
6. Se houver múltiplos resultados compatíveis, apresentar alternativas.
7. Se não houver resultado, declarar ausência de referência; não inventar registro.

## 6. SQL não substitui julgamento técnico

`SQL → RECUPERA → ESPECIALISTA VALIDA → ELO CONTEXTUALIZA → ORÇAMENTO`

A aplicabilidade depende da SO, PTS Técnica, contexto, unidade, modelo, prazo, local e premissas.

## 7. Governança

Registros devem possuir, quando possível: origem, data de referência, status, responsável/validação, unidade, contexto de aplicação e versão. Histórico sem validação é referência histórica, não padrão vigente.
