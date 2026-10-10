# Matriz de dispositivos por risco

Adaptada de `brains/qa/references/mobile.md` do brain-of-agent (MIT, Francisco Edson). Comece pelo risco do app e pela base real de usuários; uma lista genérica de aparelhos não é estratégia. Registre cada combinação testada exatamente; não deduza a versão mínima suportada pela versão instalada no aparelho disponível.

App e build: [nome, versão] · SO mínimo suportado: [versão] · Base de usuários (fonte): [ex.: analytics da loja, data] · Data: [AAAA-MM-DD]

## Dimensões

| Dimensão | Escolha inicial | Quando ampliar | Escolha para esta release | Motivo |
| --- | --- | --- | --- | --- |
| SO | Mínima suportada e versão representativa atual da base | Mudança de SDK, APIs nativas, permissões ou incidente em uma versão | | |
| Hardware | Aparelho representativo e um com recursos limitados | Câmera, NFC, biometria, memória, fabricante, problema térmico | | |
| Tela e entrada | Tela pequena e fonte ampliada | Tablet, dobrável, orientação, teclado especial | | |
| Distribuição | Instalação limpa e atualização desde versão em uso | Migração de banco local, assinatura, login, esquema de armazenamento | | |
| Rede | Estável e interrupção no fluxo crítico | App offline, upload, streaming, rede corporativa, reconexão frequente | | |
| Acessibilidade | TalkBack/VoiceOver e fonte ampliada no fluxo crítico | Componentes novos, gestos próprios, gráficos, controles sem rótulo | | |

## Combinações executadas

| # | Plataforma | SO e versão | Modelo ou emulador | Resolução e idioma | Escala de fonte | Instalação (limpa / atualização) | Permissões | Flags e backend | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | | | | | |

## Emulador, simulador ou aparelho físico

Emulador e simulador dão retorno rápido e estados reproduzíveis. Valide em aparelho físico os riscos que dependem de hardware, consumo, rede real ou comportamento de fabricante. O Android distingue testes locais e instrumentados e admite emulador ou aparelho nos instrumentados (V-08); isso não torna os ambientes equivalentes. Emulação de viewport no navegador não prova nada de binário mobile.

## O que esta matriz não cobre

[ex.: iOS (sem macOS), aparelho físico de fabricante X, distribuição pela loja]
