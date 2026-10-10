# Registro de evidências de bancada

Adaptado de `registro-evidencias-qa.md` do brain-of-agent (MIT, Francisco Edson) com os níveis de evidência de V-27. Registre também resultados negativos. Oculte segredos e dados pessoais (SSID, senhas, tokens, números de série sensíveis).

| Evidência | Caso / funcionalidade | Método (host / simulado / hardware) | Placa e revisão | Comando | Saída (trecho ou caminho do log) | Estado | Artefatos | Limitação |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | passou / falhou / não executado / não verificável | | |

## Cartão de gravação (preencher ANTES de pedir confirmação)

- Objetivo: <...>
- Comando exato: `<...>`
- Placa / MCU: <...> · Porta ou probe: <...> (ambíguo? liste candidatos e pare)
- Binário: caminho `<...>`, tamanho `<...>`, hash `<...>`; endereço de gravação (obrigatório para `.bin`): `<...>`
- Escopo de erase: <nenhum / setor / flash inteira>
- Leitura de verificação prevista: <sim/não e como>
- Caminho de recuperação confirmado: <como recuperar a placa se falhar>
- O que será observado depois: <console, log, RTT; comando de leitura>
- Confirmação do usuário no chat (data/hora, texto): <"confirmo gravar" + referência da mensagem>

## Execução

ID: <id> · Caso: <id> · Tentativa: <n>
Método: <execução em hardware / simulação / análise estática / revisão>
Esperado e fonte: <resultado observável e de onde vem o oráculo>
Obtido: <resultado real>
Estado: <passou / falhou / não executado / não verificável>
Ferramentas e versões: <idf.py, west, probe-rs, toolchain>
Limitação e alcance da conclusão: <...>

## Mudança e revalidação

Achado original: <id> · Correção e revisão: <arquivos / commit> · Revalidação: <casos, evidências> · Regressões: <escopo e resultado> · Pendências: <...>

## O que ficou gravado na placa ao final

<versão, hash, partições alteradas, eFuses (devem ser "nenhuma alteração")>
