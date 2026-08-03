# ELO Enterprise Integration

## Objetivo

Definir a arquitetura de integração da EIP com sistemas corporativos e industriais, permitindo que o ELO seja adotado por diferentes empresas sem depender de um ERP, MES, PLM, WMS ou tecnologia específica.

## Sistemas previstos

- ERP
- MES
- PLM
- WMS
- CRM
- bancos de dados
- APIs corporativas
- sistemas legados
- filas e event streams
- arquivos e fontes controladas

## Princípio central

O ELO não substitui automaticamente sistemas especialistas. Ele integra seus dados e eventos quando necessários para conhecimento, análise, planejamento, decisão ou governança.

## Arquitetura

```text
Enterprise System
      ↓
Adapter / Connector
      ↓
Contract Validation
      ↓
Security + Governance
      ↓
Canonical ELO Representation
      ↓
Domains / Knowledge / Analytics / Cognitive Layer
```

## Regras

- cada integração deve declarar sistema de origem e responsabilidade
- fonte de verdade deve permanecer explícita
- formatos proprietários devem ser isolados em adapters
- contratos canônicos devem reduzir acoplamento entre sistemas
- sincronizações devem preservar identidade, timestamp e versionamento quando aplicável
- falhas de integração devem ser observáveis e auditáveis

## Portabilidade industrial

A separação entre contratos canônicos e adaptadores específicos permite instalar a EIP em empresas com diferentes stacks tecnológicos, mantendo os mesmos conceitos de domínio e capacidades cognitivas.

## Estrutura prevista

```text
enterprise/
├── README.md
├── contracts/
├── adapters/
├── erp/
├── mes/
├── plm/
├── wms/
├── databases/
└── events/
```
