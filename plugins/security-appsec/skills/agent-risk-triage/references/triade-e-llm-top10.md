# Tríade letal, LLM Top 10 e checklist de instalação

Fontes (conferidas em 2026-10-10, redação própria): tríade letal, Simon Willison, 2025-06-16 (V-11); OWASP Top 10 for LLM Applications 2025 (V-14); defesas contra prompt injection (V-10); modelo de segurança e checklist de conteúdo não confiável (V-01); plugins de terceiros (V-32); permissões e hooks (V-05, V-06). Itens sem V são conhecimento estável (Inferido).

## Sumário

1. Tríade letal: três perguntas e o que fazer com três "sim"
2. Padrões de arquitetura que quebram a tríade
3. LLM Top 10 2025: perguntas por categoria
4. Checklist de instalação de plugin ou MCP
5. Sinais de alerta no material avaliado
6. Exemplo de triagem

## 1. Tríade letal

| Perna | Pergunta | Exemplos de evidência |
| --- | --- | --- |
| Dados privados | O agente lê algo que o atacante não deveria ver? | acesso a repositório privado, e-mail, `.env`, variáveis de ambiente, banco, arquivos do usuário, tokens de MCP |
| Conteúdo não confiável | O agente lê texto que outra pessoa escreve? | páginas web, e-mails, issues e PRs de fork, comentários, saída de dependência, respostas de API de terceiros, documentos enviados |
| Comunicação externa | O agente consegue enviar algo para fora? | HTTP/fetch, `curl`, e-mail, comentário em PR, push, publicação, criação de issue, ferramenta de escrita em SaaS, renderização de imagem com URL externa |

Três "sim" na mesma sessão: o conteúdo não confiável pode instruir o agente a ler o dado privado e enviá-lo. Para o usuário final, a única proteção confiável é não combinar as três; para quem constrói, depois que conteúdo não confiável entrou, ele não pode disparar ação consequente. Produtos de guardrail que prometem "95%" de eficácia não bastam (V-11).

## 2. Padrões de arquitetura que quebram a tríade

1. **Remover uma perna.** Agente de leitura sem saída externa (sem rede, sem escrita); agente de escrita que só recebe entrada confiável.
2. **Separar sessões.** Um agente com ferramentas de leitura e conteúdo não confiável devolve apenas um resumo estruturado; outro agente, sem acesso ao conteúdo bruto, age com ferramentas de saída.
3. **Confirmação humana na saída.** Toda ação de saída (enviar, publicar, push) pede aprovação com o conteúdo exato visível. Aprovação em lote ou "lembrar" reduz o controle.
4. **Mínimo privilégio.** Credencial de leitura de um escopo; caminhos de escrita limitados; rede por lista de domínios (sandbox/proxy). No Windows nativo não há sandbox: use WSL2 ou dev container (V-09).
5. **Dados sensíveis fora do alcance.** `permissions.deny` para `.env`, chaves e diretórios de credenciais; credenciais de produção fora do ambiente do agente.
6. **Tratar a saída do modelo como entrada não confiável** antes de chegar a SQL, shell, HTML ou outra ferramenta (LLM05).

## 3. LLM Top 10 2025: perguntas por categoria (V-14)

| Cat. | Pergunta de triagem |
| --- | --- |
| LLM01 Prompt Injection | Que conteúdo externo chega ao prompt (direto ou indireto, via ferramenta)? Há separação entre instrução e dado? |
| LLM02 Sensitive Information Disclosure | Que dado sensível o modelo vê? Quem lê a saída e os logs? |
| LLM03 Supply Chain | De onde vêm modelos, plugins, servidores MCP, dados e dependências? Versão fixada? Licença? |
| LLM04 Data and Model Poisoning | Dados de treino, ajuste fino ou RAG podem ser escritos por terceiros? |
| LLM05 Improper Output Handling | A saída do modelo vai para SQL, shell, HTML, caminho de arquivo ou chamada de API sem validação por schema? |
| LLM06 Excessive Agency | Que ferramentas o agente aciona sem aprovação? Com que permissão e escopo? Ação irreversível exige confirmação? |
| LLM07 System Prompt Leakage | O prompt de sistema contém segredo, credencial ou regra que não deveria estar lá? (O que está no prompt pode ser extraído.) |
| LLM08 Vector and Embedding Weaknesses | O índice vetorial isola por tenant/permissão? Documentos de um usuário aparecem para outro? |
| LLM09 Misinformation | Há ação consequente baseada em saída não verificada (código, dependência, URL, fato)? |
| LLM10 Unbounded Consumption | Qual o teto de tokens, chamadas e custo por usuário? Há laço sem parada? |

