---
name: threat-model-upload
description: Mede se o modelo de ameaças de uma feature de upload produz DFD textual com fronteiras de confiança, STRIDE por fluxo, resposta e teste por ameaça, marca o que não foi descrito como Suposição e não trava quando ninguém pode responder.
tags: [security-appsec, threat-model, stride, batch-mode, mobile]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega em uma só resposta um documento em rascunho com DFD textual, fronteiras de confiança, tabela de ameaças STRIDE com resposta e teste, Suposições rotuladas, risco residual e decisões pendentes do humano, sem parar para perguntar e sem inventar fatos de arquitetura."
model: sonnet
---
Vamos adicionar upload de foto de perfil no nosso produto. Hoje existem o site (SPA em React) e o app Android, e os dois falam com o mesmo backend Django. O desenho que temos é este: o cliente envia a imagem para a API; o backend grava o original em um bucket S3 privado; um worker Celery gera thumbnails de 64 e 256 px com Pillow e publica em uma CDN pública; a URL do avatar aparece no perfil público do usuário e nos comentários. Não temos diagrama nem documento de design.

Modela as ameaças dessa feature. Estou rodando este pedido em lote e ninguém vai estar disponível para responder perguntas hoje, então entregue o que der, do jeito mais útil possível.
