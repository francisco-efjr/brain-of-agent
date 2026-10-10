# STRIDE por fluxo: perguntas, controles típicos e testes

Base: definições STRIDE da Microsoft Learn e quatro fases do OWASP Threat Modeling Cheat Sheet (CC BY-SA 4.0) (V-17, conferido em 2026-10-10). Os exemplos de controle e teste são redação própria a partir de conhecimento estável do domínio (Inferido) e das cheat sheets OWASP de autorização, sessão, CSRF, SSRF e validação (V-18, V-36, V-37, V-23, V-20). Reconfira versões e valores antes de citar como vigentes.

## Sumário

1. Perguntas e controles por categoria
2. Quais categorias valem para cada elemento (STRIDE por elemento)
3. Privacidade: LINDDUN
4. Componentes LLM
5. Outros métodos (uma linha cada)
6. Probabilidade e impacto sem pseudo-precisão

## 1. Perguntas e controles por categoria

| Categoria | Pergunta para o fluxo | Controles típicos | Teste de verificação (exemplo) |
| --- | --- | --- | --- |
| Spoofing (autenticidade) | Quem pode se passar por usuário, serviço ou origem? | autenticação forte, MFA, assinatura de webhook, mTLS entre serviços, validação de `Origin` | requisição sem credencial ou com credencial de outro ambiente retorna 401; webhook com assinatura inválida é descartado |
| Tampering (integridade) | O que pode ser alterado em repouso ou em trânsito? | TLS, assinatura/HMAC, autorização de escrita por objeto, cálculo de preço/total no servidor, constraints de banco | campo `total` enviado pelo cliente é ignorado e recalculado; arquivo alterado em trânsito falha na verificação |
| Repudiation (não repúdio) | Que ação sensível fica sem rastro ou sem autoria? | log de auditoria imutável com quem/quando/onde, sem dado sensível; relógio confiável | após alterar papel de usuário existe registro com autor e valor anterior; alerta dispara em N falhas de login |
| Information disclosure | Que dado vaza (resposta, erro, log, cache, URL, backup, terceiros)? | autorização por objeto e por propriedade, mínimo de campos, criptografia, erros genéricos, `Cache-Control: no-store`, mascarar logs | resposta de erro não traz stack nem SQL; usuário B não lê campo `hash` de A; log não contém token |
| Denial of service | O que pode ser tornado indisponível ou caro (CPU, memória, custo por chamada)? | limites de tamanho/taxa/paginação, timeouts, filas com teto, cotas por usuário/tenant | corpo acima do limite retorna 413; `?limit=100000` é truncado; exportação pesada repetida recebe 429 |
| Elevation of privilege | Como alguém ganha privilégio que não tem (papel, tenant, função admin, execução de código)? | negar por padrão, checagem de função no servidor, separação de privilégios, mínimo privilégio da conta do banco, sandbox | usuário comum em rota admin recebe 403; PATCH com `role: admin` não muda o papel (relê o recurso) |

Pergunte sempre pela fronteira: "o que muda de poder quando o dado cruza esta linha?". Se a resposta é "nada", a fronteira provavelmente está mal desenhada ou o fluxo é interno e fica fora do foco.

## 2. Quais categorias valem para cada elemento (STRIDE por elemento)

Conhecimento estável de modelagem (Inferido; fonte não lida nesta execução). Serve como atalho; na dúvida, avalie as seis.

| Elemento do DFD | S | T | R | I | D | E |
| --- | --- | --- | --- | --- | --- | --- |
| Entidade externa (usuário, terceiro) | sim | | sim | | | |
| Processo (serviço, função) | sim | sim | sim | sim | sim | sim |
| Armazenamento (banco, bucket, cache, fila) | | sim | sim (se for log) | sim | sim | |
| Fluxo de dados (canal, API, fila) | | sim | | sim | sim | |

## 3. Privacidade: LINDDUN

Use quando houver dados pessoais (V-17 cita LINDDUN; as sete categorias abaixo são conhecimento estável, Inferido): Linking (ligar registros de uma pessoa), Identifying (identificar o titular), Non-repudiation (provas indesejadas contra o titular), Detecting (inferir participação), Data disclosure, Unawareness (titular sem ciência), Non-compliance (descumprir política ou lei). Para cada fluxo com dado pessoal, registre finalidade, dados necessários, destinatários, retenção e descarte (brain fullstack). Requisitos legais (LGPD, GDPR) exigem avaliação específica: o plugin não tem fonte primária validada para citar artigos e isto não é parecer jurídico.

## 4. Componentes LLM

Para cada componente que chama modelo ou agente (V-14, V-11): LLM01 Prompt Injection (que conteúdo externo entra no prompt?), LLM02 Sensitive Information Disclosure, LLM05 Improper Output Handling (saída para SQL, shell, HTML), LLM06 Excessive Agency (ferramentas e permissões), LLM07 System Prompt Leakage, LLM10 Unbounded Consumption. Teste da tríade letal: dados privados + conteúdo não confiável + comunicação externa; três "sim" exigem remover uma capacidade, separar sessões ou exigir confirmação humana antes da ação de saída. Controle em texto de prompt não vale como controle.

## 5. Outros métodos (V-17: escolha pelo escopo)

- Attack trees: decomponha um objetivo do atacante em ramos de ações; bom para um ativo crítico.
- Abuse cases: histórias "como atacante, quero X"; bom para lógica de negócio.
- PASTA: processo de sete etapas orientado ao risco de negócio; pesado, para sistemas grandes.
- OCTAVE: avaliação organizacional de ativos e riscos; escopo de empresa, não de feature.
- VAST: modelo escalável para muitas equipes, ligado a ferramentas; escopo de organização.
- LINDDUN: privacidade (seção 3).

## 6. Probabilidade e impacto sem pseudo-precisão

- Probabilidade: Alta (qualquer usuário autenticado consegue, sem conhecimento especial), Média (exige pré-condição ou conhecimento), Baixa (exige acesso privilegiado, combinação rara ou insider).
- Impacto: Alta (dados de muitos usuários, dinheiro, tomada de conta, execução de código), Média (dados de um usuário, indisponibilidade parcial), Baixa (informação pouco sensível, inconveniência).
- Prioridade = alta probabilidade com alto impacto primeiro. Escreva sempre a justificativa de uma frase; sem ela, o ranqueamento é opinião sem rastro.
- Não atribua percentuais, valores em dinheiro ou CVSS a ameaças de desenho: não há fonte validada para isso aqui.