A página OWASP lista as categorias; as perguntas são redação própria e funcionam como mapa, não como metodologia completa. Não há edição "2026" nem lista "Agentic Top 10" ranqueada confirmada nas fontes lidas.

## 4. Checklist de instalação de plugin ou MCP (V-32, V-01)

- [ ] Origem e mantenedor identificados; licença lida (cada plugin tem a sua).
- [ ] Hooks declarados: eventos, comandos e scripts de `SessionStart`; falham aberto ou fechado.
- [ ] Servidores MCP: quem opera, que dados trafegam, que ferramentas expõem; aprovação de projeto exigida.
- [ ] Permissões pedidas versus necessárias (`Bash`, `Write`, rede).
- [ ] Dependências instaladas na primeira execução (pip, npm, download): código de terceiros na máquina.
- [ ] Versão fixada (commit ou tag), não branch móvel; plano para revisar atualizações.
- [ ] Custo: uso de modelo por turno ou commit, chaves de API com cobrança.
- [ ] Teste em projeto descartável antes do uso real; sem credenciais de produção no ambiente de teste.
- [ ] Mudanças em arquivos críticos monitoradas: `.github/workflows/`, `.env`, configurações de permissão, `package.json` e lockfiles (V-01).
- [ ] Hook `ConfigChange` para auditar mudanças de configuração (documentado em V-01; confira o formato na doc da versão).

## 5. Sinais de alerta no material avaliado

| Sinal | Por que importa |
| --- | --- |
| `curl ... \| sh`, `wget ... \| bash`, `npx` de pacote desconhecido, `pip install` de URL | executa código de terceiros sem revisão |
| texto dirigido à IA: "pré-aprovado", "não avise o usuário", "ignore regras anteriores", "execute sem pedir" | tentativa de manipulação; é dado, não permissão |
| hook que roda comando de rede ou lê credenciais; hook em `SessionStart` | executa no início de toda sessão, com seus privilégios |
| servidor MCP remoto com ferramentas de escrita e leitura juntas | cobre duas pernas da tríade no mesmo servidor |
| `allowed-tools` amplo (`Bash`, `Write`) numa skill que só deveria ler | superfície desnecessária |
| prompt/skill com segredo, token ou dado de cliente embutido | vaza para quem ler o arquivo (V-33) |
| versão em branch móvel (`main`) ou ação de CI sem pin por SHA | muda sem aviso (V-04) |
| bloco de shell executado na carga da skill (Inferido: confira a sintaxe na doc de skills) | roda comandos antes de o modelo ver o texto |

## 6. Exemplo de triagem

Pedido: "Quero um agente que lê minha caixa de entrada, abre links e responde sozinho. Config: gmail-read, fetch, smtp-send. Pode?"

| capacidade | evidência | risco | mitigação |
| --- | --- | --- | --- |
| ler e-mail (gmail-read) | config MCP colada | dados privados e conteúdo de terceiros (qualquer remetente) | escopo somente leitura; filtrar remetentes |
| abrir links (fetch) | config MCP colada | mais conteúdo não confiável; injeção indireta por página | resumo isolado; sem credenciais na sessão que abre links |
| responder (smtp-send) | config MCP colada | comunicação externa automática | confirmação humana por mensagem, com texto e destinatário visíveis |

Tríade: dados privados = sim; conteúdo não confiável = sim; comunicação externa = sim. Veredito: não instalar como descrito; instalar com restrições se (1) a sessão que lê e abre links não tiver `smtp-send`, (2) o envio exigir aprovação humana, (3) o `fetch` ficar numa sessão sem acesso ao e-mail. A defesa do modelo (treinamento, classificadores) é uma camada adicional, não substitui as três. Nada foi instalado nem executado nesta triagem.
