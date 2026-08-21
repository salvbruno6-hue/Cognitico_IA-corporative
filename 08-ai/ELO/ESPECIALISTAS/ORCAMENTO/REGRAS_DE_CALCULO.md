# Regras Canônicas de Cálculo — Especialista de Orçamento

**Versão:** 1.0  
**Status:** Proposta operacional para validação do ELO  
**Governança:** ELO  
**Domínio:** Especialista de Orçamento  
**Finalidade:** concentrar os cálculos recorrentes usados pelo Especialista, evitando fórmulas dispersas, premissas ocultas e recomputações inconsistentes.

> Esta base define **como calcular**, não define automaticamente **preços**. Preços, produtividades, perdas, coeficientes e valores unitários devem vir de tabelas oficiais, composição validada, documento de referência ou decisão explicitamente registrada.

## 1. Princípio de cálculo

Toda linha calculada deve possuir:

1. item ou composição de origem;
2. unidade de medida;
3. quantidade-base;
4. fator(es) aplicável(is);
5. fórmula utilizada;
6. valor unitário, quando houver;
7. origem do valor unitário;
8. resultado;
9. evidência ou premissa;
10. indicação se o resultado é padrão, excedente, customização ou pendência.

Nunca inventar coeficiente, preço, produtividade, perda ou quantidade.

## 2. Quantidade direta

Quando a quantidade estiver explicitamente definida:

`Q = quantidade informada`

Exemplo: 3 tomadas adicionais → `Q = 3 un`.

## 3. Área

Para superfícies retangulares:

`A = comprimento × largura`

Para várias superfícies:

`A_total = Σ A_i`

Aplicar descontos de vãos somente quando a regra da composição determinar que portas, janelas ou aberturas devem ser descontadas:

`A_liquida = A_bruta − A_descontos`

Não descontar automaticamente. A regra depende da composição oficial.

## 4. Comprimento linear

Para elementos dimensionados por comprimento:

`L_total = Σ L_i`

Exemplos: rodapé, perfis, calhas, tubulações, eletrodutos, acabamentos e arremates.

## 5. Perímetro

Para ambiente retangular:

`P = 2 × (comprimento + largura)`

Usar somente quando a composição exigir perímetro.

## 6. Volume

Para elementos prismáticos:

`V = comprimento × largura × altura`

Exemplo: concreto, bases ou volumes de material quando a unidade da composição for `m³`.

## 7. Conversão de unidades

Sempre normalizar a unidade antes de multiplicar quantidade por preço.

Exemplos:

- `1 m = 1.000 mm`
- `1 m² = 10.000 cm²`
- `1 m³ = 1.000 litros`

A conversão deve ficar registrada quando alterar a unidade original da informação.

## 8. Quantidade com fator

Quando uma composição utiliza quantidade-base multiplicada por fator:

`Q_composição = Q_base × fator`

O fator deve possuir origem identificável. Se não houver fator oficial, o Especialista deve registrar a pendência em vez de inventá-lo.

## 9. Perda / acréscimo técnico

Quando houver percentual de perda formalmente aplicável:

`Q_com_perda = Q_base × (1 + perda/100)`

A perda não deve ser aplicada duas vezes. O Especialista deve conferir se a composição ou o preço unitário já incorpora a perda.

## 10. Custo direto do item

`Custo_item = Quantidade × Valor_unitário`

Para composição:

`Custo_composição = Σ Custo_item`

Separar, quando aplicável:

- material;
- mão de obra interna;
- mão de obra externa;
- equipamento;
- transporte;
- serviço;
- outros custos formalmente previstos.

## 11. Mão de obra

Quando houver produtividade oficial:

`Horas = Quantidade × Coeficiente_de_mão_de_obra`

ou, quando a produtividade estiver expressa em unidades por hora:

`Horas = Quantidade / Produtividade`

Depois:

`Custo_MO = Horas × Valor_hora`

Separar as categorias existentes na tabela oficial, por exemplo:

- ajudante;
- profissional;
- encarregado.

Não criar valor-hora por inferência quando a tabela oficial não estiver disponível.

## 12. Composição de interligações

Uma interligação deve ser decomposta em seus componentes reais quando a documentação ou composição oficial assim exigir:

`Custo_interligação = materiais + mão_de_obra + equipamentos + demais componentes aplicáveis`

Exemplos de grupos a verificar:

- elétrica;
- hidráulica;
- esgoto;
- drenagem;
- nivelamento;
- mobilização;
- carro de apoio;
- Munck/içamento;
- transporte.

A distância, quantidade de pontos e demais parâmetros devem ser extraídos do escopo, layout, vistoria ou premissa registrada.

## 13. Modelo-base + excedentes

O preço do modelo-base deve permanecer separado dos acréscimos.

`Orçamento = Valor_modelo_base + Σ Excedentes + Σ Customizações + Σ Serviços adicionais`

