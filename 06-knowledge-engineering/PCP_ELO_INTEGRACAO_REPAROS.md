---
parent: PCP_INSTRUCOES_GERAIS_GOVERNANCA.md
level: 3
type: instrucao_especializada
process: PCP externo — cobertura física e integração ELO
purpose: detalhar a interpretação do ELO sobre reparos e cobertura
---

# Instrução ELO: integração PCP, reparos e cobertura de demanda

## Objetivo
Definir como o ELO deve interpretar a relação entre demanda, estoque, reparos e fabricação no PCP externo.

## Cadeia oficial
Demanda Comercial → Histórico Comparável → Previsão → Fator → Estoque → Reparos Recuperáveis → Produção Programada → Déficit de Fabricação → Carga Operacional → Demanda Humana → RH.

## Regra do fator
O fator continua sendo calculado sobre a demanda comparável, por natureza e produto/modelo quando aplicável.

O fator não deve ser aplicado ao estoque, ao número de reparos ou ao quadro atual de RH.

## Regra de reparo
Reparo só entra como cobertura quando a unidade modular estiver identificada e a condição de status/data for válida.

Sem unidade: GAP_REPARO_SEM_UNIDADE.
Sem data confiável quando necessária: GAP_REPARO_SEM_DATA.

GAP não vira cobertura por inferência.

## Regra contra dupla contagem
A cobertura física é consolidada no nível de modelo. A natureza da demanda continua separada no cálculo de comparabilidade e fator.

Assim, a mesma unidade não pode ser contada simultaneamente para Evento, Sazonalidade, SPOT ou outra natureza.

## Déficit
Necessidade adicional de fabricação = máximo entre zero e:
demanda prevista - estoque disponível - reparos recuperáveis - produção programada.

Esse resultado é analítico. Não libera automaticamente uma ordem de produção.

## Próximo estágio
Somente após identificar o saldo adicional de fabricação o PCP pode avaliar carga, capacidade, gargalos, lead time, sequenciamento, componentes, composição funcional, produtividade e posteriormente demanda humana.

## Projeto Integrador
A reflexão operacional deve considerar visibilidade, lead time, tempos padrão, capacidade, sequenciamento, reprogramações e gargalos. Essas dimensões contextualizam o impacto do saldo de fabricação, sem alterar a regra de comparabilidade da demanda.

## Quando a planilha da Qualidade chegar
1. Identificar o campo de identidade do módulo.
2. Reconciliar com mt_unidades_modulares.
3. Reconciliar modelo e taxonomia.
4. Reconciliar com mt_ordens_reparo.
5. Identificar faltantes e duplicidades.
6. Validar datas e status.
7. Preparar a carga somente após validação.
8. Testar a cobertura.
9. Versionar a regra no Git.
10. Validar o estado no Supabase.

## Governança
GitHub é a autoridade canônica para regras, documentação, migrações, views e funções.
Supabase é a autoridade do estado operacional efetivamente armazenado.

Divergências devem ser registradas e reconciliadas. Não editar manualmente o histórico de migrações para esconder divergências.

## Gate de liberação
Documentação versionada → regra de identidade definida → estrutura Supabase conhecida → regra de cobertura definida → validação de duplicidade definida → procedimento de carga definido → teste de reconciliação executável.

A planilha da Qualidade será uma fonte operacional a validar, não uma nova autoridade de produto.
