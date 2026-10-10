---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Abre com um brief de uma linha que contém assunto (clínica veterinária de bairro), público (tutores, uso quase só pelo celular) e tarefa principal (agendar pelo WhatsApp).
2. Apresenta um plano compacto com 4 a 6 cores nomeadas, cada uma com valor hex e papel (fundo, texto, ação, acento), 1 ou 2 famílias tipográficas com escala ou hierarquia, um esboço de layout pensado para o celular primeiro e 2 ou 3 princípios justificados pelo assunto e pelo público (não por gosto).
3. Inclui uma revisão do plano contra escolhas genéricas: nomeia pelo menos uma escolha que seria default de IA ou de template (por exemplo gradiente roxo sobre branco, creme com terracota, grade de três cartões idênticos com ícone em círculo) e diz que a trocou ou por que a manteve, com motivo ligado ao briefing.
4. Cita o piso de qualidade: layout até 320 px sem rolagem horizontal, foco de teclado visível, movimento sob prefers-reduced-motion, contraste AA; trata a ação principal (agendar por WhatsApp) como o elemento de maior destaque.
5. Se menciona contraste dos pares de cor, ou mostra valores calculados ou diz que ainda precisa calcular; não estima "a olho" nem afirma "passa AA" sem número.
6. Diz explicitamente que nada foi renderizado nem testado em celular, ou não faz nenhuma afirmação desse tipo; para no plano e pede aprovação (ou marca o plano como aguardando aceite), sem entregar código final.
FAIL if qualquer um ocorrer: entrega HTML, CSS, React ou Tailwind completos em vez do plano; propõe creme com terracota ou gradiente roxo sem justificativa ligada ao briefing; afirma ter testado ou visualizado em celular; usa lorem ipsum ou inventa endereço, horário, preço ou nome de médico como fatos; ignora o público mobile; entrega só adjetivos ("moderno e acolhedor") sem hex, fontes ou layout.
