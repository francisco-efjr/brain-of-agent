# Runbook de incidente com dado de tenant (ANPD e GDPR)

Redação própria. **Não é orientação jurídica**: o jurídico e o encarregado decidem se e quando comunicar. Fontes: página oficial da ANPD sobre incidente de segurança (V-61, classe A para prazo e condições), análise do escritório Lefosse (fonte secundária para o início da contagem, o registro e os critérios de risco), LGPD arts. 37, 39, 41, 46 e 48 (V-27), GDPR art. 33 (V-28, cópia de terceiros). Conferido em 2026-10-10. Rótulos: Verificado (lido na página), Verificado em fonte secundária, Inferido, Suposição, Não verificável.

## 0. Quando usar e limites

Use quando houver suspeita ou confirmação de que dado de um tenant foi exposto, alterado ou perdido (por exemplo, um bug mostrou a lista de clientes de um tenant a outro). A skill produz o runbook e a linha do tempo. Ela não altera o produto, não notifica ninguém e não afirma conformidade. Triagem técnica de vazamento suspeito entre tenants, somente leitura, está no prompt PR-29 da skill `prompts`.

## 1. Preservar evidência (somente leitura)

1. Não altere o produto nem apague logs. Registre quem fez o quê, quando.
2. Capture: logs de acesso e de auditoria do período, consulta ou rota suspeita, versão do código em produção, configuração de RLS e role da aplicação (consultas de catálogo em `tenant-rls-migration`).
3. Isole o canal se necessário (a decisão de desligar rota é humana e vai para o responsável).
4. Registre cadeia de custódia: quem coletou, onde está guardado.

## 2. Registrar os dois instantes (V-61)

| Instante | Definição | Valor |
| --- | --- | --- |
| T1, detecção | quando o incidente foi detectado | [data e hora, fuso] |
| T2, conhecimento | quando se soube que o incidente afetou dados pessoais | [data e hora, fuso] |

A contagem do prazo de comunicação parte de T2 (a página oficial exige que o incidente esteja confirmado e envolva dados pessoais; a leitura de que o prazo conta do conhecimento pelo controlador vem do Lefosse, fonte secundária). Não conte de T1 sem ressalva. Registre também a hora da decisão de risco.

## 3. Classificar

| Pergunta | Registro |
| --- | --- |
| Quais tenants (origem e destino da exposição)? | |
| Quais categorias de dado (identificação, contato, financeiros, autenticação, sensíveis, de crianças, adolescentes ou idosos, sigilosos)? | |
| Quantos titulares, aproximadamente? Larga escala? | |
| Durante quanto tempo? Houve acesso efetivo ou só possibilidade? | |
| Dados pessoais da LGPD estão envolvidos? | |

Critérios de risco ou dano relevante (Lefosse, secundária): dados sensíveis, de crianças, adolescentes ou idosos, financeiros, de autenticação, sigilosos, em larga escala. Nem todo incidente exige comunicação: o controlador avalia o risco (V-61).

## 4. Papéis e contrato

- Se o SaaS é operador (LGPD art. 39: trata conforme instruções do controlador), o contrato com o tenant fixa como e em quanto tempo o SaaS avisa o tenant; o tenant, como controlador, avalia o risco e comunica a ANPD e os titulares. O prazo para o operador avisar o controlador não foi pesquisado: siga o contrato. Se o SaaS é controlador de dados de conta, a obrigação é dele (V-27).
- GDPR art. 33(2): o processador avisa o controlador sem demora injustificada.
- Quem decide e quem executa: encarregado (LGPD art. 41), jurídico, responsável de segurança, porta-voz. Nomes e contatos no runbook do produto.

## 5. Contar os prazos (aviso: confirmar com o jurídico)

