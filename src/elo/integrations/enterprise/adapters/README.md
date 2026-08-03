# Enterprise Integration Adapters

## Objetivo

Definir os adaptadores concretos que ligam os contratos canônicos do ELO aos sistemas empresariais e industriais reais.

## Função

Cada adapter converte o contrato canônico para o formato específico do sistema externo e vice-versa, isolando o núcleo do ELO de detalhes proprietários.

## Adaptadores previstos

- ERP Adapter
- MES Adapter
- PLM Adapter
- WMS Adapter
- Database Adapter
- API Adapter
- Legacy Adapter
- Event Adapter

## Responsabilidades

- autenticar com o sistema externo
- converter payloads
- lidar com peculiaridades do sistema de origem/destino
- preservar rastreabilidade de mapeamento
- capturar e normalizar erros
- respeitar políticas de segurança e governança

## Princípios

- adaptador é substituível
- adaptador não deve conter regra central do domínio
- adaptador não deve alterar o contrato canônico
- adaptadores devem ser facilmente testáveis com mocks e stubs

## Estrutura prevista

```text
adapters/
├── README.md
├── erp/
├── mes/
├── plm/
├── wms/
├── databases/
├── api/
├── legacy/
└── events/
```

## Regras

- toda conversão deve ser explícita e rastreável
- o adaptador deve preservar contexto mínimo necessário para auditoria
- falhas no sistema externo devem ser classificadas e reportadas de forma padronizada
- nenhum adaptador pode bypassar o contrato canônico
