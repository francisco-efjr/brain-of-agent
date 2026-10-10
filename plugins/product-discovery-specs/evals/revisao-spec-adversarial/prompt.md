---
name: revisao-spec-adversarial
description: Mede se o revisor de specs reporta as lacunas reais de uma spec colada (requisito vago, contradição entre história e FR, tecnologia em SC, ausência de fora de escopo) com severidade, confiança e local, sem reescrever a spec, sem comentar estilo e sem afirmar execução.
tags: [product-discovery-specs, spec-reviewer, adversarial-review, read-only, needs-write-grant]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill, Agent, Write]
timeout_seconds: 600
runs: 3
expected_outcome: "Relatório de revisão com as quatro lacunas (FR-001 vago, e-mail opcional contra obrigatório, SC-002 com tecnologia, falta de fora de escopo), cada uma com severidade, confiança e local, seções de checks lidos e não verificado, sem reescrever a spec e sem gravar arquivo."
model: sonnet
---
Revisa esta spec antes de eu mandar codar. Não tenho o repositório aberto aqui, é só o texto abaixo.

<spec>
# Spec: exportação de relatório de vendas (Draft)

## História P1
Como gerente de loja, quero exportar o relatório de vendas do período para analisar fora do sistema.
- O e-mail do destinatário é opcional: se vazio, o arquivo é baixado direto.

## Requisitos
- FR-001: O export deve ser rápido.
- FR-002: O sistema deve gerar o arquivo em CSV ou XLSX, conforme a escolha do gerente.
- FR-003: O e-mail do destinatário é obrigatório para o envio do arquivo.

## Critérios de sucesso
- SC-001: 95% dos exports terminam em menos de 3 segundos.
- SC-002: Existe um índice composto no PostgreSQL sobre a tabela de vendas.
</spec>