| Obrigação | Prazo | Contagem | Fonte e rótulo |
| --- | --- | --- | --- |
| Comunicar a ANPD e os titulares | três dias úteis | a partir de T2 | página oficial da ANPD citando os arts. 6 e 9 da Res. CD/ANPD nº 15/2024; Verificado na página; texto integral da resolução: Não verificado |
| Informações complementares | vinte dias úteis | a partir da comunicação (§ 3º) | página oficial; Verificado |
| Registro de todos os incidentes, comunicados ou não | no mínimo cinco anos | | Lefosse; fonte secundária |
| Prazo em dobro para agentes de pequeno porte | | | existe segundo fontes secundárias; Não verificável (não li a Resolução nº 2/2022 nem a 15/2024) |
| GDPR: notificação à autoridade | 72 horas quando viável | | art. 33(1), cópia de terceiros (V-28) |
| Contrato com o tenant | [prazo do contrato] | | contrato |

Regra de planejamento conservador (Suposição): conte o dia de T2 como dia 1 e não conte como útil feriado local nem fim de semana; qual convenção de contagem vale, e o que ocorre com horário-limite, é questão do jurídico.

Exemplo de calendário (hipotético, sem feriados): T1 na segunda-feira 10h; investigação confirma às 18h de terça-feira que dados pessoais de titulares foram expostos (T2 = terça). Contando terça como dia 1: dia 3 = quinta. Contando a partir do dia útil seguinte a T2: dia 3 = sexta. Planeje para quinta e confirme a convenção com o jurídico. O caso mostra por que T1 e T2 ficam registrados separados: contar de segunda (T1) anteciparia o prazo em um ou dois dias úteis sem base na fonte lida.

## 6. Conteúdo da comunicação

LGPD art. 48, § 1º: a ANPD define o prazo razoável e o conteúdo mínimo, incluindo os motivos de eventual demora (V-27). Conteúdo típico (Inferido do art. 33(3) do GDPR e das práticas de comunicação; conferir no formulário vigente da ANPD): natureza do incidente; categorias e número aproximado de titulares e de registros; contato do encarregado; consequências prováveis; medidas tomadas e propostas; motivos da demora, se houver. A comunicação em etapas é admitida (GDPR art. 33(4); LGPD: informações complementares).

## 7. Contenção e correção

1. Contenção: desativar a rota ou o recurso, revogar credenciais expostas, aplicar a correção mínima com teste.
2. Teste de regressão: caso novo na matriz de dois tenants (skill `tenant-isolation-tests`) que falha antes e passa depois (PAD-06, PAD-07).
3. Causa raiz: sem culpa, com o que mudar no processo, nos testes ou na arquitetura (por exemplo, filtro em mecanismo compartilhado e RLS, V-63, V-01).
4. Verificar se o mesmo padrão existe em outros lugares (skill `tenant-isolation-review`).

## 8. Linha do tempo (modelo)

| Quando (UTC e local) | Evento | Quem | Evidência |
| --- | --- | --- | --- |
| T1 | detecção | | |
| | preservação de evidência | | |
| T2 | confirmado que dado pessoal foi afetado | | |
| | avaliação de risco ou dano relevante: [resultado e justificativa] | | |
| | aviso ao tenant (controlador), conforme contrato | | |
| | decisão do jurídico sobre comunicação à ANPD e aos titulares | | |
| | contenção e correção | | |
| | complemento (até vinte dias úteis após a comunicação, se houver) | | |
| | registro do incidente (guardar por no mínimo cinco anos) | | |

## 9. Decisões que são humanas

1. Se o evento é incidente com risco ou dano relevante.
2. Se e quando comunicar a ANPD e os titulares, e por quem.
3. Quando e como avisar o tenant, além do contrato.
4. Se há titulares na UE e o GDPR se aplica.
5. Interpretação de prazos, feriados e convenção de contagem.
6. Comunicação pública.

## 10. Resposta-modelo para "temos de avisar a ANPD em três dias?"

"Depende de fatos e de papel, e a decisão é do jurídico. Pelo que li na página oficial da ANPD: o prazo é de três dias úteis para comunicar a ANPD e os titulares, conta do momento em que se soube que o incidente afetou dados pessoais (não da detecção), e vale quando há risco ou dano relevante. Como operador, o contrato com cada tenant define em quanto tempo vocês avisam o controlador, que decide e comunica. O prazo em dobro para pequeno porte e o texto integral da Resolução não foram verificados. Registrem agora T1 e T2 e preservem as evidências. Isto não é orientação jurídica."
