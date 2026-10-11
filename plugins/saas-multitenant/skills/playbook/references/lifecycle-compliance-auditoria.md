# Ciclo de vida do tenant, dados do titular (LGPD/GDPR), incidente, auditoria e fiscal

**Aviso: nada aqui é orientação jurídica.** É destilação técnica de normas e documentação. Prazos de retenção, cláusulas de DPA e enquadramento regulatório são decisões de produto e jurídico; revise com advogado antes de uso comercial. LGPD lida em texto original de 2018 (alterações posteriores não conferidas); GDPR lido em cópia de terceiros (gdpr-info.eu); Resolução CD/ANPD 15/2024 **não lida integralmente**.

Itens `V-nn` em `fontes.md`. Rótulos: Verificado, Inferido, Suposição, Não verificável.

## Sumário

- [1. Máquina de estados do tenant](#1-máquina-de-estados-do-tenant)
- [2. Onboarding idempotente e retomável](#2-onboarding-idempotente-e-retomável)
- [3. Papéis: controlador e operador](#3-papéis-controlador-e-operador)
- [4. Checklist por tenant: exportação, eliminação, retenção, incidente](#4-checklist-por-tenant-exportação-eliminação-retenção-incidente)
- [5. Runbook de incidente (ANPD)](#5-runbook-de-incidente-anpd)
- [6. DPA: cláusulas técnicas](#6-dpa-cláusulas-técnicas)
- [7. Trilha de auditoria por tenant](#7-trilha-de-auditoria-por-tenant)
- [8. Leitura de dado sensível e acesso de emergência](#8-leitura-de-dado-sensível-e-acesso-de-emergência)
- [9. Brasil: NFS-e e datas como parâmetro](#9-brasil-nfs-e-e-datas-como-parâmetro)
- [10. Lacunas](#10-lacunas)

## 1. Máquina de estados do tenant

Design nosso (**Inferido** de V-30; a Azure lista fases, não estados): `trial → active → deactivated → offboarding → deleted`.

| Transição | Gatilho | Dono | Dado afetado | Evento de auditoria |
| --- | --- | --- | --- | --- |
| `trial → active` | primeira cobrança paga (webhook) | billing | `tenant_billing.status`, `tenant_features` | `tenant.activated` |
| `trial → deactivated` | trial expira sem meio de pagamento (`missing_payment_method`) | billing | acesso bloqueado, dados preservados | `tenant.deactivated` |
| `active → deactivated` | `unpaid`/`paused`, pedido do tenant, abuso | billing/suporte | acesso suspenso; **nada apagado** | `tenant.deactivated` (motivo) |
| `deactivated → active` | regularização | billing | acesso restaurado | `tenant.reactivated` |
| `deactivated → offboarding` | cancelamento definitivo ou fim do prazo de graça | produto/jurídico | início do período de retenção | `tenant.offboarding_started` |
| `offboarding → deleted` | fim da retenção **e** instrução do controlador | operador executa | eliminação completa (seção 4) | `tenant.deleted` (com escopo e resultado) |

Regras: desativar **não** apaga (V-30, V-38); downgrade **não** apaga (V-23); cobrança falha desativa, nunca apaga (V-38); `deleted` só por instrução do controlador, com registro. Reonboarding dentro da retenção restaura (V-30). Trial usa os mesmos requisitos de segurança e SLA? infraestrutura compartilhada? migração para tenant pago e abuso são perguntas de entrada (V-30). Prazos: Suposição até o produto definir.

## 2. Onboarding idempotente e retomável

Sequência (acréscimo do crítico, **Inferido**; V-30, V-04, V-39): signup → organização (tenant) → membro dono → Customer Stripe com `metadata.tenant_id` → `tenant_features` iniciais → convites. Falha no meio **não pode** deixar tenant órfão nem Customer duplicado: cada passo grava o progresso (`onboarding_step`) e usa chave de idempotência por operação (`tenant-{id}-create-customer`); o fluxo é retomável a partir do último passo concluído.

Perguntas de entrada (V-30): residência de dados, compliance, RTO/RPO, plano de cobrança, ambiente de homologação, informações necessárias, self-service ou manual. Tenant brasileiro: CNPJ como texto (não `BIGINT`) com validação que aceite o formato alfanumérico (brain).

## 3. Papéis: controlador e operador

Quando o SaaS trata dado de clientes do tenant, em geral o **tenant é controlador** e o SaaS, **operador** (LGPD art. 39: operador trata conforme instruções do controlador; GDPR art. 28: instruções documentadas). O SaaS não decide sozinho a eliminação: executa a instrução do controlador sob as exceções do art. 16 (V-27). Quando o SaaS trata dados de seus próprios usuários (login, cobrança), é controlador desses dados. Mapear por tipo de dado e registrar em contrato.

## 4. Checklist por tenant: exportação, eliminação, retenção, incidente

Base: V-27, V-28, V-29 (síntese nossa). Template: `assets/templates/checklist-ciclo-vida-dados.md` (item × existe? × onde? × evidência × rótulo). Sem acesso ao código ou ao contrato: "Não verificado", não suponha.

| Item | O que verificar | Base (Verificado nas fontes) |
| --- | --- | --- |
| **Exportação** | endpoint ou job devolve dados do tenant ou do titular em JSON/CSV legível por máquina; escopo vem do `tenant_id` do token, nunca do corpo; teste com dois tenants | LGPD art. 18 II (**acesso**) e V (**portabilidade a outro fornecedor**, mediante requisição expressa); GDPR art. 20 (dados *fornecidos pelo titular*, formato estruturado, por consentimento ou contrato, automatizado) |
| **Eliminação** | job apaga banco, objetos em storage, caches, **índices de busca**, **réplicas**, e lista processadores notificados; registro do pedido e da conclusão; ordem e idempotência | LGPD arts. 15, 16, 18 VI; GDPR art. 17 (hipóteses a–f; exceções 17(3)) |
| **Backups** | apagar linha não apaga backup: definir prazo de expiração do backup e **dizê-lo ao tenant** | **Inferido** |
| **Retenção** | tabela por tipo de dado, com prazo em contrato e exceção legal | LGPD art. 16; prazos = **Suposição** de produto/jurídico |
| **Registro de operações** | quem acessou ou exportou dados de tenant; sem PII no log | LGPD art. 37; V-41 |
| **Incidente** | runbook (seção 5); registrar toda violação | LGPD art. 48; GDPR art. 33(5) |
| **Contrato** | DPA com as cláusulas da seção 6 | GDPR art. 28(3) |

Exceções do art. 16 da LGPD: obrigação legal ou regulatória; pesquisa com anonimização quando possível; transferência a terceiro dentro da lei; uso exclusivo do controlador anonimizado (V-27). GDPR 17(3): expressão, obrigação legal ou interesse público, saúde pública, arquivo e pesquisa, defesa em juízo. Portabilidade GDPR **não** cobre dados derivados (confirmar com jurídico, V-28).

**Correção ao brain**: na matriz de exportação, "LGPD art. 18, V" é portabilidade; o acesso é o inciso II (V-27, C14).

Implementação segura: o plugin escreve jobs e plano para revisão; **não executa** eliminação. Eliminação real só por autorização concreta, em homologação primeiro, com backup verificado e registro.

## 5. Runbook de incidente (ANPD)

Fonte: página oficial da ANPD (V-61, classe A para prazo e condições, Verificado) e Lefosse (escritório, classe B, para registro e critérios). **Não é orientação jurídica; o jurídico decide.**

1. **Preservar evidência e conter**: somente leitura no produto; não alterar nem apagar logs; isolar o vetor (por exemplo, desligar a rota) com autorização.
2. **Registrar dois instantes**: (a) quando o incidente foi **detectado**; (b) quando se **soube que dado pessoal foi afetado**. O prazo conta do segundo (Lefosse, secundária), não da detecção.
3. **Avaliar risco ou dano relevante**: o dever surge quando o incidente é confirmado, envolve dados pessoais da LGPD e pode causar risco ou dano relevante aos titulares; o controlador avalia e nem todo incidente exige comunicação (ANPD). Critérios de risco relevante (Lefosse): dados sensíveis, de crianças, adolescentes ou idosos, financeiros, de autenticação, sigilosos, em larga escala.
4. **Quem comunica**: se o SaaS é **operador**, avisa o **tenant (controlador)** no prazo do **contrato** (o prazo do operador na Resolução não foi lido: Não verificável); o controlador comunica ANPD e titulares.
5. **Prazos (ANPD)**: três dias úteis para comunicar ANPD **e titulares** (arts. 6 e 9 da Resolução 15/2024, segundo a página oficial), salvo prazo de legislação específica; informações complementares em **vinte dias úteis** a contar da comunicação (§ 3º). GDPR: 72 horas à autoridade, quando viável (art. 33(1)); o processador avisa o controlador sem demora injustificada (33(2)); notificação em etapas (33(4)).
6. **Registro**: todos os incidentes, comunicados ou não, por no mínimo **cinco anos** (Lefosse, secundária).
7. **Linha do tempo** e lista de decisões para o humano; comunicação ao tenant segundo o contrato.

**Não verificável**: prazo em dobro para agentes de pequeno porte (C17; fontes secundárias dizem que existe, texto não lido); art. 3º XII e art. 10 no texto oficial; papel do operador na Resolução; um terceiro que cita "seis dias úteis" não foi corroborado (C-g2-2).

Template: `assets/templates/checklist-ciclo-vida-dados.md` (bloco de incidente). Prompt de triagem somente leitura: PR-29 da biblioteca (processo é Suposição).

## 6. DPA: cláusulas técnicas

Cláusulas de GDPR art. 28(3) (a–h) como lista de verificação técnica: (a) instruções documentadas; (b) confidencialidade; (c) segurança (art. 32); (d) subcontratação; (e) auxílio nos direitos do titular; (f) auxílio nos arts. 32–36; (g) **eliminar ou devolver os dados ao fim, por escolha do controlador**; (h) auditorias; e o processador avisa se uma instrução parecer violar a lei. Redação própria sugerida (V-28): o processador elimina ou devolve os dados do tenant ao fim do contrato, por escolha do tenant, apaga as cópias salvo obrigação legal, e avisa o tenant de violação sem demora injustificada. Redação final é do jurídico.

## 7. Trilha de auditoria por tenant

Fonte: OWASP Logging Cheat Sheet (V-41, classe A, Verificado). NIST SP 800-92 (2006) é classe C, só referência de governança. **A visibilidade ao administrador do cliente (exportação, retenção visível, imutabilidade) continua sem fonte: os campos abaixo são nossos (Suposição).**

Linha mínima: `tenant_id`, `actor_id` (ou hash), `action`, `resource`, `result`, `ts` (UTC), `origin`; **sem** corpo de requisição, token, senha, identificador de sessão (use hash) ou PII.

Eventos obrigatórios por tenant: convite, mudança de papel, exportação/importação, desativação, chave de API criada/revogada, login SSO, ação do suporte do SaaS no tenant (inclusive impersonation), falhas de autenticação e de controle de acesso, administração de usuários e privilégios, acesso a dado sensível, upload, uso de chaves, mudanças de configuração. Falha de validação entra como sinal.

Integridade (OWASP): detecção de adulteração, mídia somente leitura/append-only, acesso aos logs monitorado e restrito, TLS no transporte, sanitizar CR e LF, falha de log não derruba a aplicação. Separe logs de **segurança, operação e auditoria**; a auditoria do tenant é consultável por `tenant_id` com RLS.

Teste (brain, V-23): ações de admin geram linha por tenant; linha não é editável pela role da aplicação (`REVOKE UPDATE, DELETE`); admin do tenant A não vê a auditoria do B.

## 8. Leitura de dado sensível e acesso de emergência

Apenas como exemplo de auditoria (brain, "Saúde"; sem conselho clínico ou regulatório): para dado sensível (LGPD art. 11), a trilha registra **leitura**, não só alteração (quem, o quê, quando, de onde); perfil sem vínculo com o titular tem acesso negado e registrado; nenhum dado sensível em log, URL ou analytics. "Quebrar o vidro" (acesso de emergência): permitido com justificativa obrigatória, alerta e revisão posterior. O mesmo desenho serve ao acesso de suporte (`autorizacao-e-tenant-context.md`, seção 9).

## 9. Brasil: NFS-e e datas como parâmetro

Aplica quando o SaaS emite ou habilita nota de serviço. Fontes: portal NFS-e Nacional (V-59, A), Resolução CGSN 191/2026 (V-60, A com ressalva), cópias não oficiais.

- **Quem é o prestador** (tenant ou SaaS)? Decida e documente. Use **homologação/produção restrita antes de produção**. Certificado do prestador fora do banco em texto puro (cofre). Grave a nota com `tenant_id` e **identificador de envio único** (idempotência). (Checklist **Inferido**.)
- A Resolução CGSN 191, de 4/8/2026 (DOU de 10/08/2026), altera a CGSN 140/2018: no art. 59 § 1º, a ME/EPP optante do Simples usa **obrigatoriamente a NFS-e de padrão nacional**, emitida pelo Emissor Nacional (web ou API); efeitos a partir de **01/11/2026**. Lida em **cópia "multivigente" do portal da Secretaria de Economia do DF**, que "não substitui o publicado oficialmente": não é o DOU.
- IBS/CBS no Simples: produzem efeitos a partir de 01/01/2027, **apenas em fonte secundária** (Fenacon, citando ato conjunto); a data em norma é Não verificável.
- **Regra (snippet 23)**: datas e regras fiscais ou regulatórias são **parâmetros com fonte e data de verificação**, nunca constantes no código. Conflito C18: vale a Resolução 191.
- Não verificável: credenciamento de integrador, emissão por terceiro, certificado do emitente.
- Spec: REQ-08 da skill `saas-feature-spec` (condicional).

## 10. Lacunas

Texto integral das Resoluções CD/ANPD 15/2024 e 2/2022; LGPD consolidada; GDPR em texto oficial (EUR-Lex truncou na leitura); visibilidade da auditoria ao admin do cliente; imutabilidade e retenção do log (sem fonte); relatos de falha real em produção; DOU para a CGSN 191; credenciamento de integrador de NFS-e; Regulamento Pix consolidado.
