# EIP-1193 no dapp: erros, eventos e confiança no provider

Fonte: EIP-1193 (Final, criada em 2018-06-30), lida em V-22. Rótulos: **Verificado** = V-22; **Inferido** = conhecimento estável de bibliotecas e EIPs vizinhas não lidas (confira na EIP e na versão da biblioteca do projeto). Fronteira: construção de UI e estado do dapp pertence ao plugin `web-frontend`; este arquivo cobre só a segurança.

IDs: `W3-SIG-01` assinatura presa a cadeia e contrato (domínio); `-02` nonce, validade e idempotência; `-03` dapp trata erros e eventos e o Provider é código não confiável; `-04` nunca pedir chave ou seed, e dados exibidos batem com o que será executado.

## 1. Fatos da norma (Verificado)

- `request(args)` é o ponto de entrada; o Provider emite `connect`, `disconnect`, `chainChanged`, `accountsChanged` e `message`.
- O Provider não gerencia chaves e deve ser tratado como código não confiável.
- Contas não são expostas por padrão: o dapp pede acesso (`eth_requestAccounts`).
- Códigos de erro: 4001 usuário rejeitou; 4100 não autorizado; 4200 método não suportado; 4900 desconectado; 4901 cadeia desconectada.

## 2. Tratamento esperado (W3-SIG-03)

| Sinal | Significa | O dapp deve | Teste/observação |
|---|---|---|---|
| Erro 4001 | A pessoa recusou | Voltar ao estado anterior sem alarme; não tentar de novo sozinho | Simular recusa e conferir que não há loop de pedidos |
| Erro 4100 | Conta ou método não autorizado | Pedir conexão de novo por ação do usuário | Chamar método sem conectar |
| Erro 4200 | Método não suportado pela carteira | Oferecer alternativa (por exemplo, assinatura mais simples) ou explicar | Carteira sem `eth_signTypedData_v4` |
| Erros 4900 e 4901 | Desconectado de todas as cadeias / da cadeia pedida | Mostrar estado desconectado, bloquear envio | Desligar a rede na carteira |
| `accountsChanged` | Conta ativa mudou | Descartar sessão, saldos e assinaturas pendentes da conta antiga; revalidar | Trocar de conta no meio de um fluxo |
| `chainChanged` | Cadeia mudou | Recarregar leituras, descartar estado derivado da cadeia antiga, revalidar `chainId` antes de assinar | Trocar de cadeia depois de montar o JSON de assinatura |
| `disconnect` | Provider perdeu conexão | Mostrar estado e não enviar | Idem |
| 4902 em `wallet_switchEthereumChain` | Cadeia não adicionada (EIP-3326) | Oferecer adicionar com parâmetros oficiais | Inferido: EIP-3326 não lida; confirme |

## 3. Perguntas de revisão

1. O `chainId` do domínio EIP-712 vem da cadeia ativa lida por `eth_chainId` no momento do pedido, ou de constante? (replay entre cadeias, `W3-SIG-01`)
2. Depois de `chainChanged`/`accountsChanged`, o estado antigo é invalidado, inclusive o JSON de assinatura que já estava montado?
3. O texto exibido à pessoa (valor em unidades legíveis, destinatário, prazo) é gerado a partir dos mesmos números que entram na struct assinada? Conversões de decimais em dois lugares divergem (`W3-SIG-04`).
4. Existe alguma tela, campo ou função que pede chave privada, seed ou mnemônico? Qualquer ocorrência é achado de severidade Alta (`W3-SIG-04`).
5. O dapp trata o objeto do provider como não confiável: não executa strings vindas dele, não confia em campos de erro para decidir autorização, não injeta mensagem de erro no HTML sem escapar (XSS)?
6. O dapp assume que existe um único `window.ethereum`? Com várias carteiras instaladas, a escolha pode ser disputada por extensões; o mecanismo de descoberta de provedores (EIP-6963) existe para isso (Inferido; EIP não lida).
7. Há assinatura opaca (`personal_sign` de um hash hexadecimal que a pessoa não consegue ler)? Prefira dados tipados (EIP-712) que a carteira mostra campo a campo.
8. Conexão automática ao carregar a página sem gesto do usuário? Prefira conexão iniciada pela pessoa.

## 4. Achados típicos e severidade sugerida

| Achado | Severidade | Observação |
|---|---|---|
| Campo ou fluxo que coleta chave/seed | Alta | Nunca é aceitável |
| Domínio EIP-712 com `chainId` fixo ou ausente | Alta se o mesmo contrato roda em mais de uma cadeia; Média caso contrário | Combine com o item de nonce |
| Assinatura montada antes de `chainChanged` e enviada depois | Média | Revalidar antes de enviar |
| Erros 4001 tratados como falha de sistema (nova tentativa automática) | Baixa a Média | Pode gerar spam de pedidos de assinatura |
| Valor exibido diferente do valor assinado | Alta | Phishing involuntário; prove com exemplo numérico |

## 5. Limites desta revisão

- Não cobre ERC-4337, EIP-7702, ERC-1271 (contas de contrato), WalletConnect nem carteiras móveis (lacuna L5; mobile pertence a `mobile-apps`): comentários sobre eles saem como Suposição.
- Não assina nem testa em rede viva. Testes de front rodam com provider simulado.
