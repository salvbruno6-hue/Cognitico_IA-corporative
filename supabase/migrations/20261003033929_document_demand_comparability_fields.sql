COMMENT ON COLUMN public.mt_pedidos_venda.natureza_demanda IS
'Classificacao da natureza da demanda comercial. Deve ser usada para separar bases comparaveis (por exemplo EVENTO, SPOT e SAZONALIDADE), sem converter a natureza em demanda humana.';

COMMENT ON COLUMN public.mt_pedidos_venda.chave_comparabilidade IS
'Identificador semantico usado pelo PCP para localizar a referencia historica equivalente da demanda. Nao deve ser preenchido por inferencia.';

COMMENT ON COLUMN public.mt_demanda_historico.natureza_demanda IS
'Natureza da demanda observada no periodo historico. Deve preservar a mesma taxonomia utilizada na previsao futura para permitir comparacao.';

COMMENT ON COLUMN public.mt_demanda_historico.chave_comparabilidade IS
'Chave da dimensao historica que precisa corresponder a previsao futura. Para EVENTO e SPOT, a ausencia impede comparabilidade automatica.';

COMMENT ON COLUMN public.mt_previsoes_demanda.natureza_demanda IS
'Natureza da demanda prevista. Deve reproduzir a estrutura que o Comercial deseja prever e ser comparavel ao historico equivalente.';

COMMENT ON COLUMN public.mt_previsoes_demanda.chave_comparabilidade IS
'Chave da dimensao futura que identifica a referencia historica equivalente. Para EVENTO e SPOT, deve existir quando a comparabilidade depender de evento/ocorrencia especifica.';