Quando um modelo já possuir preço fechado, não recomputar seus componentes internos para alterar o preço-base, salvo solicitação explícita de análise de composição.

Exemplo:

`MLT.C06 + 3 tomadas + forração PIR 32 mm + bancada/pia + janela adicional`

O MLT.C06 permanece como produto-base. Somente os itens não contemplados na configuração-base entram como excedentes/customizações.

## 14. Referência cruzada entre modelos

Quando o Especialista indicar que uma configuração de outro modelo atende a uma necessidade, o ELO deve registrar a relação:

`modelo_solicitado → modelo_referência → componente/configuração reaproveitável`

A referência não autoriza copiar automaticamente o preço integral do outro modelo.

Deve-se identificar:

1. o que é equivalente;
2. o que não é equivalente;
3. o que é excedente;
4. quais interligações surgem;
5. quais parâmetros precisam de validação.

## 15. Área e dimensões dos módulos

As dimensões canônicas vigentes devem ser consultadas na base de produtos/modelos antes de qualquer cálculo dimensional.

Para o padrão informado atualmente:

| Tamanho | Comprimento | Largura | Altura | Área de referência |
|---|---:|---:|---:|---:|
| 20 pés | 6000 mm | 2440 mm | 3010 mm | 14,6 m² |
| 15 pés | 4500 mm | 2440 mm | 3010 mm | 11,0 m² |
| 10 pés | 3000 mm | 2440 mm | 3010 mm | 7,3 m² |
| 8,5 pés | 2600 mm | 2440 mm | 3010 mm | 6,3 m² |
| 8 pés | 2400 mm | 2440 mm | 3010 mm | 5,8 m² |
| 6 pés | 1800 mm | 2440 mm | 3010 mm | 4,4 m² |

**Nota:** a área útil interna de um modelo específico prevalece sobre a área geométrica externa de referência quando o cálculo for interno ao módulo. Exemplo registrado: MLT.M01 possui área útil interna atual de **13,63 m²**.

## 16. BDI

Quando a modalidade e a tabela vigente determinarem aplicação de BDI:

`Preço_com_BDI = Custo_base × (1 + BDI/100)`

As referências atualmente registradas no processo são:

- VENDA: BDI padrão da planilha de referência = 96,00%;
- LOCAÇÃO: BDI padrão da planilha de referência = 65,00%.

Esses percentuais não devem ser tratados como universais. O Especialista deve utilizar a tabela comercial vigente para a solicitação específica.

## 17. Administração

Quando houver taxa de administração prevista pela condição comercial:

`Valor_com_administração = base_conforme_regra_comercial`

A fórmula exata deve seguir a planilha/tabela comercial vigente. Não somar percentuais por hábito sem verificar a metodologia da tabela.

## 18. Arredondamento

Manter precisão suficiente durante as etapas intermediárias e arredondar conforme o padrão da planilha oficial somente na etapa definida para apresentação/fechamento.

Evitar arredondar cada parcela prematuramente quando isso provocar divergência no total.

## 19. Validações automáticas obrigatórias

Antes do fechamento, verificar:

- unidade incompatível;
- quantidade zero ou negativa sem justificativa;
- valor unitário ausente;
- fórmula sem parâmetro de origem;
- percentual aplicado duas vezes;
- item padrão lançado novamente como excedente;
- excedente incluído no preço-base e novamente na composição;
- modelo de referência tratado como modelo-base sem autorização;
- interligação omitida;
- mão de obra não separada quando exigida;
- composição sem rastreabilidade;
- diferença entre dimensão do modelo e dimensão utilizada no cálculo.

## 20. Aprendizado controlado

Quando uma nova forma recorrente de cálculo for identificada:

1. registrar a ocorrência;
2. identificar o contexto;
3. verificar se já existe regra equivalente;
4. avaliar impacto sobre outras composições;
5. propor nova regra ou melhoria;
6. submeter ao gate de governança do ELO;
7. somente após aprovação incorporar como regra canônica.

Experiência temporária não deve ser transformada automaticamente em regra permanente.

## 21. Regra de segurança

Se o cálculo puder ser realizado, mas faltar um parâmetro crítico, o Especialista deve apresentar:

- fórmula pretendida;
- parâmetro ausente;
- fonte esperada;
- impacto no orçamento;
- pergunta ou ação de vistoria necessária.

É preferível um cálculo pendente e rastreável a um valor estimado sem fundamento.

## 22. Relação com o ELO

O **ELO** audita as relações e a coerência do cálculo.

O **Especialista de Orçamento** executa os cálculos, composições e fechamento.

O ELO pode contestar:

- fórmula;
- parâmetro;
- origem;
- duplicidade;
- classificação;
- relação entre modelo e excedente;
- omissão de composição/interligação.

O Especialista deve responder à contestação com evidência e correção quando procedente.
