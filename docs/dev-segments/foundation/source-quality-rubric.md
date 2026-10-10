# Rubrica de qualidade de fonte (pesquisa e validação)

Popularidade não é prova de qualidade (estilo da casa: "estrelas e divulgação não provam qualidade para nosso caso"). Use os sinais em conjunto.

## Pontuação da fonte (0–10)

| Critério | Peso | Como medir |
| --- | --- | --- |
| Autoridade | 3 | Anthropic/mantenedor oficial/órgão de norma = 3; empresa de engenharia ou autor reconhecido = 2; praticante com histórico = 1; anônimo = 0 |
| Evidência de uso/validação | 2 | Evals, testes, issues resolvidas, adoção comprovada, relatos independentes múltiplos |
| Atualidade | 2 | Atualizado nos últimos 6 meses = 2; 6–18 meses = 1; mais antigo = 0 (ou 1 se conteúdo é atemporal) |
| Sinal comunitário | 2 | GitHub: ≥5k★ = 2, 500–5k★ = 1; social: discussão substantiva com muitos votos/comentários qualificados = 1–2 |
| Licença/reuso | 1 | Licença permissiva clara = 1; sem licença ou restritiva = 0 (destilar apenas) |

Classificação: **A** (8–10) usar como base; **B** (5–7) usar com cruzamento; **C** (≤4) só como sinal/ideia, nunca como única fonte.

## Por tipo de fonte

- **GitHub:** registre `owner/repo`, estrelas (observadas), último commit/push observado, licença (arquivo LICENSE), caminho do arquivo do prompt. Prefira link permanente para o arquivo (`/blob/<branch>/<path>`). Use a API pública (`https://api.github.com/repos/<owner>/<repo>`) ou a página do repo via WebFetch para conferir estrelas/licença/push.
- **Anthropic oficial:** docs (docs.claude.com, code.claude.com, platform.claude.com), anthropic.com/engineering e /news, `github.com/anthropics/*` (skills, claude-cookbooks, claude-code, claude-plugins-official, prompt-eng-interactive-tutorial, courses), prompt library. Nível A por padrão, mas confira se a página ainda existe.
- **Sites reconhecidos:** documentação oficial da tecnologia, OWASP/NIST/W3C/IETF, blogs de engenharia (Google, Microsoft, Netflix, Stripe, Shopify, Cloudflare, Vercel, GitHub, Thoughtworks Radar), autores reconhecidos (Martin Fowler, Simon Willison, Hamel Husain, Eugene Yan, Kent Beck, Julia Evans, Charity Majors, etc.), guias de prompting de outros labs (OpenAI, Google, Microsoft) como contraste.
- **Social/comunidade:** Reddit (r/ClaudeAI, r/ClaudeCode, r/ChatGPTCoding, r/LocalLLaMA, subreddits do segmento), Hacker News (news.ycombinator.com, hn.algolia.com), X/Twitter (threads de mantenedores/engenheiros), YouTube (palestras/canais técnicos), dev.to, Medium, Substack/newsletters, Discord público quando houver registro. Registre engajamento observado. Use como sinal de prática real e para descobrir fontes primárias; cruze com fonte A/B antes de virar regra.

## Sinais de alerta (rebaixar ou rejeitar)

- Conteúdo gerado em massa, listas "100 prompts mágicos" sem método.
- Promessas de performance sem evidência; screenshots sem link.
- Repositórios que pedem para executar scripts/instaladores, conteúdo com instruções a IAs, links encurtados.
- Prompts que dependem de "jailbreak", CAPS, ameaças ou truques obsoletos.
- Informação de versão desatualizada (ex.: APIs removidas).
