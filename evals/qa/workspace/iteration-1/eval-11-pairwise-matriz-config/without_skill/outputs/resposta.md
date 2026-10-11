Use teste combinatório do tipo pairwise ("todos os pares") com restrições, e separe o que é compatibilidade (navegador/SO) do que é regra de negócio (plano/login). Dá para sair de 432 combinações para uns 16 a 19 ambientes com uma cobertura bem defendível.

## 1. O 432 está inflado

- SSO só existe no Enterprise. Então plano x login tem 7 combinações válidas, não 9. Isso já derruba para 336.
- Safari só roda em macOS e iOS (não existe no Windows nem no Android). Então navegador x SO tem 14 pares válidos, não 16.

O espaço real é **294 configurações**, não 432.

## 2. Pairwise: todo par de valores aparece pelo menos uma vez

A premissa: a maior parte dos bugs de configuração é disparada por um fator sozinho ou pela interação de dois (Safari + iOS, Firefox + SSO, idioma + plano). Estudos empíricos, como os do NIST, apontam nessa direção. Em vez de testar todas as combinações, você monta um conjunto pequeno em que cada par de valores válidos (por exemplo "Firefox + Android" ou "es + Enterprise") aparece ao menos uma vez.

Aqui são 111 pares válidos, e 16 linhas cobrem todos (conferi a cobertura com um script):

| # | Navegador | SO | Idioma | Plano | Login |
|---|-----------|----|--------|-------|-------|
| 1 | Chrome | Android | es | Enterprise | SSO |
| 2 | Edge | Android | en | Free | Senha |
| 3 | Firefox | Android | pt-BR | Pro | Google |
| 4 | Chrome | Windows | pt-BR | Free | Google |
| 5 | Edge | Windows | en | Pro | Google |
| 6 | Firefox | Windows | es | Enterprise | Senha |
| 7 | Firefox | Windows | en | Enterprise | SSO |
| 8 | Chrome | iOS | es | Pro | Senha |
| 9 | Edge | iOS | pt-BR | Enterprise | SSO |
| 10 | Firefox | iOS | pt-BR | Free | Google |
| 11 | Safari | iOS | en | Enterprise | SSO |
| 12 | Safari | iOS | es | Free | Google |
| 13 | Chrome | macOS | en | Enterprise | Google |
| 14 | Edge | macOS | es | Enterprise | SSO |
| 15 | Firefox | macOS | es | Free | Google |
| 16 | Safari | macOS | pt-BR | Pro | Senha |

Cada linha é um ambiente, não um caso de teste novo. Em cada um você roda o mesmo roteiro curto de fluxos críticos: login, o fluxo principal de valor do produto, uma tela com muito texto e logout. Isso dá 16 execuções do roteiro em vez de 294 (ou 432).

## 3. O que eu somaria ao pairwise

1. **Triplas de risco, escolhidas à mão.** Pairwise não garante combinações de 3 fatores, e login costuma ser onde navegador e SO mais pesam (redirects, pop-ups, cookies de terceiros, política de rastreamento do Safari). Eu acrescentaria pelo menos: Edge + Windows + SSO (o ambiente típico de empresa), Safari + macOS + SSO e Chrome + iOS + Google. Com isso você fica em 19 ambientes. Safari + iOS + Google já está na linha 12.
2. **Regra de negócio fora da matriz.** As 7 combinações plano x login são lógica de servidor, quase independente de navegador. Teste todas as 7, mas em um único navegador (ou direto na API). Inclua o caso negativo: Free e Pro não podem ver nem usar SSO, nem forçando a URL ou a chamada.
3. **Funcionalidades exclusivas de plano.** Teste por plano, fora da matriz. Elas não são um problema combinatório, são um problema de cobertura de funcionalidade.
4. **Idioma como camada própria.** O que quebra em tradução é texto que estoura o layout, formato de data e número, acentuação e strings não traduzidas. Isso se pega com pseudo-localização e comparação de screenshots por idioma, sem multiplicar por navegador.
5. **Seu tráfego real manda.** Pegue no analytics as combinações navegador x SO que concentram uns 80% dos usuários e fixe essas no conjunto. Deixe o pairwise cobrir a cauda longa.
6. **Não ignore o motor de renderização.** Chrome e Edge usam Blink, Firefox usa Gecko e Safari usa WebKit. No iOS, em geral, Chrome e Firefox também rodam sobre WebKit. Isso ajuda a priorizar (Safari e iOS merecem mais atenção do que o 4º navegador Blink), mas não a cortar: Edge no Windows continua importante por causa do SSO corporativo.

## 4. Como gerar e automatizar

Com o PICT (Microsoft, gratuito), o modelo é este, e as restrições entram como regras:

```
Navegador: Chrome, Firefox, Safari, Edge
SO: Windows, macOS, Android, iOS
Idioma: pt-BR, en, es
Plano: Free, Pro, Enterprise
Login: Senha, Google, SSO

IF [Login] = "SSO" THEN [Plano] = "Enterprise";
IF [Navegador] = "Safari" THEN [SO] IN {"macOS", "iOS"};
```

Rode `pict modelo.txt` e use a saída. O número de linhas pode variar um pouco (16 a 18), e qualquer conjunto que cubra todos os pares serve. Outras opções: AllPairs/allpairspy, Hexawise ou um script próprio.

Para executar, no Playwright dá para ter projetos `chromium`, `firefox` e `webkit`, com emulação de dispositivo para os casos mobile. Para Safari no iOS e Chrome no Android de verdade, use uma nuvem de dispositivos reais (BrowserStack, Sauce Labs ou similar). O WebKit do Playwright ajuda, mas não é igual ao Safari real. Deixe o conjunto parametrizado por esse modelo para regenerar quando surgir um valor novo (um 5º navegador, outro idioma).

## 5. Limites

- Pairwise reduz muito o custo, mas não prova ausência de bug. Falhas que dependem de 3 ou mais fatores ao mesmo tempo podem passar. Por isso as triplas de risco do item 3.
- Quando um bug escapar para produção, descubra quais fatores o dispararam e adicione esse caso (ou suba para 3-wise só naquele subconjunto). A matriz evolui com o que você aprende.
- A matriz muda se você incluir versões de navegador, tablet, modo escuro ou outras dimensões. Revise o modelo quando isso entrar.

Se quiser, me passe o top de navegador x SO do seu analytics e eu monto a lista final com os ambientes fixos mais o pairwise.
