# Sistema visual ELO Web — referência VEXIA ELO v8.0

Fonte visual: HTML fornecido pelo usuário nesta conversa. Implementação em `src/app/globals.css` e `src/components/elo-dashboard.tsx`. Este documento descreve a interface corporativa; não define autoridade de dados nem automações de produção.

## Direção

- Fundo azul-marinho `#0a1628`, painéis `#111d3a` e texto `#f0f4ff`.
- Ação corporativa: gradiente `#6c5ce7 → #0984e3`. Orquestrador: `#8b5cf6 → #3b82f6`.
- Estados: verde `#00b894`, amarelo `#fdcb6e`, vermelho `#e17055`, azul `#0984e3`.
- Cards translúcidos `rgba(255,255,255,.04)`, borda discreta, raio 12 px e controles de 8 px.
- Tipografia Inter com fallback system-ui. Tabelas densas, cabeçalho fixo e rolagem horizontal.
- Topo de 56 px com hexágono E, faixa horizontal de 12 áreas, ícones visíveis em telas estreitas.
- Subabas contornadas, modal para edição e revisão, Kanban horizontal e botão flutuante apenas no Orquestrador.
- Foco visível, navegação acessível por nome e transições reduzidas quando o sistema solicita.

## Áreas

| Área | Navegação | Ação visual principal |
| --- | --- | --- |
| Orquestrador | 🧠 | Analisar questão, insights, gargalos e simulação local |
| Dashboard | 📊 | KPIs, modelo e sazonalidade informados |
| Comercial | 💰 | Solicitações, sazonalidade de 12 meses e movimentação |
| Almoxarifado | 📦 | Estoque e pedidos de material |
| Compras | 🛒 | Pedidos e lead time |
| Produção | 🏭 | Kanban e serviços externos |
| Planejamento/PCP | 📋 | SO → Checklist → Orçamento → Revisão; Kanban, projetos e OF |
| Expedição | 🚚 | Expedição, quarentena e reparo |
| Catálogo | 📚 | Taxonomia, Lista Mãe, BOM e diretório |
| Chat | 💬 | Comunicação e comando revisado |
| Notificações | 🔔 | Alertas derivados |
| Configurações | ⚙️ | Integrações e backup local |

## Conteúdo e comportamento

As etiquetas e botões nas telas setoriais devem nomear tarefas corporativas. A marca ELO identifica o produto e o Orquestrador; termos internos de implementação não viram ações setoriais.

O HTML de referência contém usuários e senhas de demonstração, login Google simulado, chaves no cliente, números aleatórios, arquivos fictícios e automações que criam OF/Projeto automaticamente. Esses dados e comportamentos não são parte do sistema visual. A interface conserva valores vazios até entrada explícita, fonte, revisão e autorização. Orçamento é setor dentro de Planejamento/PCP.

## Componentes CSS

`.elo-header`, `.elo-hex`, `.elo-top-nav`, `.elo-nav-item`, `.elo-page`, `.elo-panel`, `.elo-kpi`, `.elo-badge`, `.elo-button`, `.elo-subtab`, `.elo-input`, `.elo-table`, `.elo-modal-overlay`, `.elo-modal`, `.elo-kanban`, `.elo-float`.

A prévia Vercel deve ser validada visualmente após autenticação; build isolado não comprova a experiência pós-login.
