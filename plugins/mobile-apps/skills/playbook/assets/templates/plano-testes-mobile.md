# Plano de testes mobile: [feature ou release]

Adaptado do template `plano-de-teste` do brain-of-agent (MIT, Francisco Edson) e das fontes V-08, V-65 a V-70. Enxuto: serve para decidir, não para documentar. Cada linha diz o que o teste **prova** e o que **não prova**.

Plataformas e versões lidas: [ex.: Android Compose, iOS 17+, RN 0.7x] · Ambiente de execução disponível: [ex.: Windows; sem macOS; emulador Android] · Data: [AAAA-MM-DD]

## 1. Contexto e riscos

Qual é a mudança, quem usa, pior efeito realista de uma falha, prazo e como se publica e se desfaz. Declare suposições ("Supondo que...").

| ID | Risco (falha → efeito) | P (1-3) | I (1-3) | Nível | Mitigação (camada mais barata que o prova) |
| --- | --- | --- | --- | --- | --- |
| R1 | [resposta perdida depois de o servidor processar → cobrança duplicada] | 2 | 3 | Alto | [teste de integração com identidade de operação] |

## 2. Camadas e ferramentas

Escolha por plataforma sem trocar o stack que já atende ao risco.

| Camada | Android | iOS | Flutter | React Native | O que prova | O que não prova |
| --- | --- | --- | --- | --- | --- | --- |
| Unitário | ViewModel com fake | Swift Testing | unitário | Jest | Regra e estados | Renderização e SO |
| Componente / UI | `createComposeRule` / Espresso | XCTest + XCUIAutomation (macOS) | widget test | RNTL por texto/papel | Fluxo principal da tela | Hardware e rede real |
| Integração | instrumentado | XCTest | `integration_test` (+ `patrol` para UI nativa) | Jest + módulos | Contrato entre partes | Loja e aparelhos de fabricante |
| E2E | poucos | poucos | poucos | Detox / Appium / Maestro só para o vital | Jornada crítica | Todas as combinações de aparelho |

Regras: sem `sleep` (espere condição); `testID` só em E2E de app multilíngue; E2E só para autenticação, função central e pagamentos; nenhum teste enfraquecido para passar; bug novo ganha teste que falhava antes.

## 3. Matriz de ciclo de vida e rede

| Cenário | Ação controlada | Resultado esperado | Camada | Executado? |
| --- | --- | --- | --- | --- |
| Formulário parcial + app em segundo plano | Alternar de app e voltar | [regra] | UI | |
| Resposta perdida após processamento | Cortar a rede após o envio | Uma operação; reconciliação ao reconectar | Integração | |
| Fila offline após reiniciar app e aparelho | Reiniciar | Fila preservada, ordem e identidade | Integração | |
| Troca de conta A para B | Logout e login | Sem vazamento de cache, fila ou notificações | UI | |
| Atualização desde a versão anterior | Instalar sobre a anterior | Dados preservados; uma leitura e uma escrita | Manual | |

## 4. Dados e ambientes

Contas e registros sintéticos criados por API ou fixture; nenhum dado de produção. Aparelhos e emuladores usados: [lista]. Sem macOS, iOS fica "Não verificável".

## 5. Critérios de entrada, saída e suspensão

- Entrada: [ex.: build instalável; contas sintéticas prontas]
- Saída: [ex.: riscos altos com teste executado e evidência; nenhum defeito crítico aberto]
- Suspensão: [ex.: ambiente indisponível por mais de 4 h]

## 6. Evidências e relato

Use `registro-evidencias.md`. Se só houve emulador Android, escreva exatamente isso; não estenda o resultado a iOS, aparelho físico ou loja.
