# Checklist de ciclo de vida de dados do tenant e do titular

**Não é orientação jurídica.** Revise com advogado antes de uso comercial. Base: `V-27`, `V-28`, `V-29`, `V-61` (LGPD em texto original de 2018; GDPR em cópia de terceiros; Resolução CD/ANPD 15/2024 não lida integralmente). Se faltar acesso ao código ou ao contrato, registre "Não verificado" em vez de supor.

Papel do SaaS por tipo de dado: [operador (tenant é controlador) | controlador] · Escopo: [produto/tenant] · Data: [..]

## A. Itens

| Item | Existe? | Onde (arquivo, job, contrato) | Evidência | Rótulo |
| --- | --- | --- | --- | --- |
| **Exportação**: endpoint/job devolve dados do tenant/titular em JSON ou CSV legível por máquina; escopo vem do `tenant_id` do token; teste com dois tenants | | | | |
| Exportação distingue **acesso** (LGPD art. 18, II) e **portabilidade** a outro fornecedor (art. 18, V; GDPR art. 20: dados fornecidos pelo titular) | | | | |
| **Eliminação**: banco, storage, caches, índices de busca, réplicas, processadores notificados | | | | |
| Eliminação executa a instrução do controlador (art. 39) e respeita as exceções do art. 16 | | | | |
| Registro do pedido e da conclusão da eliminação | | | | |
| **Backups**: prazo de expiração definido e **comunicado ao tenant** | | | | |
| **Retenção**: tabela por tipo de dado, com prazo em contrato (prazos = decisão de produto e jurídico) | | | | |
| **Registro de operações** (quem acessou ou exportou dados de tenant), sem PII (art. 37) | | | | |
| **Incidente**: runbook (bloco B) e registro de todos os incidentes | | | | |
| **DPA** com as cláusulas de GDPR art. 28(3) (instruções, confidencialidade, segurança, subcontratação, auxílio, devolução/eliminação, auditorias) | | | | |
| Desativação e downgrade não apagam dados | | | | |

## B. Runbook de incidente (ANPD, V-61)

| Campo | Valor |
| --- | --- |
| Instante da **detecção** | |
| Instante em que **se soube que dado pessoal foi afetado** (a contagem começa aqui) | |
| Dados afetados e titulares estimados | |
| Risco ou dano relevante? (dados sensíveis, de crianças, adolescentes ou idosos, financeiros, de autenticação, sigilosos, em larga escala) | |
| Papel do SaaS (operador ou controlador) e prazo contratual para avisar o tenant | |
| Aviso ao tenant (controlador) enviado em | |
| Comunicação à ANPD e aos titulares: **três dias úteis** (controlador decide e comunica) | |
| Informações complementares: **vinte dias úteis** a contar da comunicação | |
| GDPR (se aplicável): 72 horas à autoridade quando viável (art. 33) | |
| Evidência preservada (somente leitura) | |
| Registro do incidente (guardar por no mínimo cinco anos: fonte secundária) | |
| Decisões para o humano e o jurídico | |

Não verificável: prazo em dobro de pequeno porte; papel do operador na Resolução; art. 3º, XII e art. 10 no texto oficial.

## C. Auditoria por tenant (V-41)

Campos: `tenant_id`, `actor_id`, ação, recurso, resultado, instante UTC, origem; sem corpo, token, senha ou PII. Eventos: convite, mudança de papel, exportação, desativação, chave de API, login SSO, ação do suporte. Visibilidade ao admin do cliente: [decisão de produto: Suposição].

## D. Brasil, quando aplica (V-59, V-60)

Prestador de NFS-e definido: [tenant | SaaS] · Homologação antes de produção · Certificado fora do banco em texto puro · Datas fiscais em tabela de parâmetros (fonte, data de verificação) · NFS-e Nacional obrigatória para ME/EPP do Simples a partir de 01/11/2026 (Res. CGSN 191/2026, lida em cópia do DF, não no DOU).

## E. Saída

Tabela preenchida + pendências + aviso de que não é orientação jurídica. Eliminação nunca é executada pela IA sem autorização concreta.
