# Memórias de Cálculo Recorrente — Especialista de Orçamento

**Status:** Camada operacional governada — proposta para validação do ELO  
**Domínio:** Especialista de Orçamento  
**Finalidade:** armazenar padrões de cálculo que aparecem repetidamente em orçamentos e permitir sua reutilização paramétrica em novas dimensões, sem transformar uma experiência isolada em regra canônica automaticamente.

## 1. Conceito

Uma memória de cálculo recorrente é um **molde paramétrico de cálculo**, não um preço fixo.

Ela pode registrar, por exemplo, que uma janela basculante normalmente é composta por:

- tubos/perfis;
- chapas;
- área ou perímetro da esquadria;
- ferragens/acessórios;
- solda/fabricação;
- pintura/acabamento;
- vidro, quando aplicável;
- instalação;
- demais componentes identificados pela composição oficial.

A mesma lógica pode ser reaplicada para outra largura e altura, desde que os parâmetros, unidades e relações estejam validados.

## 2. Estrutura mínima da memória

Cada memória deve possuir:

| Campo | Finalidade |
|---|---|
| `memory_id` | Identificador único da memória |
| `nome` | Nome operacional do padrão |
| `familia` | Família técnica do item |
| `contexto` | Situação em que apareceu |
| `parametros_entrada` | Dimensões e variáveis necessárias |
| `componentes` | Materiais/serviços relacionados |
| `relacoes` | Relações dimensionais entre parâmetros |
| `formulas` | Fórmulas validadas |
| `unidades` | Unidade de cada parâmetro e resultado |
| `fonte` | Origem documental/experiência |
| `confiabilidade` | Grau de confiança da memória |
| `status` | experimental, validada ou canônica |
| `ultima_validacao` | Data da última revisão |
| `usos` | Quantidade de reutilizações |
| `divergencias` | Casos em que a memória não se aplicou |

## 3. Exemplo — janela basculante

### Memória candidata

`MEM-CALC-ESQ-JANELA-BASCULANTE`

**Entrada:**

- largura `W`;
- altura `H`;
- quantidade `Q`;
- tipo de perfil/tubo;
- espessura da chapa;
- tipo de vidro, quando aplicável;
- acessórios/ferragens;
- acabamento;
- condição de instalação.

**Relações geométricas possíveis:**

`Área = W × H`

`Perímetro = 2 × (W + H)`

As relações de consumo de tubos, chapas, ferragens e mão de obra **não devem ser presumidas** apenas a partir da geometria. Elas devem ser aprendidas de composição, ficha técnica ou histórico validado.

### Aplicação paramétrica

Se uma memória validada possuir consumo de tubo por unidade de perímetro:

`Tubo_total = Perímetro × coeficiente_tubo`

Se possuir consumo de chapa por área:

`Chapa_total = Área × coeficiente_chapa`

Se possuir quantidade fixa de ferragens por janela:

`Ferragens_total = Q × ferragens_por_unidade`

Os coeficientes precisam possuir origem e unidade. Sem isso, a memória permanece experimental.

## 4. Separação entre lógica e preço

A memória guarda principalmente **relações de cálculo**.

Exemplo:

`janela 1200 × 800 → área, perímetro, componentes e coeficientes`

Ela não deve gravar automaticamente:

`janela = R$ X`

O preço deve ser obtido da tabela/composição vigente.

Assim, uma mesma memória pode funcionar quando os preços de tubos, chapas, mão de obra ou acessórios forem atualizados.

## 5. Reutilização em novas dimensões

Quando surgir uma nova janela:

1. identificar a família;
2. procurar memória recorrente compatível;
3. comparar parâmetros da nova solicitação com os parâmetros da memória;
4. recalcular as grandezas dimensionais;
5. reaplicar somente coeficientes cuja validade esteja comprovada;
6. consultar preços atuais;
7. identificar componentes que mudaram por causa da dimensão;
8. enviar divergências para o Especialista/ELO.

## 6. Limites de extrapolação

A memória não pode ser aplicada cegamente quando:

- a dimensão estiver fora da faixa validada;
- o material mudar;
- o sistema construtivo mudar;
- a função mudar;
- a quantidade de componentes mudar estruturalmente;
- houver exigência normativa diferente;
- a composição de origem não for equivalente.

Nesses casos, o Especialista deve marcar a memória como **parcialmente aplicável** ou **não aplicável**.

## 7. Aprendizado por recorrência

Quando o mesmo padrão aparecer repetidamente:

`ocorrência → comparação → agrupamento → memória candidata → validação → reutilização`

A recorrência aumenta a prioridade de avaliação, mas **não concede aprovação automática**.

## 8. Loop de evolução

```text
Novo orçamento
      ↓
Identificação do item
      ↓
Existe memória recorrente?
   ┌──┴──┐
  SIM   NÃO
   ↓     ↓
Validar  Registrar ocorrência
   ↓     ↓
Aplicar  Agrupar recorrências
   ↓     ↓
Auditar  Criar memória candidata
   └──┬──────┘
      ↓
ELO avalia relação e evidência
      ↓
Especialista valida aplicação
      ↓
Aprovada?
  ┌──┴──┐
 NÃO   SIM
  ↓     ↓
Temporal  Memória validada
        ↓
  Reutilização paramétrica
```

## 9. Relação com a memória temporal

Uma experiência nova pode primeiro existir como memória temporal de contexto.

Quando houver recorrência e evidência suficiente, ela pode ser promovida para **Memória de Cálculo Recorrente**.

Somente após avaliação de identidade canônica, consistência e impacto sistêmico poderá ser promovida para regra canônica.

## 10. Auditoria do ELO

O ELO deve verificar:

- se a memória realmente corresponde à família do item;
- se os parâmetros estão completos;
- se as unidades são compatíveis;
- se os coeficientes possuem origem;
- se houve extrapolação indevida;
- se a memória duplicará uma composição existente;
- se a aplicação gera excedente corretamente;
- se houve mudança estrutural que exige especialista;
- se a memória deve permanecer temporal ou ser promovida.

## 11. Resultado esperado

O objetivo é que o Especialista deixe de recalcular do zero padrões recorrentes.

Ele passa a trabalhar com:

**identificação → memória → parametrização → cálculo → preço vigente → auditoria → aprendizado.**

Isso permite acelerar orçamentos recorrentes sem transformar experiências não verificadas em regras permanentes.