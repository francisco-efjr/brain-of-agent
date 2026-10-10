# Anchor: constraints de conta e o que verificar em cada uma

Fonte: Anchor, "Account Constraints" (https://www.anchor-lang.com/docs/references/account-constraints) e índice da documentação, lidos em 2026-10-10 (V-21, classe A). **Cobertura parcial**: as seções "Footguns" e "Sealevel Attacks" existem no índice e não foram lidas; não há scanner Solana neste plugin; CPI, Token-2022 e aritmética de Rust ficam fora (lacuna L8). Redação e exemplos próprios.

Rótulos: **Verificado** = V-21; **Suposição** = prática comum do ecossistema Solana ou raciocínio de segurança que a página não descreve; confirme na documentação da versão do Anchor do projeto.

IDs: `W3-SVM-01` toda conta com tipo e constraint, `UncheckedAccount` com `/// CHECK:`; `-02` `signer` onde há autoridade; `-03` PDAs com `seeds`/`bump` canônicos; `-04` `init_if_needed` só com defesa contra reuso; `-05` `realloc`/`close` e contas com fundos; `-06` versão do Anchor conferida.

## 1. Constraints registradas na referência (Verificado)

| Constraint | O que faz (segundo a referência) | O que o revisor verifica | ID |
|---|---|---|---|
| `signer` / tipo `Signer` | Exige que a conta tenha assinado a transação | Toda conta de autoridade é `Signer`; compare instruções irmãs | SVM-02 |
| `mut` | Marca a conta como mutável (e checa que é gravável) | Contas que o código modifica têm `mut`; contas que não deveriam mudar não têm | SVM-01 |
| `dup` | Permite a mesma conta mutável em dois campos (por padrão o Anchor bloqueia mutáveis duplicadas) | Cada uso de `dup` tem justificativa; sem `dup`, duas contas distintas são exigidas | SVM-01 |
| `seeds` + `bump` | Deriva e valida PDA do programa atual | Seeds identificam o dono/escopo; `bump` canônico; a mesma PDA não é derivável por seeds de outro contexto (Suposição quanto ao risco de colisão) | SVM-03 |
| `has_one = campo` | Exige que `conta.campo == outra_conta.key()` | Liga autoridade ao estado guardado (`vault.authority == authority.key()`) | SVM-02 |
| `address = pubkey` | Exige chave pública específica | Constantes corretas e do ambiente certo (devnet vs mainnet) | SVM-01 |
| `owner = programa` | Exige dono da conta | Não substitui o dono de `Account<T>`, que já checa `T::owner()` | SVM-01 |
| `constraint = expr` | Expressão booleana arbitrária | A condição realmente cobre o risco; mensagem de erro (`@ Err`) explica | SVM-01 |
| `init` / `init_if_needed` | Cria a conta; `init_if_needed` cria só se não existir (exige feature) | A página **não descreve** os riscos de reutilizar conta existente; trate como ponto de revisão (Suposição) | SVM-04 |
| `realloc` | Redimensiona a conta; reduzir devolve lamports acima do mínimo isento de aluguel | Contas que guardam fundos: o saldo mínimo continua coberto; efeito em cofres | SVM-05 |
| `close = destino` | Fecha a conta e envia lamports ao destino | Destino é controlado por quem deve ser; dados não reaproveitáveis | SVM-05 |
| `zero` | Conta recém-criada com dados zerados | Uso correto em inicialização grande | SVM-01 |
| `discriminator` | Define o discriminador do tipo | Antes do Anchor 1.0, contas com discriminador zerado podiam ser tomadas via IDL; confira a versão | SVM-06 |
| `executable` | Exige que a conta seja um programa | Em CPI, o programa chamado é o esperado (CPI: fora da cobertura) | SVM-01 |
| `/// CHECK:` | Obrigatório em contas sem tipo (`UncheckedAccount`/`AccountInfo`) | O argumento do comentário é correto, não um "seguro por design" genérico | SVM-01 |

## 2. Tipos que já validam algo

| Tipo | Valida | Não valida |
|---|---|---|
| `Account<'info, T>` | Dono do programa e discriminador do tipo `T`; desserializa | Relação com outras contas (use `has_one`/`constraint`) |
| `Signer<'info>` | Assinatura | Que seja a autoridade correta (ligue com `has_one`/`constraint`) |
| `Program<'info, P>` | Que a conta é o programa `P` | — |
| `SystemAccount<'info>` | Dono = programa do sistema | Que seja a conta esperada |
| `UncheckedAccount<'info>` / `AccountInfo` | Nada | Tudo: exige `/// CHECK:` e sua revisão |

## 3. Exemplo vulnerável e corrigido

Vulnerável (instrução de saque):

```rust
#[derive(Accounts)]
pub struct Withdraw<'info> {
    #[account(mut)]
    pub vault: Account<'info, Vault>,
    /// CHECK: o dono do cofre
    pub authority: UncheckedAccount<'info>,
    #[account(mut)]
    pub destination: SystemAccount<'info>,
}
```

Problemas: `authority` não é `Signer` e não está ligada a `vault` (SVM-02); o comentário `/// CHECK:` não explica a segurança; `vault` não valida PDA (SVM-03). Qualquer chamador passa a chave pública do dono sem assinar.

Corrigido:

```rust
#[derive(Accounts)]
pub struct Withdraw<'info> {
    #[account(
        mut,
        has_one = authority,
        seeds = [b"vault", authority.key().as_ref()],
        bump = vault.bump,
    )]
    pub vault: Account<'info, Vault>,
    pub authority: Signer<'info>,
    #[account(mut)]
    pub destination: SystemAccount<'info>,
}
```

Por que: `has_one` liga o estado à autoridade; `Signer` exige assinatura; `seeds`/`bump` amarram a conta à PDA do dono, com bump armazenado; `destination` é conta do sistema. Esta correção cobre contas; a lógica do handler (limites, rent) continua exigindo revisão.

## 4. Perguntas fora da cobertura (Suposição; rotule e não conclua)

- CPI: o programa chamado é validado (`Program<'info, T>`)? contas passadas na CPI vêm do chamador sem checagem? (lacuna L8)
- Token-2022 e extensões de token: o programa aceita mint com extensões que mudam o comportamento (taxa, hooks)? (lacuna L8)
- Aritmética: `checked_add/sub/mul` ou `overflow-checks` no perfil de release? (Rust não reverte overflow em release por padrão, a menos que configurado: confirme no `Cargo.toml` do projeto.)
- Reinicialização de conta, confusão de tipos e substituição de contas em `remaining_accounts` são classes clássicas descritas em Sealevel Attacks, que não foi lido.

## 5. Como escrever os achados

Formato de `contract-security-review` adaptado: `programa/arquivo.rs:linha — instrução/struct`, severidade, confiança, ID `W3-SVM-*`, cenário do tipo "o chamador passa a conta X em vez da Y", impacto (quem perde o quê), correção mínima (constraint a acrescentar), evidência ("pendente: sem ferramentas de teste Solana neste plugin"). Sempre com a faixa de cobertura parcial no topo.
