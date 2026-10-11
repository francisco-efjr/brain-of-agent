# Handoff / checkpoint da sessão

Uso: fim de sessão, mudança de agente, ou antes de compactar o contexto. Fatos, não narrativa. Registre decisões exatas, problemas resolvidos, opções descartadas, estado atual e pendências difíceis de reencontrar. Estilo do brain-of-agent (MIT) adaptado a lojas.

- Projeto/loja: [NOME] · Plataforma e versão: [X] · Ambiente: [teste | dev | live] · Data: [AAAA-MM-DD] · Modo: [normal | ECOMMERCE-COMPLETO pedido pelo usuário]

## 1. Entregue
| Artefato | Caminho | O que contém |
| --- | --- | --- |
| [ARQUIVO] | [CAMINHO] | [RESUMO] |

## 2. Verificado, Inferido, Suposição, Não verificável
| Afirmação | Rótulo | Evidência (comando e saída essencial, arquivo:linha) |
| --- | --- | --- |
| [AFIRMAÇÃO] | Verificado | `[comando]` → [saída] |
| [AFIRMAÇÃO] | Inferido | [análise] |
| [AFIRMAÇÃO] | Não verificável | [motivo: sem acesso/credencial/norma] |

## 3. Decisões e opções descartadas
- Decisão: [X] porque [MOTIVO] · Descartado: [OPÇÃO] porque [MOTIVO]

## 4. Pendências
- [ ] [AÇÃO] — dono: [NOME] — bloqueio: [X]

## 5. Riscos
- [RISCO] — severidade — mitigação

## 6. Efeitos externos
- Nenhum efeito real (cobrança, reembolso, etiqueta, nota fiscal, publicação, escrita em produção) foi executado: [CONFIRMADO | EXCEÇÕES AUTORIZADAS: LISTA]

## 7. Próximo passo
- [UMA AÇÃO CONCRETA]

## 8. Retomar
- Comando de verificação: `[COMANDO]` · Arquivo de progresso: [CAMINHO] · Contexto mínimo para reler: [ARQUIVOS]
