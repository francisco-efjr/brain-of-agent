Não teste as 432. Faça três coisas, nesta ordem:

1. **Tire o que não existe.** SSO só no Enterprise corta 432 para 336. Se o Safari só roda em macOS e iOS (suposição abaixo), cai para **294 combinações reais**.
2. **Use pairwise nas 294.** Dezessete configurações cobrem todo par de valores (todo navegador com todo SO, todo idioma com todo plano, todo login com todo navegador etc.). Acrescente 3 por risco: **20 configurações no total**.
3. **Plano × login não é configuração, é regra de negócio.** Teste com uma tabela de decisão pequena, no nível mais barato (API), em um navegador só. Não gaste linhas da matriz com isso.

**Suposições (confirme):**
- Safari só em macOS e iOS (não existe no Windows nem no Android).
- SSO só com plano Enterprise, e plano e idioma não mudam o comportamento do navegador.
- Cada linha roda a mesma jornada: login, a jornada que paga as contas e logout. Pairwise decide *onde* rodar, não *quanto* testar em cada lugar.

## As 20 configurações

As linhas 1 a 17 saem do gerador de pairwise, com as exclusões "SSO só Enterprise" e "Safari só macOS/iOS". As linhas E1 a E3 foram escolhidas por mim.

| # | Navegador | SO | Idioma | Plano | Login |
| --- | --- | --- | --- | --- | --- |
| 1 | Chrome | macOS | es | Enterprise | SSO |
| 2 | Safari | iOS | pt-BR | Free | Google |
| 3 | Firefox | macOS | pt-BR | Pro | Senha |
| 4 | Chrome | Windows | en | Free | Senha |
| 5 | Edge | Windows | es | Pro | Google |
| 6 | Firefox | Android | en | Enterprise | Google |
| 7 | Edge | iOS | pt-BR | Enterprise | Senha |
| 8 | Firefox | Android | es | Free | Senha |
| 9 | Firefox | Windows | pt-BR | Enterprise | SSO |
| 10 | Chrome | Android | pt-BR | Pro | Google |
| 11 | Safari | iOS | en | Pro | Senha |
| 12 | Edge | macOS | en | Free | Google |
| 13 | Safari | iOS | es | Enterprise | SSO |
| 14 | Edge | Android | en | Enterprise | SSO |
| 15 | Chrome | iOS | es | Enterprise | SSO |
| 16 | Safari | macOS | pt-BR | Free | Senha |
| 17 | Firefox | iOS | es | Free | Senha |
| E1 | Safari | macOS | pt-BR | Pro | Google |
| E2 | Safari | macOS | en | Enterprise | SSO |
| E3 | Chrome | Android | es | Enterprise | SSO |

**Por que E1 a E3.** Pairwise garante pares, não trios. Login por Google e por SSO dependem de redirecionamento, pop-up e cookies, que é onde navegadores se comportam diferente (a proteção contra rastreamento do Safari é o caso clássico). Das 42 combinações possíveis de navegador × SO × login, as 17 linhas cobrem 17. Entre as 25 restantes escolhi as duas de maior risco que ficaram de fora (Safari no macOS com Google e com SSO) e Chrome no Android com SSO, a mais provável de ser usada em volume entre as que sobraram. Idioma e plano nessas três são só preenchimento. Se tiver incidente ou chamado de login em outra combinação, troque as extras por ela.

## Como rodar sem virar 20 testes manuais por release

- **No PR:** só Chromium (uma ou duas linhas).
- **Noturno:** as 20 linhas automatizadas nos três motores (Chromium, Firefox, WebKit), com emulação mobile para o layout.
- **Antes do release:** Safari real em iPhone (linhas 2, 11, 13) e Chrome real em Android (10, E3), manual ou em nuvem de dispositivos. O WebKit do Playwright não é o Safari, e no Brasil todo navegador de iOS usa WebKit. Por isso as linhas 7, 15 e 17 (Edge, Chrome e Firefox no iOS) valem pouco como motor extra; se esses navegadores forem raros nos seus dados, declare "melhor esforço" e corte.
- **Regressão completa:** só na configuração mais usada nos seus dados de acesso, não nas 20.
- Se faltar tempo, rode primeiro as linhas com SSO e com Safari iOS, mas saiba que cortar linhas reabre pares descobertos.

## Plano × login: tabela de decisão (fora da matriz)

| Caso | Esperado |
| --- | --- |
| Conta Free ou Pro chama o endpoint de SSO direto, pulando a tela | recusado; nenhuma sessão criada |
| Conta Free ou Pro chama pela API um recurso exclusivo de plano superior | recusado (403 ou o código do seu contrato) |
| Enterprise: usuário removido no provedor de identidade tenta entrar | sem acesso; sessões e tokens existentes revogados |
| Enterprise: SSO com domínio não verificado | não entra |
| Downgrade Enterprise → Pro com usuários que só entram por SSO | precisa de regra explícita (bloqueia ou migra para senha); nunca deixar a conta sem acesso |

A última linha só tem resultado esperado depois que o PO definir a regra.

## O que fica de fora e o risco que sobra

- Defeito que exija **três ou mais fatores** além dos trios cobertos (por exemplo, Firefox no Android com SSO) pode passar. Probabilidade baixa, mas não zero.
- Cada linha roda só a jornada crítica. Funcionalidade secundária é testada na configuração de referência; um defeito específico de navegador numa tela secundária pode escapar.
- Pairwise não verifica texto cortado, formato de data e número nem pluralização por idioma. Isso pede um teste próprio (unitário nos formatadores e uma passada visual por idioma, com atenção ao es e ao pt-BR, que costumam ter textos mais longos).
- Os números só valem se as suposições valerem.

## O que mudaria o resultado (me diga)

1. Algum desses navegadores roda em combinação que eu excluí ou incluí errado (Chrome, Firefox e Edge no iOS têm suporte oficial)?
2. Qual a participação de cada navegador e SO nos últimos 90 dias? Isso decide o que é "suportado" e o que é "melhor esforço".
3. Preço, moeda ou conteúdo mudam por idioma? Se sim, plano × idioma vira regra de negócio e ganha casos próprios.
4. O SSO tem um único provedor de identidade ou vários (SAML, OIDC)? Cada protocolo ou provedor vira um valor novo no parâmetro "login".
5. Enterprise com SSO obrigatório ainda aceita senha? Isso muda a tabela de decisão.
6. Qual é a jornada crítica que cada linha deve executar?

**O que verifiquei e o que não.** Rodei o gerador de pairwise (com seu autoteste) e conferi por força bruta que as 17 linhas cobrem os 111 pares possíveis, sem nenhuma combinação proibida. Nada foi executado contra o seu app, e as restrições de navegador × SO e a premissa de que plano e idioma não afetam o navegador são suposições. Se quiser, gero o CSV ou a configuração de projetos do Playwright para essa matriz.
