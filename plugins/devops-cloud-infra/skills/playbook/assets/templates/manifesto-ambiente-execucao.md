# Manifesto do ambiente de execução

<!--
Manifesto curto que acompanha qualquer deploy, teste de pipeline ou diagnóstico: explica mais
falhas que o nome "homologação". Sem segredos. Base: dados-ambientes-ci.md do brain-of-agent (MIT).
Use também como preflight: identidade do ambiente, versão implantada, dependências, relógio e permissões.
-->

| Campo | Valor |
| --- | --- |
| Artefato ou commit (identificador imutável) | [imagem@sha256:..., SHA do commit] |
| Configuração (revisão e flags relevantes, sem segredos) | [REVISÃO DO REPOSITÓRIO DE CONFIG] · [FLAGS] |
| Dados e schema (versão das migrações, massa, seed ou namespace) | [VERSÃO] |
| Dependências (reais, sandbox ou simuladas; versões conhecidas) | [LISTA] |
| Execução (comando, parâmetros, runner, início e fim, fuso) | [DADOS] |
| Plataforma (SO, runtime, versão do cluster, nuvem e região) | [DADOS] |
| Limites conhecidos (diferenças que podem mudar o comportamento) | [LISTA] |

## Preflight

| Verificação | Resultado | Rótulo |
| --- | --- | --- |
| Identidade do ambiente confirmada por comando de leitura | | |
| Versão implantada = artefato esperado | | |
| Dependências necessárias acessíveis | | |
| Relógio e fuso coerentes | | |
| Permissões suficientes (e não além do necessário) | | |

Falha de setup é bloqueio ou erro de infraestrutura: não é aprovação nem, automaticamente, defeito do produto.

## Fidelidade escolhida e justificativa

[Cálculo puro dispensa cluster de produção; concorrência de banco pode exigir o isolamento real; segurança depende de identidade, TLS, proxy e permissões; desempenho depende de topologia, dados e capacidade. Qual fidelidade foi escolhida e por quê?]

## Ambiente efêmero (se aplicável)

Criação: [MECANISMO] · observabilidade: [COMO] · expiração: [PRAZO] · limite de custo: [VALOR] · serviços compartilhados que continuam fora: [LISTA]
