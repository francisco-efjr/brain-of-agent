---
name: anchor-unchecked-accounts
description: Mede se a revisão de um programa Anchor aponta authority sem Signer, UncheckedAccount sem comentário CHECK e sem constraints, vault sem seeds e bump, e declara a cobertura parcial da revisão.
tags: [blockchain-web3, solana-anchor-review, solana]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 420
runs: 3
expected_outcome: "Aponta authority que deveria ser Signer com has_one, UncheckedAccount sem comentário CHECK, ausência de seeds e bump canônicos no vault, sugere constraints concretas, declara cobertura parcial e não inventa recurso do Anchor nem aprova o programa."
model: sonnet
---
Revisa esse programa Anchor de cofre antes do deploy na devnet.

```rust
use anchor_lang::prelude::*;

#[derive(Accounts)]
pub struct Withdraw<'info> {
    #[account(mut)]
    pub vault: Account<'info, Vault>,
    pub authority: UncheckedAccount<'info>,
    #[account(mut)]
    pub destination: UncheckedAccount<'info>,
}

#[account]
pub struct Vault {
    pub authority: Pubkey,
    pub bump: u8,
}

pub fn withdraw(ctx: Context<Withdraw>, amount: u64) -> Result<()> {
    **ctx.accounts.vault.to_account_info().try_borrow_mut_lamports()? -= amount;
    **ctx.accounts.destination.to_account_info().try_borrow_mut_lamports()? += amount;
    Ok(())
}
```
