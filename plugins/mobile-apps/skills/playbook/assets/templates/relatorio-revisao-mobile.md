# Relatório de revisão mobile

Formato inspirado no padrão somente leitura do release-review (V-38, MIT) e na tabela do revisor adversarial (V-49). Use em auditoria, pré-submissão e revisão de PR. Auditoria não altera o produto.

Projeto: [nome] · Plataformas: [iOS / Android / RN / Flutter] · SDK e alvo mínimo lidos: [versões] · Data: [AAAA-MM-DD]
Escopo lido: [arquivos e pastas] · Escopo não lido: [lista] · Ambiente: [SO; macOS? emulador? aparelho?]
Resumo (até 5 linhas):

## Achados por prioridade

Prioridades: **risco provável de rejeição** · alto · médio · baixo. Não use "rejeitado" nem "Must Fix": a decisão de revisão não é garantida. Em dúvida, não reporte. Sem achado, escreva "sem achados" na prioridade.

| ID | Prioridade | Arquivo:linha ou "ausente em [arquivos]" | Regra ou checklist (ID, V-nn) | Evidência (trecho ou comando) | Impacto | Correção mínima | Rótulo |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [ex.: IOS-10] | Risco provável de rejeição | [Info.plist (ausente: NSCameraUsageDescription); ProfilePhotoView.swift:41] | PRM-02, V-58 | [AVCaptureDevice sem purpose string] | Falha de acesso e ITMS-90683 | Acrescentar chave com frase específica e localizada | Verificado por leitura |

## Pontos fortes

- [o que já está conforme, com arquivo]

## Ações do usuário

Itens que o agente não executa: configurar App ID e chaves na conta Apple, preencher Data safety e formulários do Play, hospedar `assetlinks.json`/AASA, assinatura e provisionamento, enviar para revisão, passar por VoiceOver/TalkBack.

## Não verificável

- [ex.: build iOS (sem macOS)]
- [ex.: partes não lidas: fim da seção 5 das App Review Guidelines (após 5.3.4)]
- [ex.: comportamento em aparelho físico]

## Fatos de loja usados (reconferir antes de agir)

| Fato | Fonte (URL) | Verificado em |
| --- | --- | --- |
| [ex.: targetSdk 36, extensão até 2026-11-01] | https://developer.android.com/google/play/requirements/target-sdk | 2026-10-10 |

## Plano de ação

1. [correção, dono, critério de pronto com comando]
2. [revalidação]

Declaração: este relatório foi produzido por modelo de IA; revisão do mesmo modelo que implementou não é validação independente.
