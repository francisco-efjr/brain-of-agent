# Runbook: modelo comentado e exemplo

Conteúdo: 1 modelo · 2 exemplo `DiskFull` · 3 checklist de revisão · 4 notas de fonte.

O exemplo é **ilustrativo**: servidor, caminhos e comandos vêm do pedido de exemplo; nenhum comando foi executado e nenhuma saída foi observada. Em uso real, cada valor vem do usuário ou do repositório.

## 1. Modelo

````markdown
# Runbook: <alerta ou tarefa>

- Quando usar: <alerta exato ou sintoma>
- Gravidade e impacto: <...>
- Público: <on-call, SRE, suporte>
- Acessos necessários: <papéis, ferramentas; sem credenciais>
- Responsável: <time e canal>
- Última verificação: <AAAA-MM-DD ou "nunca verificado">

## 1. Pré-requisitos
## 2. Procedimento
### Passo N: <verbo no infinitivo + objeto>
```bash
<comando exato>
```
Esperado (não executado): <critério observável>
Se diferente: <ir ao passo X | escalar para Y>
## 3. Verificação
## 4. Rollback
## 5. Escalonamento
## 6. Manutenção
````

## 2. Exemplo: alerta `DiskFull` na VM de logs

Pedido do usuário (resumido): comandos conhecidos `df -h`, `journalctl --vacuum-size=500M`, `rm -rf /var/log/old/*`, `systemctl restart rsyslog`; "rode para ver a saída". Resposta da skill: não executa; escreve o runbook com "Esperado (não executado)" e lista os comandos para o usuário validar.

````markdown
# Runbook: DiskFull na VM de logs

- Quando usar: alerta `DiskFull` (uso de /var/log acima do limiar configurado)
- Gravidade e impacto: alta; perda de logs novos quando o disco enche
- Público: on-call com acesso SSH à VM de logs
- Acessos necessários: SSH com sudo na VM `<VM_LOGS>`
- Responsável: time de plataforma, canal `<CANAL>`
- Última verificação: nunca verificado

## 1. Pré-requisitos

- Confirme que o alerta é real (passo 1). Não execute durante rotação de logs agendada (`<JANELA>`).
- Tenha à mão a política de retenção de logs (`<LINK_POLITICA>`; link a confirmar).

## 2. Procedimento

### Passo 1: Confirmar o uso de disco
```bash
df -h /var/log
```
Esperado (não executado): coluna Use% acima do limiar do alerta para o ponto de montagem de `/var/log`.
Se diferente: o alerta pode ser ruído; confira o dashboard `<DASHBOARD>` e, sem uso alto, encerre e registre.

### Passo 2: Listar o que ocupa espaço
```bash
du -sh /var/log/* | sort -h | tail -n 10
```
Esperado (não executado): lista com os 10 maiores itens; `old/` e o diretório do journal entre eles.
Se diferente: outro diretório domina; escale para o dono do serviço correspondente.

### Passo 3: Listar o que seria apagado em `/var/log/old`
```bash
ls -lh /var/log/old | head -n 50
```
Esperado (não executado): arquivos arquivados além da retenção.
Se diferente: diretório vazio ou inexistente; pule o passo 5.

### Passo 4 [DESTRUTIVO]: Reduzir o journal para 500 MB
Peça confirmação humana antes de executar; registre quem confirmou.
```bash
sudo journalctl --vacuum-size=500M
```
Esperado (não executado): mensagem informando os arquivos do journal removidos e o espaço liberado.
Se diferente: nenhuma liberação; siga ao passo 5. Erro de permissão: escale.

### Passo 5 [IRREVERSÍVEL]: Remover logs antigos já copiados
Confirme com o dono dos logs que (a) a retenção permite apagar e (b) existe cópia fora desta VM. Peça confirmação humana antes de executar; registre quem confirmou.
```bash
sudo rm -rf /var/log/old/*
```
Esperado (não executado): comando sem saída; `df -h /var/log` mostra espaço liberado.
Se diferente: erro de "dispositivo ocupado" ou espaço não liberou; arquivos podem estar abertos por um processo; vá ao passo 6.

### Passo 6 [DESTRUTIVO]: Reiniciar o rsyslog para liberar arquivos abertos
Peça confirmação humana antes de executar. Impacto: breve perda de mensagens em trânsito.
```bash
sudo systemctl restart rsyslog
```
Esperado (não executado): sem saída; `systemctl status rsyslog` em `active (running)`.
Se diferente: serviço em `failed`; escale com a saída de `journalctl -u rsyslog -n 50`.

## 3. Verificação

```bash
df -h /var/log
systemctl is-active rsyslog
```
Esperado (não executado): Use% abaixo do limiar do alerta por 15 minutos (`<TEMPO>`); `active`; alerta `DiskFull` resolvido no `<SISTEMA_DE_ALERTAS>`.

## 4. Rollback

- Passo 4: não há volta para os logs removidos do journal; ponto sem retorno.
- Passo 5: sem volta, exceto se houver a cópia externa confirmada.
- Passo 6: iniciar de novo com `sudo systemctl start rsyslog`.
- Prefira ampliar o volume (`<PROCEDIMENTO_DE_AMPLIACAO>`) a apagar quando a retenção exigir manter os dados.

## 5. Escalonamento

Escale ao time de plataforma (`<CANAL>`) se: o uso não cair após o passo 5; o rsyslog não voltar; ou o alerta reabrir em 1 hora. Envie: horário do alerta, saídas dos passos 1 e 2, passos executados e quem confirmou cada um.

## 6. Manutenção

Quem atender este alerta atualiza o runbook. Se a sequência virar sempre a mesma, proponha automação (rotação e retenção) em vez de manter comandos manuais.
````

## 3. Checklist de revisão (sim/não)

- [ ] Cada passo: comando, "Esperado (não executado)" e "Se diferente".
- [ ] Passos que mudam estado têm rótulo e confirmação; antes deles há passo de leitura.
- [ ] Ponto sem retorno identificado no rollback.
- [ ] Nenhuma saída inventada; nenhum segredo ou IP real.
- [ ] Escalonamento diz quando, quem e com quais informações.
- [ ] Data de verificação presente; responsável nomeado.
- [ ] Leitor limpo respondeu às perguntas sem novas lacunas.

## 4. Notas de fonte

- Esqueleto (cabeçalho, pré-requisitos, procedimento, verificação, rollback, escalonamento) segue o arquivo de templates do `techdocs-authoring` (MIT) em redação própria (V-31).
- Ideias de playbook por alerta, atualização por quem atende, automação de listas fixas e "rollback, depois correção, depois avanço" vêm do capítulo On-Call do SRE Workbook (CC BY-NC-ND 4.0), citadas como ideias, sem texto derivado.
- Rótulo: estrutura Verificada (V-31, classe B); exemplo e comandos ilustrativos, comportamento dos comandos depende de versão e distribuição (Não verificável aqui).
