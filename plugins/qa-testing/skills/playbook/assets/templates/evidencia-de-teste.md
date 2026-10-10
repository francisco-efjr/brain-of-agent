# Evidência de teste: <mudança>

Como usar (à mão ou com o comando `/qa-testing:qa-evidence`): preencha **somente** com comandos e saídas desta sessão. O que não foi rodado vai para "NÃO testado". Cole a saída real (truncada, com o caminho do log); nunca o resultado esperado como se fosse o obtido. Evidência de sessão anterior ou de outra versão não vale. Fontes: V-28, V-40, V-07; campos "comando", "saída" e "NÃO testado" são acréscimo do plugin (Suposição apoiada em V-01).

- **Data, ambiente e versão:** <AAAA-MM-DD · local/staging · commit ou build>
- **Escopo (o que foi alterado):** <arquivos e comportamento>
- **Comando executado:** `<comando literal>` · **Código de saída:** <n>
- **Saída relevante:**

  ```text
  <colar; truncar o resto e apontar para o log: caminho>
  ```

- **Verificado** (por teste ou execução manual; cada item com comando e trecho de saída): <comportamentos confirmados>
- **Teste de regressão** (se for correção): <falha colada sem a correção> → <verde colado com a correção>
- **Diff conferido:** <o diff alterou, removeu ou pulou teste ou asserção? sim/não e justificativa>
- **NÃO testado** (lacuna e motivo): <...>
- **Riscos residuais:** <se… então…>
- **Rótulos:** Verificado · Inferido · Suposição · Não verificável (marque cada afirmação)

Convenção de saída de scripts de teste para agente: poucas linhas; `ERROR <arquivo>:<teste> - <motivo curto>` em uma linha; sumário final de 3 linhas (total, falhas, caminho do log); log completo em arquivo.
