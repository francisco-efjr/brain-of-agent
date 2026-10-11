# Notas — eval-10-chatbot-rag-banco (with_skill)

## Arquivos da skill lidos (skills/qa)

- `SKILL.md` (inteiro)
- `references/ia-e-llm.md` (inteiro; base principal: diagnóstico de RAG, OWASP LLM 2025, protocolo de repetição e incerteza, suíte mínima em pytest/promptfoo)
- `references/estrategia.md` (inteiro; matriz de risco, níveis, shift-right, critérios de saída)
- `references/dominios.md` (inteiro; seções de pagamentos, PIX, SaaS multi-tenant, documentos brasileiros — CPF `529.982.247-25` veio daqui)
- `references/seguranca.md` (inteiro; LGPD para QA, OWASP, allowlist/exfiltração)
- `references/dados-ambientes-ci.md` (inteiro; massa sintética, virtualização, gates que não ficam verdes por vácuo)
- `assets/templates/plano-de-teste.md` (lido; não preenchi o template completo porque o pedido era "como eu testo isso?", resposta em formato de conversa)

Não abri: `design-de-testes.md`, `automacao-*.md`, `performance.md`, `acessibilidade.md`, `mobile.md`, `unitarios-e-integracao.md`, `requisitos-e-bdd.md`, `bugs-e-relatorios.md`, `processo-e-gestao.md`, os outros templates e os scripts (`documentos_br.py` etc.; não os executei, usei só o CPF de exemplo da referência e escrevi a validação de CPF/Luhn no harness).

Não li o conteúdo da pasta `evals/`. Ao criar a pasta de saída, um `ls` do diretório pai exibiu os nomes `eval_metadata.json`, `with_skill`, `without_skill`; não abri nenhum deles.

## O que executei

- `python3 -m unittest -v test_avaliar`: 16 testes, todos passam (Python 3.14, só biblioteca padrão; `pytest` não está instalado, por isso usei `unittest`).
- `avaliar.py` contra os três bots falsos com `--n 10`: bom 180/180 e exit 0; ruim reprovado (falha crítica em 10 de 18 casos) e exit 1; instável reprovado; `--filtro` sem match devolve exit 2.
- Nenhuma requisição de rede, nenhum LLM real.

## Incertezas

- **Escopo do bot**: assumi FAQ somente leitura, sem acesso a conta nem ferramentas. Se tiver, a resposta muda bastante (teste de agente, autorização por cliente, estado final). Está nas perguntas no fim da resposta.
- **Regex como oráculo**: é a 1ª camada. A primeira versão do harness tinha um falso positivo (`solicita_credencial` pegava "Nunca compartilhe senha" da própria FAQ) e um falso negativo (`realizado` não casava com `realizei`); os testes do harness pegaram os dois e corrigi. Outros falsos positivos prováveis: a heurística de cartão (13 a 19 dígitos + Luhn) pode acusar telefone com DDI por acaso (cerca de 10% das sequências passam no Luhn); a heurística de credencial depende de redação e precisa de revisão humana dos casos sinalizados.
- **Dados sintéticos**: FAQ, tarifas, telefones e limites do "Banco Exemplo" são inventados para o demo. O Pix noturno de R$ 1.000,00 foi inspirado em `dominios.md`, mas não é requisito do banco do usuário.
- **Bots falsos**: `bot_bom` imita o comportamento desejado com regras simples (remove comentário HTML do documento, filtra interno e não vigente). Isso não mostra que um LLM faria o mesmo; só mostra que o harness distingue um comportamento do outro.
- **Limiar de 80%** (`--min-taxa`) é placeholder; a referência diz que 90% ou 95% também não são padrões universais.
- **Regulação**: não afirmei nenhuma norma específica de SAC, Banco Central ou ANPD; mandei confirmar com compliance e jurídico. A menção à lista OWASP LLM 2025 segue `ia-e-llm.md` e não foi checada de forma independente (sem rede).
- **Tamanho da resposta**: ficou longa para uma pergunta aberta. Mantive por ser um domínio de risco alto e pedir plano + artefato; poderia ser cortada nas seções 2 e 6 se o usuário quiser só o essencial.
- A resposta não cita número de casos ideal como regra: "50 a 100" é ponto de partida meu, não vem da skill.
