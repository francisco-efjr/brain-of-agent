# Checklist pré-deploy (para o usuário executar)

O agente prepara este checklist e **para**. Deploy, assinatura e transmissão de transações são feitos por você, no seu terminal ou carteira: o erro aqui perde fundos de forma irreversível. O agente não lê chave, seed nem `.env`. Itens marcados **(V-…)** vêm das fontes validadas; **(Suposição)** é composição própria do plugin; confira cada um ao seu contexto. Este checklist não é aconselhamento financeiro nem substitui auditoria humana externa.

## Código e build

- [ ] Versão do compilador e do Foundry travadas e registradas (`foundry.toml`, `forge --version`). (Suposição)
- [ ] Tag auditada do OpenZeppelin pinada; `audits/` lido; sem `master`/`latest`. (V-09)
- [ ] `forge build` sem warnings; `forge test` verde com a saída arquivada. (V-01, V-27)
- [ ] Invariantes e fuzz executados com `runs`, `depth` e `seed` registrados; contadores provam cobertura. (V-02)
- [ ] Relatório de auditoria com Cobertura e itens em "Verificação pendente" resolvidos ou aceitos por escrito. (V-14, V-16)
- [ ] `ffi` ausente ou `false` em `foundry.toml` nos scripts de deploy. (Suposição; página de configuração do Foundry)

## Acesso e governança

- [ ] `DEFAULT_ADMIN_ROLE` em multisig (ou `AccessControlDefaultAdminRules`); nenhuma função sensível em EOA único. (V-08)
- [ ] Operações sensíveis atrás de timelock; plano de recuperação escrito **antes** de qualquer renúncia ao admin. (V-08)
- [ ] Papel de pausa/limites definido, com quem aciona e como se desativa. (V-01)
- [ ] Eventos `RoleGranted`/`RoleRevoked` monitorados. (V-08)

## Upgradeability (se aplicável)

- [ ] `_disableInitializers` na implementação; `_authorizeUpgrade` restrito; sem `delegatecall`/`selfdestruct` na implementação. (V-09)
- [ ] Layout de storage comparado com a versão em produção (ferramenta do plugin de upgrades, executada por você). (V-09)
- [ ] Um `ProxyAdmin` novo por deploy. (V-09)

## Oráculos e rede

- [ ] Endereço de cada feed conferido na lista oficial **da rede de deploy**; heartbeat lido na página do feed e usado como limite de idade. (V-19)
- [ ] Em L2: feed de uptime do sequenciador e período de carência definidos; alias de endereço e taxa de dados L1 considerados. (V-20)
- [ ] Teste em fork local e em testnet atual (rede conferida na documentação do momento; Goerli está descontinuada). (Suposição)

## Chaves e operação

- [ ] Chaves fora do repositório e do contexto de qualquer agente; deploy a partir de carteira/hardware ou keystore sob seu controle. (V-04)
- [ ] Nenhum `--private-key` em linha de comando ou histórico do shell. (Suposição)
- [ ] Endereço do deployer sem papel permanente após o deploy. (Suposição)
- [ ] Procedimento de rotação de chaves e contato de emergência definidos. (V-18, SCN-05)

## Pós-deploy

- [ ] Verificação do código no explorer (fluxo não validado pelo plugin: lacuna L10; siga a documentação do Foundry/explorer).
- [ ] Parâmetros iniciais, tetos de depósito e limites conferidos on-chain por leitura. (V-01)
- [ ] Monitoramento de eventos críticos ativo. (V-08)

Resultado: [pronto | pendências: …] · Responsável: [nome] · Data: [ ]
