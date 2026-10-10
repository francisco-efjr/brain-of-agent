# Plano de design: [tela, fluxo ou produto]

Template T-01. Uso: antes de construir UI nova ou redesenho, e como insumo para `ui-designer` e para o plugin de frontend. Preencha em texto, sem código. Marque cada decisão sem fonte como Suposição. Marca, tokens e `DESIGN.md` existentes vencem qualquer escolha abaixo.

## 1. Brief e superfície

- **Brief em uma linha:** [assunto] para [público], para que [tarefa principal].
- **Superfície:** [Persuade | Operate | Read | Experience]; se híbrido, por seção: [seção → modo].
- **O que a pessoa deve lembrar depois de usar** (uma frase): [___]
- **Plataforma e stack:** [web | iOS | Android]; [framework e biblioteca de componentes].
- **Fontes de verdade encontradas:** [DESIGN.md, tokens, componentes, guia de voz] ou "nenhuma encontrada".
- **Restrições:** [acessibilidade (padrão: WCAG 2.2 AA), idioma, marca, prazo].

## 2. Tokens propostos

| Papel | Token | Valor | Contraste (par e razão calculada) |
| --- | --- | --- | --- |
| Texto principal | `color.text.default` | [#______] | [com fundo: __:1] |
| Fundo | `color.surface.default` | [#______] | n/a |
| Ação primária | `color.action.primary` | [#______] | [texto sobre ela: __:1] |
| Acento / destaque | `color.accent` | [#______] | [__:1] |
| Feedback (erro, aviso, sucesso) | `color.feedback.*` | [#______] | [__:1 cada] |
| Tipografia | família(s) e escala | [1 ou 2 famílias; corpo ≥ 16 px; medida < 80 caracteres] | n/a |
| Espaçamento | escala | [base 4 ou 8] | n/a |
| Raio e elevação | | [hierarquia, não raio uniforme] | n/a |
| Movimento | | [no máximo um momento orquestrado; só transform/opacity; sob prefers-reduced-motion] | n/a |

Regra: 4 a 6 cores nomeadas com hex e papel; contraste **calculado** pela fórmula WCAG, não estimado.

## 3. Layout

[Esboço em texto ou ASCII só para comparar alternativas; ponto de entrada, fluxo do olhar, zona primária; comportamento em 320, 768 e 1440 px.]

## 4. Estados obrigatórios

| Componente ou tela | Vazio | Carregando | Erro | Texto longo | Mobile 320 px | Foco/teclado |
| --- | --- | --- | --- | --- | --- | --- |
| [___] | [ação] | [forma do esqueleto] | [mensagem] | [truncar/quebrar] | [ok/ajuste] | [ordem de foco] |

## 5. Princípios (2 ou 3, justificados pelo assunto)

1. [princípio] porque [razão ligada ao assunto ou ao público].

## 6. Revisão contra o genérico

| Escolha que coincide com um padrão genérico | Decisão | Por quê |
| --- | --- | --- |
| [ex.: grade de três cartões com ícone] | [mudei X, ou mantive porque o briefing pede Y] | [razão] |

Pergunta de fechamento: alguém adivinharia este visual só pela categoria do produto? [sim/não e o que mudou]

## 7. Acessibilidade e plataforma

Alvo: [WCAG 2.2 AA]. Alvos de toque: [≥ 24 px CSS; meta 44]. Foco visível, reflow em 320 px, movimento reduzido: [como serão atendidos]. Convenções de plataforma: [___].

## 8. Suposições e decisões em aberto

- [Suposição ou decisão que o usuário precisa confirmar]

## 9. Gate

[Redesenho amplo: aguardando aprovação. Ajuste pequeno: segue, com as suposições acima registradas.]

---

## Exemplo preenchido (ilustra o formato; a marca real do projeto vence)

- **Brief:** landing de clínica veterinária de bairro para tutores de cães e gatos que chegam pelo celular, para que agendem consulta pelo WhatsApp.
- **Superfície:** Persuade. **Lembrar:** "dá para marcar em dois toques e eles cuidam do meu bicho".
- **Tokens:** texto `#1A1C1E` sobre `#FFFFFF` (17,09:1); ação `#0F766E` com texto `#FFFFFF` (5,47:1); superfície de apoio `#E6F4F1` com texto `#1A1C1E` (15,12:1); aviso `#B45309` sobre branco (5,02:1); erro `#B42318` sobre branco (6,57:1). Tipografia: títulos em grotesca com personalidade (por exemplo Bricolage Grotesque) e corpo em sans legível (por exemplo Source Sans 3), a confirmar licença e carregamento; corpo 17 px, medida 62 caracteres.
- **Revisão contra o genérico:** troquei a grade de três cartões com ícone em círculo por uma lista de serviços com preço de consulta fornecido pelo cliente; mantive o CTA único "Agendar pelo WhatsApp"; removi o carrossel de depoimentos (sem depoimentos reais).
- **Suposições:** tom caloroso e direto (sem guia de voz); horário de funcionamento a informar pelo cliente.
