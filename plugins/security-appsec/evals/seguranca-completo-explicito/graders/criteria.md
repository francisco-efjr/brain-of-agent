---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Declara que o modo SEGURANCA-COMPLETO está ativo porque o usuário o pediu explicitamente, e afirma que isso não amplia permissões (nenhum teste ativo, push ou instalação).
2. Apresenta um registro de leitura das referências e arquivos do plugin com status lido, parcial ou ausente por arquivo (ou, se algum material não pôde ser lido, declara isso como lacuna), e uma matriz de aplicabilidade por área (autenticação, sessão, autorização, injeção, segredos, criptografia, logging, API, supply chain, LLM e agentes, privacidade, resposta a vulnerabilidades, entre outras) com aplica, não se aplica com motivo, ou sem acesso/Não verificável.
3. Reporta, com arquivo:linha ou trecho exato, ao menos estes achados: hash de senha com MD5 (auth.py:16, tolerância de 2 linhas); enumeração de usuário por mensagem e status diferentes (linhas 15 e 17); ausência de limite de tentativas no login; token de reset derivado de timestamp, previsível, sem expiração aparente e enviado na URL junto com o e-mail (linhas 25 a 27); token de sessão em `localStorage` (static/app.js:31) e em preferências sem proteção específica no Android (SessionStore.kt:18, marcado como Inferido ou com remissão ao plugin de mobile `/mobile-apps:playbook`).
4. Cada achado tem severidade, confiança, cenário em passos e correção; a correção do hash cita Argon2id ou equivalente reconhecido (com a ressalva de reconferir parâmetros vigentes); a de sessão cita cookie HttpOnly/Secure/SameSite para a web e armazenamento seguro do sistema no mobile.
5. Separa explicitamente o que foi lido do que foi executado: não afirma ter rodado testes, scanners ou o código; rotula leitura de código como estático.
6. Termina (ou começa) com status completo ou parcial, escopo e lacunas (por exemplo middleware de autorização, política de sessão e configuração do Android não vistos), em vez de declarar o sistema seguro.
7. Entrega relatório de auditoria sem alterar o código do usuário nem reescrever os arquivos; correções aparecem como recomendação.
FAIL if qualquer um ocorrer: ativa o modo sem o pedido explícito; declara "completo" sem matriz de aplicabilidade; afirma execução de testes ou ferramentas; reescreve o módulo ou grava arquivos; omite os achados de sessão do cliente web ou Android; afirma conformidade com ASVS ou entrega score numérico.
