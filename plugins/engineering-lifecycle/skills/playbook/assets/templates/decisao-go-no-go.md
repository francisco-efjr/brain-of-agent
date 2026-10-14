# Modelo: decisão GO ou NO-GO (saída do `/ship`)

Use ao fim do `/engineering-lifecycle:ship` (skill [shipping-and-launch](../../../shipping-and-launch/SKILL.md)). Formato adaptado da Fase C do `/ship` do agent-skills (Addy Osmani, MIT), com o rótulo de severidade do brain. Regras que o preenchimento respeita:
- Os três relatórios (revisão, segurança, testes) vêm de subagentes despachados **na mesma rodada**; a síntese e a decisão são da sessão principal, nunca de um subagente.
- Todo achado tem `arquivo:linha`. Achado sem localização vira "Não verificado" e não bloqueia sozinho.
- Qualquer **Critical** (ou **High** de segurança) é bloqueador e o veredito padrão é NO-GO, **salvo aceite explícito do usuário**, registrado abaixo. A persona `security-auditor` usa escala própria (Critical, High, Medium, Low); a Fase B do `/ship` promove o High dela a bloqueador. Mantenha o rótulo de origem na coluna Severidade, em vez de convertê-lo.
- **Plano de rollback antes de qualquer GO** ([plano-de-rollback.md](plano-de-rollback.md)).
- Acessibilidade, infraestrutura e documentação não são cobertas pelas três personas: verifique direto e diga como.
- Pular o fan-out só se tudo isto vale: ≤ 2 arquivos, diff < 50 linhas e sem autenticação, pagamento, dados ou configuração. Registre o motivo.
- A decisão não faz push, deploy nem publicação; esses passos exigem confirmação do usuário.

```markdown
# Decisão de lançamento: [MUDANÇA / RELEASE] · [AAAA-MM-DD]

**Veredito: GO ou NO-GO**
Escopo: [commits, branch, diff de N arquivos e M linhas] · Fan-out: [executado em uma rodada, ou pulado com o motivo]

## Bloqueadores (corrigir antes de lançar)
| ID | Origem | Severidade | `arquivo:linha` | Evidência | Correção |
| --- | --- | --- | --- | --- | --- |
| [B1] | [persona ou direto] | [Critical ou High] | [src/x.ts:42] | [o que mostra] | [o que fazer] |

## Correções recomendadas (deveriam sair antes)
| ID | Origem | Severidade | `arquivo:linha` | Recomendação |
| --- | --- | --- | --- | --- |
| [R1] | [persona] | [Required, Optional, Nit ou FYI] | [src/y.ts:10] | [...] |

## Riscos aceitos (lança mesmo assim)
- [risco] · mitigação: [...] · aceito por: [nome, data, onde está registrado]

## Verificação direta (fora das personas)
- Acessibilidade (WCAG 2.2 AA): [teclado, leitor de tela, contraste: o que foi visto] · rótulo [Verificado, Inferido ou Não verificado]
- Infraestrutura: [variáveis de ambiente (só nomes), migrações, flags, monitoramento] · rótulo [...]
- Documentação: [README, ADR, changelog] · rótulo [...]
- Suíte e build: [comando e resultado desta sessão] · rótulo [...]

## Plano de rollback
- Gatilhos: [...]
- Procedimento: [passos, quem executa]
- Tempo de recuperação: [alvo]
- Documento completo: [caminho do plano de rollback]

## Relatórios por persona (completos)
- code-reviewer: [caminho ou resumo com `arquivo:linha`]
- security-auditor: [caminho ou resumo; prova de conceito descritiva, sem payload]
- test-engineer: [caminho ou resumo]

## Não verificado
- [o que não pôde rodar e por quê]

## Pendências do humano
- [decisão, de quem, para quando]
```

## Checagem

- [ ] Cada bloqueador e cada correção tem `arquivo:linha`.
- [ ] Nenhum Critical sem correção ou aceite explícito registrado.
- [ ] O rollback existe, com gatilho, passos, banco e tempos.
- [ ] A síntese foi feita na sessão principal e cada persona rodou somente leitura.
- [ ] Os rótulos Verificado, Inferido e Não verificado estão em cada verificação direta.
