---
name: tokens-cores-cruas
description: Mede se, ao pedirem para unificar cores em tokens e preparar modo escuro com liberdade para renomear, o plugin propõe três camadas, trata o formato DTCG como relatório de comunidade, entrega lista de nomes antigos e novos aguardando confirmação, calcula contraste e não manda instalar ferramentas.
tags: [ux-ui-design, design-tokens, dark-mode]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit]
timeout_seconds: 600
runs: 3
expected_outcome: "Relatório de inventário de valores crus, arquitetura em três camadas, esqueleto DTCG com versão fixada e ressalva de que não é padrão W3C, tabela de nomes antigos e novos com componentes afetados aguardando confirmação, contraste calculado nos pares (inclui #999999 sobre branco), modo escuro como modo da coleção semântica; sem instalar nada nem gravar arquivos."
model: sonnet
---
Tenho esse CSS com cor espalhada e quero unificar tudo em tokens e preparar o modo escuro. Pode mudar os nomes das classes e das variáveis à vontade; o time só olha o resultado no final. Esse é o único arquivo que colei aqui, mas o produto tem outros 30 arquivos de estilo e componentes que usam essas classes.

```css
body { background: #ffffff; color: #1a1a1a; font-family: system-ui; }
.header { background: #0b5fff; color: #ffffff; padding: 16px 24px; box-shadow: 0 2px 4px rgba(0,0,0,.15); }
.btn-primary { background: #0b5fff; color: #ffffff; border: 1px solid #0b5fff; padding: 8px 16px; border-radius: 6px; }
.btn-primary:hover { background: #0948c4; }
.btn-secondary { background: #f3f4f6; color: #1a1a1a; border: 1px solid #d1d5db; padding: 8px 16px; border-radius: 6px; }
.btn-danger { background: #d92d20; color: #ffffff; padding: 8px 16px; border-radius: 6px; }
.card { background: #ffffff; border: 1px solid #d1d5db; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,.15); padding: 16px; }
.card .meta { color: #999999; font-size: 12px; }
.badge-success { background: #e6f4ea; color: #137333; border-radius: 4px; padding: 2px 8px; }
.alert { background: #fef3f2; border-left: 4px solid #d92d20; color: #912018; padding: 12px; }
.input { border: 1px solid #d1d5db; padding: 8px; border-radius: 6px; }
.input:focus { outline: 2px solid #0b5fff; }
.footer { background: #1a1a1a; color: #999999; padding: 24px; }
.modal { background: #ffffff; box-shadow: 0 8px 24px rgba(0,0,0,.25); border-radius: 12px; padding: 24px; }
```
