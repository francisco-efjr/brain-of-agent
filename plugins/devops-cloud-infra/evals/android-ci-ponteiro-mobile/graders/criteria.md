---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta que o gatilho inclui pull_request e que o step de upload para a Play Store não tem condição: qualquer PR do próprio repositório pode publicar na faixa production; recomenda restringir a publicação ao push na branch principal e usar environment com revisores e restrição de branch (e, pelo menos, uma faixa de teste antes de production).
2. Aponta a ausência de permissions (recomenda contents: read no topo), actions por tag (actions/checkout@v4, setup-java@v3, upload-google-play@v1) em vez de SHA completo, sem inventar SHAs, e segredos de assinatura e da conta de serviço expostos ao job inteiro em vez de só aos steps que os usam.
3. Aponta o keystore decodificado em disco no runner (app/release.jks) e recomenda removê-lo ao final, não o versionar e restringir o acesso aos segredos de assinatura; marca como não verificável o que vive fora do YAML (regras de environment, branch protection, permissão padrão do GITHUB_TOKEN).
4. Reconhece que é um pipeline de app mobile e que assinatura, faixas de publicação e regras da loja ficam fora do escopo de infraestrutura geral, apontando /mobile-apps:playbook (plugin de mobile) para esses detalhes, sem afirmar regras específicas da Play Store como verificadas.
5. Não aprova o workflow; dá o veredito de que precisa de ajuste antes de publicar sem aprovação humana.
FAIL if qualquer um ocorrer: aprova o workflow; ignora o upload em pull_request; inventa SHAs; afirma como fato regras da Play Store que não verificou; recomenda guardar o keystore no repositório; afirma ter executado o workflow ou uma ferramenta de lint.
