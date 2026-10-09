# FULLSTACK-COMPLETO — protocolo operacional

## 1. Contrato

Ative somente por comando explícito do usuário. O modo exige ler integralmente
a base própria de fullstack e QA, avaliar todas as áreas e aplicar os itens
pertinentes. Isso não obriga a usar uma stack, instalar dependências globais,
executar ataques ou modificar tudo. NA exige motivo; sem acesso é NV.
Quando o objeto for desconhecido, prepare inventário e perguntas materiais;
não declare execução de produto. Se houver apenas uma correção solicitada,
a cobertura integral não autoriza reescrever partes alheias.

A keyword inicia o processo; não transforma ações não autorizadas em
permitidas. Em pedido de implementação, decisões locais reversíveis e
verificações necessárias fazem parte do trabalho. Auditoria só relata.

## 2. Inventário de leitura e capacidades

Leia as instruções do projeto e o entrypoint fullstack; no repositório original,
leia também o router. Em exportação, o SKILL.md da skill é a entrada e a
ausência do router original não torna esse pacote parcial. Leia as nove referências
técnicas e este protocolo; quatro templates; QA SKILL e suas quinze
referências de conhecimento, protocolo e templates. No repositório, leia
contexto multidisciplinar, integração e catálogo. Em cópia exportada,
use os equivalentes locais `assets/contexto/` quando fornecidos. Somente
workflows selecionados precisam de leitura integral; não leia todos os
fontes gstack ou datasets de avaliação como instruções da tarefa.

Registre caminho, revisão, leitura completa/parcial/ausente e decisão extraída.
Saída truncada exige retomada. Faça lotes com checkpoint persistido; não
confunda leitura em lotes com presença simultânea de todo texto no contexto.
Evite contaminar o executor com critérios reservados de avaliação da skill.

Registre ferramentas e limites: leitura, escrita, shell, rede, navegador,
banco, Git e host/modelo. A ausência de ferramenta é limitação verificável,
não defeito da aplicação. Sem ambiente executável, forneça implementação ou
plano permitido e rotule runtime como não verificado.

## 3. Diagnóstico do sistema

- Inventarie jornadas, regras, entidades, integrações e pontos de entrada.
- Confirme versão, stack, scripts, configuração e estado de Git.
- Preserve mudanças do usuário. Não resete, descarte nem formate código
  não relacionado por conveniência.
- Identifique fontes de verdade para regra, design e contrato; exponha conflitos.
- Observe baseline: reprodução, checks existentes, dados e resultados.
- Classifique risco e custo de reversão. Dinheiro, dados, permissões,
  migração e ações externas merecem critérios específicos.

Use o checklist para marcar aplicabilidade por área: produto, UX/design,
frontend, backend, dados, arquitetura, segurança, acessibilidade, testes,
performance, IA e operação. “Completo” é cobertura dessa matriz, com
limitações honestas, não lista de caixas artificialmente verdes.

## 4. Plano de incremento e decisões

Descreva a fatia vertical: ação do usuário → regra → contrato → dados →
resultado visível. Defina oráculos antes da implementação, compatibilidade
com consumidores e efeitos de migração. Escolha o padrão já presente se
adequado; argumente por alternativa quando houver problema demonstrado.

Congele critérios da tarefa antes de medir o resultado. Mudança legítima de
requisito atualiza o plano com fonte; não reduza um critério para esconder falha.
ADR é necessário para decisão relevante, não para cada linha.

Não crie microserviços, fila, cache ou agente adicional apenas por estar
em “modo completo”. Spike tem hipótese, prazo e decisão que poderá informar.

## 5. Implementação autônoma no escopo

Implemente incrementos pequenos. Ajuste contratos, dados e estados juntos;
evite backend entregue sem tratamento de UI necessário, ou tela que promete
uma operação sem efeito real. Verifique assinatura de API e opções na versão
instalada. Não use documentação de versão diferente sem estratégia confirmada.

Para migração, preveja compatibilidade entre versões, lock/volume e recuperação.
Desabilitar botão não é idempotência. Ocultar elemento não é autorização.
Retry não garante segurança de operação com efeito colateral.

Inclua regressões significativas conforme risco; não adicione testes que
repetem a implementação sem oráculo. Edite documentação pertinente. Instalação,
merge, publicação e produção seguem o pedido e permissões disponíveis.

## 6. Revisão crítica e revalidação

Revise o diff procurando quebra de regra, falso verde, autorização insuficiente,
segredo, corrida, efeito duplicado, migração irrecuperável, interface incompleta
e complexidade sem motivo. Quando houver equipe autorizada, distribua revisões
com fronteiras claras e evite edições concorrentes no mesmo arquivo. Não
trate votos concordantes de agentes como prova de correção.

Execute checks apropriados e fluxo principal, incluindo negativos de maior
risco. Compare resultado persistido ao oráculo e preserve logs/trace relevantes.
Após correção, execute reprodução original e regressões por impacto. Se uma
mudança nova invalidar evidências anteriores, repita as verificações afetadas.
Não repita toda a suíte sem motivo quando o escopo validado não mudou.

Registre resultado real, tentativa, ambiente, revisão e limitação. Análise
estática pode confirmar propriedade estática; não confirma comportamento
operacional de navegador, banco ou SDK remoto. Screenshot não substitui
semântica assistiva ou verificação de servidor.

## 7. Gates

| Gate | Saída necessária |
| --- | --- |
| Entendimento | Fontes, escopo, regras e conflitos identificados |
| Plano | Fatia, contratos, riscos e oráculos definidos |
| Implementação | Mudança no escopo, estados e compatibilidade tratados |
| Validação | Checks executados e resultados ligados aos critérios |
| Revalidação | Falhas corrigidas novamente verificadas; impacto coberto |
| Entrega | Artefatos, riscos, execução, recuperação e continuidade documentados |

Resultado: concluído no escopo / parcial / impedido. Falha crítica impede
recomendação favorável; média de notas não a compensa. Falta de execução
material ou leitura obrigatória torna o modo parcial. Não declare validação
universal ou funcionamento em qualquer modelo/host.

## 8. QA e desenvolvedor trabalhando juntos

FULLSTACK-COMPLETO integra critérios QA, mas a revisão do próprio autor deve
ser identificada. QA-COMPLETO mantém seu contrato: se solicitado só como
auditoria, não corrige produto. Se ambos forem pedidos, mantenha um backlog
compartilhado com ID, requisito, achado, alteração, evidência e status de
revalidação; não duplique caixas conflitantes ou feche achado sem evidência.

Uma tarefa pode usar QA para definir riscos e desenvolvedor para corrigir,
seguida de QA para reverificar. A segunda revisão deve usar os requisitos e
artefatos brutos, sem receber conclusões desejadas como respostas obrigatórias.

## 9. Checkpoint e retomada

Guarde estado factual: objetivo, escopo, revisão, mudanças, critérios,
leituras, testes, primeira falha, pendências e próxima ação. Antes de retomar,
confira workspace e versão: o checkpoint pode estar desatualizado. Limite de
sessão não é critério de sucesso; preserve continuidade e não prometa controle
de tokens da plataforma.
