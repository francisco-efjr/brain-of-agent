# Decisões e trade-offs

Cada decisão: contexto, opções, critério, recomendação do plugin e fonte (itens V em [fontes.md](fontes.md)). Onde duas fontes divergem, a resolução e o motivo estão na tabela de conflitos. Decisão material no projeto do usuário vira ADR ([adr-contrato.md](../assets/templates/adr-contrato.md)). Conferido em 2026-10-10.

## Sumário

- [T-01 Proxy upgradeable ou contrato imutável](#t-01-proxy-upgradeable-ou-contrato-imutável)
- [T-02 `fail_on_revert` em invariantes](#t-02-fail_on_revert-em-invariantes)
- [T-03 `optimizer_runs`](#t-03-optimizer_runs)
- [T-04 Offset virtual ou depósito inicial morto (ERC-4626)](#t-04-offset-virtual-ou-depósito-inicial-morto-erc-4626)
- [T-05 Padrão de proxy: Transparent, UUPS ou Beacon](#t-05-padrão-de-proxy-transparent-uups-ou-beacon)
- [T-06 Admin: EOA, multisig e timelock](#t-06-admin-eoa-multisig-e-timelock)
- [T-07 Auditoria sequencial ou em paralelo](#t-07-auditoria-sequencial-ou-em-paralelo)
- [T-08 Foundry-first ou Hardhat](#t-08-foundry-first-ou-hardhat)
- [T-09 LLM ou fuzzing](#t-09-llm-ou-fuzzing)
- [T-10 Taxonomia de rótulos](#t-10-taxonomia-de-rótulos)
- [T-11 `answeredInRound` e idade do preço](#t-11-answeredinround-e-idade-do-preço)
- [T-12 Biblioteca auditada ou código próprio](#t-12-biblioteca-auditada-ou-código-próprio)
- [Tabela de conflitos entre fontes](#tabela-de-conflitos-entre-fontes)

## T-01 Proxy upgradeable ou contrato imutável

| Opção | Ganho | Custo / risco |
| --- | --- | --- |
| Imutável | Superfície menor; usuário confia só no código publicado; sem classes UPG | Bug crítico só se corrige migrando usuários |
| Upgradeable | Correção e evolução sem migrar | Novo poder privilegiado (quem atualiza); erros de initializer e de layout; usuários confiam em quem controla o upgrade |

Critério: reversibilidade de erro × confiança exigida. Se escolher upgradeable: justifique o padrão (T-05), restrinja quem atualiza (T-06), timelock nas operações sensíveis, plano de migração de storage entre versões maiores do OpenZeppelin (UPG-04). Recomendação: **imutável por padrão** para contratos pequenos e estáveis; upgradeable quando a equipe tem processo para tudo acima. Fonte: V-09, V-08. O upgrade em si é irreversível em estado: trate-o como migração de dados.

## T-02 `fail_on_revert` em invariantes

| Opção | Efeito | Risco |
| --- | --- | --- |
| `false` | Reverts do handler não falham o teste | Pode esconder falhas se o handler não restringe entradas (Inferido) |
| `true` | Qualquer revert falha | Ruído se o handler gera ações inválidas |

Critério: o handler só expõe ações válidas? Se sim, `true` é seguro e mais informativo; se não, `false` com contadores que provam cobertura. Seja qual for: **decida e documente** os reverts esperados. A página oficial só mostra `false` no exemplo, sem recomendar. Fonte: V-02. Rótulo: Inferido.

## T-03 `optimizer_runs`

`--optimize-runs` estima quantas vezes o contrato executará seus opcodes na vida: valor alto otimiza custo de execução (mais caro no deploy), valor baixo otimiza o deploy/tamanho. Não é número de passes. Critério: contrato chamado muito (AMM, token) × contrato raramente chamado ou limite de 24 KB. Recomendação: escolha por perfil de uso, registre no relatório e meça com `forge snapshot --diff` com a configuração de produção (inclusive via-IR). Fonte: V-23.

## T-04 Offset virtual ou depósito inicial morto (ERC-4626)

| Opção | Ganho | Custo |
| --- | --- | --- |
| Shares/ativos virtuais com offset de precisão (doc do OpenZeppelin) | Sem capital preso; mitigação embutida | Precisão adicional; confirmar qual offset a versão instalada aplica |
| Depósito inicial "morto" pelo deployer | Simples de entender | Capital preso permanentemente; precisa acontecer antes de qualquer outro depósito |

Critério: quem controla o primeiro depósito? Em ambos os casos: teste "atacante doa, vítima deposita; perda ≤ limite" (VLT-03). Recomendação: offset + teste; depósito morto como defesa adicional em cofres criados por factories. Fonte: V-10. A doc não confirma o padrão da implementação base: leia o código.

## T-05 Padrão de proxy: Transparent, UUPS ou Beacon

| Padrão | Use quando | Cuidado |
| --- | --- | --- |
| Transparent | Admin separado, regra simples | `ProxyAdmin` novo por deploy; custo de gás de checagem do admin (Inferido) |
| UUPS | Implementação leve e lógica de upgrade no contrato | `_authorizeUpgrade` obrigatório e restrito; esquecer trava ou abre |
| Beacon | Muitas instâncias com a mesma lógica | Um dono do beacon atualiza todos atomicamente: risco concentrado |

Fonte: V-09. Escolha registrada em ADR.

## T-06 Admin: EOA, multisig e timelock

EOA único é ponto único de falha e alvo de roubo de chave (SCN-05). Em produção: `DEFAULT_ADMIN_ROLE` em multisig, `AccessControlDefaultAdminRules` para transferência em duas etapas, `TimelockController` nas operações sensíveis para dar janela de reação. Contra: o timelock atrasa correções de emergência; resolva com um papel de pausa separado (poder estreito) em vez de encurtar o timelock. Nunca renuncie ao admin sem plano de recuperação. Fonte: V-08.

## T-07 Auditoria sequencial ou em paralelo

Pipelines de terceiros lançam muitos subagentes caçadores com aprovação acima de um limite; a doutrina geral indica que multiagente ganha em amplitude de pesquisa e perde em código com dependências compartilhadas, a um custo de tokens muito maior. Recomendação: **sequencial por contrato**; paralelo só com aprovação do usuário e estimativa de custo; um escritor por arquivo; revisores sem `Bash`. Fonte: V-15 (classe C, corroborada), prompt-principles P-19.

## T-08 Foundry-first ou Hardhat

Foundry tem fontes oficiais validadas (invariantes, fuzz, gás, configuração). Hardhat 3 não tem fonte validada; a única lida (skill comunitária) estava desatualizada. Recomendação: Foundry-first. Para Hardhat, diga "sem fonte validada" e rotule **Suposição**; não cite plugins descontinuados (`@nomiclabs/hardhat-etherscan`). Fonte: V-02, lacuna L3.

## T-09 LLM ou fuzzing

Dan Luu: na média, fuzzing teve menor latência e menos falso positivo do que pedir a um LLM que ache bugs; o LLM às vezes vence uma tentativa isolada. Produtos de revisão por LLM funcionam. São **complementares**: o LLM produz hipóteses e propriedades, fuzz/invariantes/PoC decidem. Fonte: V-07.

## T-10 Taxonomia de rótulos

OWASP SC Top 10 (2025) como rótulo principal; `swc_id` opcional só como identificador estável (registro desatualizado desde 2020); EthTrust v3 quando o usuário pedir níveis [S]/[M]/[Q]. Fonte: V-13.

## T-11 `answeredInRound` e idade do preço

Guias de auditoria muito citados mandam checar `answeredInRound`; a documentação atual da Chainlink o marca como obsoleto e a idade se mede por `updatedAt`. Resolução: seguir a doc atual; mencionar `answeredInRound` apenas como "obsoleto; confira a versão do feed". Doc atual prevalece sobre repositórios e guias. Fonte: V-19.

## T-12 Biblioteca auditada ou código próprio

Para criptografia, autenticação, papéis e padrões de token, prefira OpenZeppelin (ou equivalente auditado) a código próprio: menos superfície, menos bugs. Reimplemente só com motivo escrito e testes de invariante. Confirme a versão instalada: o OpenZeppelin 5.x removeu extensões (por exemplo, `ERC20Snapshot` não consta da API do ERC-20 5.x). Fonte: V-25, V-08.

## Tabela de conflitos entre fontes

| Conflito | Lados | Resolução |
| --- | --- | --- |
| Limiar de confiança | `/security-review`: >80%, faixas 0,7–1,0 e corte 8 de 10 | **≥ 0,8 na escala 0–1**: uma escala só |
| Exclusão de DoS | Prompt web exclui DoS; contrato trava fundos por gás/laço | DoS por gás é achado válido; fora só estilo/golfe sem impacto de segurança |
| `answeredInRound` | Guias antigos mandam checar; doc atual o marca obsoleto | Doc atual (T-11) |
| "≥ 3 execuções" | Atlas afirma; a página de Dan Luu não traz o número | Heurística **Inferida** da variância; sem citar como fato |
| `model` do agente | Exemplos fixam `opus`; V-24 recomenda `inherit` | `inherit`; fixar modelo é escolha de custo |
| `Bash` em revisor | Exemplo oficial usa `Bash`; a doc avisa que abre brecha de escrita | Revisor **sem `Bash`**; quem precisa rodar `forge` é outro agente com escopo claro |
| Instalação de ferramentas | READMEs de terceiros mandam `curl … \| bash`, editar `settings.json`, `--break-system-packages` | O plugin não instala nem referencia essas instalações; o usuário instala pelas páginas oficiais |
| Tom das regras comunitárias | "Save the ethics talk", avisos só "críticos", "Don't care about sources" | Rejeitado: segurança e fontes têm prioridade |
| Métricas de qualidade | Números de auditores LLM sem metodologia | Não citar; só o benchmark cego autorreportado do krait, como calibração |
