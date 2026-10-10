# Checklist de entrega de UI

Marque cada item com [x] e cole a evidência ao lado; item sem evidência fica como "Não verificado". Origem: checklist de `frontend-e-estado.md` e de `apple-design.md` do brain-of-agent (MIT), adaptado. Entrega: [nome], data: [AAAA-MM-DD].

## Nove itens (toda tela ou fluxo)

- [ ] 1. Estado mapeado: fonte de verdade, URL e transições. Evidência: [lista de estados]
- [ ] 2. Vazio, carregando, falha, recuperação, sessão expirada e conteúdo longo cobertos. Evidência: [capturas ou testes]
- [ ] 3. Resposta obsoleta, duplo envio e perda de rascunho protegidos (e o servidor trata duplicação). Evidência: [teste ou `arquivo:linha`]
- [ ] 4. Semântica, foco, nomes acessíveis e feedback de operação. Evidência: [roteiro de teclado, axe]
- [ ] 5. Regras confirmadas no servidor; a UI não é fronteira de autorização. Evidência: [`arquivo:linha`]
- [ ] 6. Componentes compartilhados e tokens revisados antes de introduzir variação. Evidência: [busca no código]
- [ ] 7. Responsividade (320 px), zoom 200%, temas e preferência de movimento. Evidência: [capturas]
- [ ] 8. Carregamento e interação medidos com condições registradas. Evidência: [orçamento de performance]
- [ ] 9. Contrato real e jornada revalidados após mudar estado ou endpoint. Evidência: [reexecução]

## Aceite de acabamento (12 itens)

- [ ] Plataforma, stack e versão mínima confirmadas
- [ ] Funções originais preservadas e mapa de alterações disponível
- [ ] Comandos e atalhos implementados, não apenas desenhados
- [ ] Todos os estados relevantes têm comportamento e teste
- [ ] Tokens, tipografia e densidade seguem o produto e a plataforma
- [ ] Navegação por teclado e foco avaliados no fluxo
- [ ] Preferências e tecnologias assistivas pertinentes verificadas
- [ ] Temas e fundos reais não destroem a legibilidade
- [ ] Redimensionamento, overflow e dados extremos não quebram a tarefa
- [ ] Falha e recuperação preservam informações e evitam ação duplicada
- [ ] Persistência, segurança e performance não foram inferidas de screenshots
- [ ] Limitações de protótipo e medições não realizadas estão explícitas

## Comandos de verificação (saída desta sessão)

| Comando | Resultado | Saída ou caminho do artefato |
| --- | --- | --- |
| [typecheck] | [passou / falhou / não executado] | [saída] |
| [lint] | | |
| [teste] | | |
| [build] | | |
| [e2e] | | |

## Falhas comuns a conferir

Screenshot bonita sem o fluxo funcionando; toast como único registro de erro; skeleton infinito; índice de array como identidade de entidade mutável; cache do usuário anterior após logout.
