# Exemplo: upload de avatar com thumbnails e CDN

Exemplo fictício e deliberadamente curto, para calibrar o nível de detalhe. Tudo marcado como Suposição precisaria de confirmação com o time; nenhum fato aqui descreve um sistema real.

## 1. Escopo e ativos

- Dentro: upload de imagem de perfil por usuário autenticado, worker que gera thumbnails, armazenamento em bucket, entrega por CDN.
- Fora: login, perfil textual, moderação humana de conteúdo.
- Ativos: contas dos usuários, integridade do domínio do site (conteúdo servido na origem principal ou não), infraestrutura do worker, custo de armazenamento e processamento.
- Atores: usuário autenticado malicioso, usuário comum, visitante anônimo que carrega a página, terceiro que descobre a URL do bucket.

## 2. DFD textual

```text
E1 Usuário (navegador)        S1 Bucket de originais        S2 Bucket de thumbnails (atrás da CDN)
P1 API de upload              P2 Worker de thumbnails       E2 CDN
F1: E1 -> P1 | arquivo de imagem + metadados | HTTPS | sessão do usuário
F2: P1 -> S1 | arquivo original | credencial de serviço da API
F3: P1 -> P2 | evento "novo original" com chave do objeto | fila
F4: P2 -> S1 | leitura do original ;  F5: P2 -> S2 | escrita do thumbnail
F6: E2 -> S2 | leitura do thumbnail ;  F7: E1 <- E2 | thumbnail por URL pública
B1 internet | API (F1)      B2 API | armazenamento (F2, F5)      B3 conteúdo do usuário | worker (F4)
B4 armazenamento | CDN | internet (F6, F7)
Suposição S-1: a CDN serve os thumbnails de um domínio diferente do site principal.
Suposição S-2: o worker usa uma biblioteca de imagens do sistema, sem sandbox.
Suposição S-3: o nome do objeto no bucket é derivado do ID do usuário.
```

## 3. Tabela de ameaças (amostra)

| id | fluxo | ameaça | cat. | prob. | imp. | resposta | controle | teste |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | F1 | arquivo polyglot (imagem + HTML/JS) aceito pelo tipo declarado | T / I | Alta | Média | mitigar | tipo verificado pelo conteúdo (assinatura), reprocessar a imagem (re-encode), servir da origem separada (S-1) com `X-Content-Type-Options: nosniff` e `Content-Disposition` adequado | upload de `.html` renomeado para `.png` é recusado; resposta do thumbnail tem `nosniff` |
| T2 | B3 / F4 | arquivo malformado explora a biblioteca de imagens do worker (execução de código) | E | Média | Alta | mitigar | limites de dimensão, memória e tempo; worker com mínimo privilégio e isolado (container sem credenciais amplas); biblioteca atualizada | imagem de 30000x30000 é rejeitada por limite; worker sem acesso à rede interna |
| T3 | F1 | upload massivo esgota armazenamento ou custo | D | Alta | Média | mitigar | limite de tamanho por arquivo, cota por usuário, limite de taxa; descartar originais após processar (se o negócio permitir) | arquivo acima do limite recebe 413; N uploads por minuto recebem 429 |
| T4 | F2 / S-3 | usuário sobrescreve avatar de outro (ID do objeto vem do cliente) | T / E | Média | Alta | mitigar | chave do objeto gerada no servidor a partir da sessão; nunca do corpo da requisição | usuário B envia `userId` de A no corpo e o avatar de A permanece intacto (relê o recurso) |
| T5 | F7 / F2 | metadados EXIF com geolocalização vazam | I | Média | Média | mitigar | remover EXIF no re-encode | thumbnail gerado de foto com GPS não contém EXIF |
| T6 | F1 | upload sem registro: não se sabe quem enviou conteúdo ilegal | R | Baixa | Média | mitigar | log de auditoria com usuário, hash do arquivo e horário (sem o conteúdo) | após upload existe registro com autor e hash |
| T7 | S1 | URL ou listagem do bucket de originais pública por engano | I | Média | Alta | mitigar | bloquear acesso público no bucket; acesso só por credenciais de serviço | requisição anônima ao objeto original retorna 403 |

## 4. Risco residual e confirmações

- Residual: parser de imagem sempre pode ter vulnerabilidade desconhecida; mitigação é isolamento e atualização, não eliminação.
- Confirmar: S-1 (domínio separado da CDN), S-2 (worker isolado?), S-3 (como o nome do objeto é formado), política de retenção do original.
- Não coberto: moderação de conteúdo, direito autoral, privacidade da imagem em si (LINDDUN não aplicado neste exemplo).
- Próximo passo: transformar T1, T2, T4 e T7 em testes automatizados antes da implementação.
