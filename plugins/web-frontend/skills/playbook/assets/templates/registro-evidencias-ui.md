# Registro de evidências de UI

Uma linha por verificação. O objetivo é impedir o relato do que se esperava que acontecesse: cada entrada traz o comando ou roteiro, a saída real e o caminho do artefato. Base: `registro-evidencias-qa.md` do brain-of-agent (MIT) e a nota de verificação de V-37, adaptados. Não registre segredos nem dados pessoais; use dados fictícios.

| ID | Data | Ação ou roteiro | Comando | Saída real (resumo ou trecho) | Artefato (caminho) | Status | Limitação |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EV-01 | [AAAA-MM-DD] | [o que foi feito] | [comando literal ou "manual"] | [o que foi observado] | [captura, trace, JSON] | [Verificado / Inferido / Não verificado / Falhou / Não executado] | [alcance da conclusão] |

Status: **Verificado** só com comando ou captura gerados nesta sessão; **Inferido** para leitura de código ou comportamento não observado; **Não verificado** quando faltou ambiente, navegador ou acesso; **Falhou** com a saída da falha.

## Execução detalhada (quando a linha da tabela não basta)

- ID: [EV-nn] · Tentativa: [n] · Ambiente: [navegador e versão, viewport, tema, build]
- Estado inicial: [dados e rota]
- Esperado e fonte do oráculo: [resultado observável e de onde vem]
- Obtido: [resultado]
- Artefatos: [capturas em 320 px e desktop, console, trace, vídeo]
- Alcance da conclusão: [o que isto prova e o que não prova]

## Nota de verificação (sequência de cinco passos)

1. Rodar a suíte existente e registrar a saída. 2. Escrever o teste que falha. 3. Implementar. 4. Verificar a tela no navegador (captura em 320 px e desktop, console sem erros novos) e registrar a nota. 5. Promover a verificação a teste permanente.

## Mudança e revalidação

- Achado original: [ID]
- Correção e revisão: [arquivos ou commit]
- Revalidação: [casos e resultados]
- Evidências invalidadas por mudança posterior: [lista] e o que foi repetido
- Pendências: [o que falta]
