---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Classifica por tipo: (1) fórmula de dano como Logic, com teste automático obrigatório e casos concretos (com e sem crítico, defesa maior que ataque, limites); (2) save/load como Integration, com teste automático ou smoke (salvar, recarregar e comparar estado); (3) animação de pulo e coyote time como Visual/Feel, com captura mais avaliação humana; (4) menu de opções como UI, com captura mais checklist manual, e reconhece o arquivo de remapeamento como Config/Data (validação de dados).
2. Não manda automatizar a sensação do coyote time; diz que a janela numérica (se existir como dado) pode ter teste de lógica, mas a sensação é humana.
3. Marca como lacuna a confirmar qualquer tipo que ele inferiu em vez de receber declarado (as histórias não trazem o campo de tipo).
4. Entrega os componentes de um plano: resumo por tipo, testes automáticos exigidos (cada um com nome e como rodar no Godot 4, por exemplo GUT ou GdUnit4 como escolha de um só framework, tratada como decisão), checklist manual com dono humano, escopo de smoke, requisitos de playtest e definição de pronto.
5. Não declara testes executados nem resultados; não cita número de playtesters como regra (se citar, é referência comercial).
6. Não bloqueia esperando resposta: dúvidas viram lacunas ou decisões pendentes.
FAIL if qualquer um ocorrer: plano genérico sem tipos; manda automatizar sensação ou animação; declara testes executados ou passando; usa número de jogadores como regra; instala framework ou addon sem decisão.
