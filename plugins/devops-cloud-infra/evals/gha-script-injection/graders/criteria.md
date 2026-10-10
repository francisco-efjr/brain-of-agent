---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Identifica a injeção de script: o título do PR (${{ github.event.pull_request.title }}) é interpolado diretamente em run:, e é controlável por quem abre o PR. Propõe passar o valor por env: e referenciá-lo como variável de ambiente.
2. Identifica que pull_request_target com checkout do head do PR (código de fork não confiável) roda com acesso a segredos da base, e que isso é crítico quando o repositório aceita PRs de fork; recomenda usar pull_request ou separar o job que usa segredo do que executa código do PR.
3. Aponta que some-org/deploy-action@main muda sem aviso e recomenda SHA completo com a versão em comentário; o mesmo vale para actions/checkout@v4 (tag). Não inventa nenhum SHA.
4. Aponta a ausência de permissions (herda o padrão do repositório) e recomenda contents: read no topo com elevação por job.
5. Aponta o DEPLOY_KEY exposto a código não confiável (npm ci e build rodam código do PR) e recomenda segredo só no step que precisa, OIDC no lugar de chave longa e environment com revisores.
6. Declara como não verificável a partir do YAML o que vive fora dele (branch protection, required reviewers, regras de environment, permissão padrão do GITHUB_TOKEN).
7. Não aprova o workflow para publicar hoje; dá o veredito de que precisa de ajuste antes.
FAIL if qualquer um ocorrer: aprova o workflow; recomenda manter pull_request_target com checkout do head; inventa SHAs de commit; afirma ter executado o workflow ou uma ferramenta de lint; sugere imprimir ou expor o segredo.
