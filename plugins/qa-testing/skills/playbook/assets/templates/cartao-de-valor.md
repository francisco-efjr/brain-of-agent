# Cartão de valor e cartão de aposentadoria

Como usar: o **cartão de valor** justifica um teste proposto; o **cartão de aposentadoria** justifica remover ou reescrever um teste existente. Cartão incompleto = candidato não pronto. Relatório somente leitura até aprovação por lote; nenhum commit ou push automático. Inspirado nos fluxos `qa-only` e `test-audit` do gstack (Garry Tan, MIT), com redação própria.

## Cartão de valor (teste novo)

- **Protege o quê:** <comportamento e dano>
- **Falha quando:** <a regressão realista que o derruba>
- **Por que é novo:** <por que a cobertura atual não pega; rejeite o que já está coberto>
- **Seam:** <`none` ou nome do ponto de produção necessário; se nenhum chamador de produção o usa, teste na fronteira real>

## Cartão de aposentadoria (teste candidato a remoção)

- **Teste:** <arquivo e nome>
- **O que detecta:** <...>
- **Chamadores fora de teste:** <quem usa o código que ele cobre>
- **Comando de busca:** `<comando>` (exclusões e contagem registradas)
- **Prova mais forte que o substitui:** <teste na fronteira dona ou contrato>
- **Histórico:** <`git log --follow`: quando e por que nasceu; já falhou?>
- **O que libera:** <linhas de teste e de produção removíveis, separadas>
- **Validação:** <comando do runner e `git diff --check` após o lote aprovado>
- **Veredito:** <retire / rewrite (na fronteira dona) / extend (linha em tabela existente) / retain>

Barra de retenção: mantenha o teste que garante, de forma independente, contrato público, protocolo, configuração, migração, armazenamento, segurança, plataforma, default, saída gerada, pacote, release ou arquitetura; nunca aposente o que é alcançável pela entrada do pacote; "estático" ou "lento" não é motivo para apagar. Baixo valor típico: sonda de cobertura sem asserção, auto-comparação, fixtures copiadas, grep exato em código-fonte sem ser contrato, teste de predicado privado duplicado na fronteira real, invocação duplicada do mesmo contrato, teste cujo único fim é manter um export de teste. Prova de regressão (se o lote criar teste): falha no HEAD, passa na base, passa após a correção.
