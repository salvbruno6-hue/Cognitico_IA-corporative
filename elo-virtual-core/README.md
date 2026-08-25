# ELO Virtual Core — Sandbox de Simulação

## Finalidade

Camada experimental para pesquisa e testes de cruzamentos operacionais. Não é o Core oficial, não é fonte canônica de dados e não deve comandar produção.

## Fluxo atual

`demanda -> materiais -> recursos -> capacidade/prazo -> diagnóstico`

## Regras de segurança lógica

- Dados desta pasta são explicitamente simulados.
- Recursos são abstrações; não pressupõem máquinas, empilhadeiras ou outros equipamentos reais.
- O simulador não inventa dados operacionais ausentes.
- Parâmetros não podem ser alterados automaticamente.
- O bloqueio automático permanece desabilitado.
- Decisões são diagnósticos de pesquisa, não ordens operacionais.

## Estrutura

- `data/`: datasets e relacionamentos simulados.
- `configuracoes/`: parâmetros experimentais.
- `regras/`: orquestrador de diagnóstico.
- `testes/`: cenários e asserts de regressão.

## Execução local

Na raiz de `elo-virtual-core`:

```bash
python regras/orquestrador.py
python testes/simular_cenarios.py
```

O primeiro comando gera `data/diagnostico_pcp.json`. O segundo valida que mudanças controladas nos dados alteram as decisões.

## Limite do modelo

A ausência de dados cotidianos reais sobre recursos, tempos, produtividade ou capacidade deve permanecer representada como desconhecida. Valores deste sandbox existem somente para testar o comportamento do ELO.
