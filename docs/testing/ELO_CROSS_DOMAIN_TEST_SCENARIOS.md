# ELO — Cenários de Teste Cross-Domain

## Finalidade

Transformar a governança cross-domain em comportamento falsificável antes de qualquer promoção ao Core.

## Cenários

### CD-01 — Comercial → Orçamento
Uma condição comercial deve poder ser relacionada à premissa de orçamento preservando origem e período.

**Esperado:** PASS quando a relação é reconstruível e a origem permanece COMERCIAL.

### CD-02 — Licitação → Orçamento
Um requisito de edital deve ser relacionado a item/custo do orçamento.

**Esperado:** PASS com proveniência do requisito e cobertura identificável.

### CD-03 — Licitação ≠ Comercial
Um requisito de edital não pode ser classificado automaticamente como premissa comercial.

**Esperado:** separação de domínio preservada.

### CD-04 — Orçamento → Projeto
Uma adaptação orçamentária deve apontar para a solução técnica correspondente quando houver evidência.

### CD-05 — Projeto → Produção
Uma alteração técnica deve produzir relação rastreável com o impacto produtivo, quando houver evidência operacional.

### CD-06 — Compras → Produção
Um atraso de aquisição deve poder aparecer como restrição produtiva sem alterar a origem do evento.

### CD-07 — Produção → Logística
Conclusão produtiva deve poder liberar ou condicionar uma etapa logística quando o contrato operacional existir.

### CD-08 — Resultado → Aprendizado
Um desvio observado deve gerar candidato a aprendizado, nunca regra automática.

### CD-09 — Tenant isolation
Uma relação cross-domain entre tenant A e tenant B deve ser bloqueada.

### CD-10 — Temporalidade
Uma relação expirada não pode ser usada como vigente sem indicação explícita.

### CD-11 — Conflito de fonte
Documento vigente e histórico divergente devem produzir conflito explícito e priorização pela autoridade definida.

### CD-12 — Proveniência ausente
Uma relação sem evidência suficiente deve ser marcada como incerta/pendente e não como fato consolidado.

### CD-13 — Provider externo
Resposta externa pode complementar análise, mas não pode redefinir domínio, tenant, identidade ou autoridade canônica.

### CD-14 — Cadeia completa
Demonstrar reconstrução de:

`TR/EDITAL → requisito → solução → modelo → quantidade → excedente → orçamento → projeto → compra → produção → entrega → resultado`

**Critério:** cada transição precisa ter relação identificável, proveniência e estado de confiança.

## Classificação

Cada cenário deve terminar como:

- PASS — evidência executada e comportamento correto;
- FAIL — comportamento incorreto;
- UNKNOWN — informação insuficiente para concluir;
- BLOCKED — dependência de infraestrutura/contrato ausente;
- DEFINED — cenário ainda não executado.

Documentação isolada nunca converte DEFINED em PASS.
