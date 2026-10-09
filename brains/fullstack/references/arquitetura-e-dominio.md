# Arquitetura, domínio e decisões verificáveis

Esta referência orienta descoberta, desenho e revisão de sistemas existentes. Não prescreve framework nem reescrita. As técnicas e exemplos abaixo são recomendações próprias; não equivalem a uma certificação arquitetural.

## Descobrir antes de desenhar

Mapear entradas (UI, API, eventos, arquivos), casos de uso, persistências, serviços externos, processos assíncronos e fronteiras de confiança. Registrar quem é dono de cada dado e qual sistema decide cada regra. Identificar código realmente usado e configuração por ambiente; um diagrama desatualizado é uma hipótese.

Para cada fluxo importante, produzir uma sequência: ator → comando → autorização → regra → transação → efeito externo → resposta. Marcar pontos em que o processo pode morrer. Separar consistência local de eventual: uma fila não transforma efeitos independentes em transação distribuída.

## Domínio e invariantes

Extrair invariantes em linguagem observável. Exemplos: estoque nunca fica negativo; pedido cancelado não aceita captura; soma de débitos e créditos de uma transferência permanece zero; proprietário autorizado pode ler seu recurso e um usuário externo não pode. Associar cada invariante a camada de implementação, teste e métrica de falha.

Modelar transições explicitamente: `rascunho → confirmado → pago → enviado`; cancelamento depende do estado. Evitar combinações de booleanos contraditórias como `paid=true,cancelled=true,shipped=true` sem regra de reconciliação. Estados intermediários e compensações precisam de nomes e proprietários.

## Escolher a menor arquitetura suficiente

Usar organização modular dentro do processo quando ela oferece isolamento suficiente. Considerar separação de serviços se autonomia de entrega, escalabilidade independente ou isolamento justificarem custo de comunicação, observabilidade e operação. O artigo original de Fowler/Lewis descreve características e custos dos microserviços; não é obrigação de adotá-los. [Fonte: Microservices](https://martinfowler.com/articles/microservices.html).

Antes de introduzir abstração, mostrar ao menos uma variação real que ela precisa acomodar. Uma interface de repositório pode isolar o domínio de persistência; vinte camadas que apenas repassam argumentos aumentam o custo de investigação. Avaliar complexidade pelo número de decisões que um mantenedor precisa seguir, não pela quantidade de padrões nomeados.

## Exemplo antes/depois

Antes: controller verifica saldo, grava débito, chama pagamento externo, grava crédito. Uma falha externa deixa o débito aplicado e o usuário tenta novamente.

Depois proposto: caso de uso valida identidade e comando, registra intenção única e movimentos locais atômicos, entrega trabalho externo por outbox, processa confirmação de maneira idempotente e expõe estado pendente. O desenho depende do domínio: não afirmar que outbox elimina duplicatas; consumidor ainda precisa deduplicar.

Critérios: duas requisições concorrentes produzem uma operação de negócio; falha após commit pode ser recuperada; operador consegue localizar a intenção e seus efeitos; timeout não é apresentado como rejeição definitiva se a aceitação é desconhecida.

## ADR mínima

Registrar contexto, forças, opções consideradas, decisão, consequências, hipótese verificável e condição de revisão. Exemplo: “manter módulo no monólito até observar contenção de deploy entre equipes”; a evidência de revisão é concreta. Registrar restrições impostas pelo usuário como tais.

## Checklist de análise, implementação e revalidação

- [ ] Identificar runtime, topologia, atores e dependências observados.
- [ ] Nomear invariantes e estados de negócio; revisar casos ambíguos.
- [ ] Localizar quem autentica, autoriza e decide regras.
- [ ] Definir transações e falhas entre persistência e efeitos externos.
- [ ] Comparar opções e custos antes de mudar estrutura.
- [ ] Implementar fatia vertical com contrato, regra e teste associados.
- [ ] Validar concorrência, repetição e falha parcial no fluxo alterado.
- [ ] Atualizar ADR e sequência com a arquitetura efetivamente entregue.

## Falhas de avaliação

Não confundir organização em pastas com isolamento; cobertura de linha com proteção do domínio; compilação com integração; mock de fornecedor com evidência do fornecedor. Onde faltar acesso, registrar a fronteira não observada e a validação restante.

Fontes consultadas em 2026-10-09. Compatibilidade técnica deve ser confirmada na versão do projeto antes da implementação.
