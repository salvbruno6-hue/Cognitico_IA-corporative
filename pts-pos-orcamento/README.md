# Gerador de PTS Pós-Orçamento

## O que é

Gerador replicável de documentos **PTS Pós-Orçamento** a partir de arquivos JSON de dados e de um único template Markdown Jinja2.

O mesmo template pode gerar N documentos para N obras diferentes, alterando somente o arquivo JSON de cada obra.

## Estrutura

```text
pts-pos-orcamento/
├── README.md
├── requirements.txt
├── render.py
├── schema.json
├── templates/
│   └── pts_pos_orcamento.md.j2
└── data/
    └── _template.json
```

## Como instalar

No diretório `pts-pos-orcamento/`:

```bash
pip install -r requirements.txt
```

A pasta possui seu próprio `requirements.txt` porque o repositório não possui `requirements.txt` na raiz. O `pyproject.toml` existente permanece inalterado.

## Como usar

```bash
cp data/_template.json data/SO_XXX.json
# preencher o JSON
python render.py data/SO_XXX.json
python render.py data/SO_XXX.json -o out/SO_XXX.md
```

A saída padrão é criada com o mesmo nome do JSON, substituindo a extensão por `.md`.

## Conversão opcional para DOCX

Com Pandoc instalado:

```bash
pandoc out/SO_XXX.md -o out/SO_XXX.docx
```

## Regra de replicação

Cada obra deve possuir **um JSON próprio**, usando o mesmo template Jinja2. A estrutura e a apresentação permanecem uniformes entre as obras.

## Regra de manutenção

Não editar o template para atender "casos específicos". Toda variação de conteúdo deve ser representada no JSON de dados. Alterações estruturais do template devem ser feitas somente quando forem aplicáveis ao padrão geral da PTS Pós-Orçamento.
