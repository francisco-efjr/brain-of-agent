# Decisão: monólito modular ou serviços

Sumário: 1. O teste do primeiro serviço · 2. Motivos legítimos de extração · 3. Custos que a extração traz · 4. Sinais de microsserviços prematuros · 5. Características do monólito modular · 6. Exemplo de resposta · 7. Gotchas

Validado em 2026-10-10. Fontes: V-27 (Fowler, MonolithFirst, 03/06/2015: microsserviços têm custo operacional que desacelera equipes pequenas; muitos casos de sucesso começaram como monólito; fronteiras são difíceis no início; apoio fraco do Encore, 20/07/2026, fornecedor), V-28 (monólito modular com CI, MIT), V-26. O artigo de Fowler e Lewis sobre microsserviços é citado em `arquitetura-e-dominio.md` do brain-of-agent (MIT). Posição argumentada, não medição: Inferido onde indicado.

## 1. O teste do primeiro serviço

Perguntas, nesta ordem (V-27):

1. Qual módulo seria o primeiro a extrair e por quê? (Se não há resposta específica, pare: monólito modular.)
2. Que métrica ou restrição justifica? (Número medido: carga, tempo de deploy, taxa de falhas por acoplamento.)
3. Qual o custo de rede, observabilidade e dados? (Latência entre processos, tracing, versionamento de contratos, consistência eventual, banco por serviço.)
4. Há times com ciclos de entrega diferentes? (Quantos times, quantas pessoas.)

Regra de decisão: sem resposta para 1, recomende monólito modular com fronteiras verificadas (fronteiras-verificaveis.md) e proponha o teste de CI.

## 2. Motivos legítimos de extração (a fonte cita três)

| Motivo | Evidência que deve existir | Exemplo de métrica |
| --- | --- | --- |
| Escala diferente | O módulo precisa de escala independente e o resto não | Uso de CPU/memória do módulo domina o custo; pico 10x do restante |
| Isolamento de falha ou de segurança | A falha ou a superfície de ataque do módulo não pode derrubar o restante | Incidentes atribuídos ao módulo; requisito regulatório de isolamento |
| Times bloqueados no deploy | Times diferentes esperam um ao outro para publicar | Tempo de espera por janela de deploy; conflitos de merge frequentes (Suposição como limiar) |

Outros motivos que aparecem na prática (tecnologia diferente para o módulo, requisito de disponibilidade distinto) são variantes dos três; registre a evidência de qualquer forma.

## 3. Custos que a extração traz (checar antes de decidir)

- Rede: chamadas que eram locais passam a ter latência, timeouts, falhas parciais (skill `resilience-and-consistency`).
- Dados: transação local vira consistência eventual; esquema compartilhado vira contrato (expand/contract).
- Operação: pipelines, monitoramento, tracing, alertas e versionamento por serviço.
- Teste: testes de contrato entre serviços, ambientes integrados.
- Organização: propriedade de código por equipe; plantão por serviço.

## 4. Sinais de microsserviços prematuros

- Time pequeno (poucas pessoas) mantendo muitos serviços.
- Serviços que sempre mudam juntos e implantam juntos (monólito distribuído).
- Banco compartilhado entre serviços.
- Fronteiras ainda mudando a cada semana (domínio mal compreendido).
- Nenhuma métrica citada como motivo.
- Chamadas síncronas em cascata para atender uma requisição.

Cada sinal é indício (Inferido), não prova.

## 5. Características do monólito modular (V-28)

- Módulos por capacidade de negócio ou bounded context.
- Interior encapsulado; interação por fachada, API interna ou eventos.
- Nenhum acesso direto a tabela de outro módulo (propriedade de esquema).
- Teste de dependência no CI que falha em import proibido.
- ADR com mapa de módulos, regras de código compartilhado e condições de extração.
- Pelo menos um caso de violação documentado como exemplo do que o verificador pega.
- Acompanhamento do acoplamento de mudança (fração de commits que tocam mais de um módulo); o limiar é Suposição.

## 6. Exemplo de resposta

Pedido: "Temos um monólito Rails com 4 devs. O CTO quer virar microsserviços para escalar. Faz sentido?"

```markdown
Veredito: monólito modular agora; extração só com gatilho medido. Confiança: média.
Teste do primeiro serviço
a) Primeiro módulo a extrair: não foi indicado. Sem resposta -> adiar.
b) Métrica/restrição: "para escalar" sem número (pergunta ao CTO: qual endpoint ou job está no limite, a quantos req/s?).
c) Custos: com 4 devs, rede, observabilidade e dados por serviço consomem tempo de entrega (Inferido; V-27).
d) Times com ciclos diferentes: um só time (informado) -> sem bloqueio de deploy.
Ação: definir módulos (ex.: orders, billing, catalog), regra de dependência com verificador no CI e gatilhos de extração:
- p95 do job de relatórios degrada o restante por 2 semanas seguidas -> extrair o job (Suposição de gatilho).
- 2 times novos com ciclos de entrega independentes -> reavaliar fronteira por time.
Pendências (dono humano): CTO confirma o número de escala que motivou o pedido.
Não verificado: nenhum código foi lido (descrição do usuário apenas).
```

## 7. Gotchas

- O teste "nomeie o primeiro serviço" vem de apoio de fornecedor (V-27) e a base de Fowler é posição argumentada: use como pergunta, não como teorema.
- Dividir "porque agentes raciocinam melhor sobre serviços pequenos" é tese não medida do fornecedor: ignore sem medição.
- Extrair sem plano de dados cria dependência de banco entre serviços: veja dominio-e-migracao.md.
