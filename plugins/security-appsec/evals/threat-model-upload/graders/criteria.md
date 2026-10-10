---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega o documento completo na mesma resposta, sem encerrar com perguntas bloqueantes; usa o status rascunho (ou equivalente) e lista perguntas ou lacunas em uma seção do tipo "Decisões pendentes do humano" ou "Suposições a confirmar".
2. Apresenta um DFD em texto com processos, armazenamentos, entidades externas, fluxos e pelo menos 3 fronteiras de confiança (por exemplo cliente para API, API para bucket, worker para CDN pública ou usuário para usuário via perfil público).
3. Aplica as seis categorias STRIDE aos fluxos que cruzam fronteira, com ameaças específicas do upload (por exemplo arquivo trocado entre upload e processamento, arquivo malicioso explorando o parser de imagem, SVG ou HTML servido como imagem, EXIF com localização, URL de CDN previsível ou pública, custo ou DoS por arquivos grandes).
4. Entrega tabela com probabilidade, impacto, resposta (mitigar, eliminar, transferir ou aceitar), controle concreto e teste de verificação por ameaça; transferir ou aceitar vem com risco residual.
5. Marca como Suposição o que não foi descrito (por exemplo método de autenticação, política do bucket, quem pode ver o perfil, validação já existente) e não afirma esses itens como fatos.
6. Trata o cliente web e o app Android como controlados pelo atacante (validação repetida no servidor) e, para detalhes específicos de Android, indica o que muda ou aponta o plugin de mobile (`/mobile-apps:playbook`), sem inventar detalhes de plataforma.
7. Não afirma ter executado testes, ferramentas ou lido arquivos do repositório.
FAIL if qualquer um ocorrer: lista genérica do OWASP sem DFD; afirma fatos de arquitetura que o usuário não descreveu; para e pede respostas sem entregar o modelo; ameaças sem resposta e sem teste; atribui conformidade ou score numérico.
