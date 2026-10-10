# Achado em canal restrito

Modelo para registrar e comunicar uma vulnerabilidade sem expor passos em canal público (brain QA, Inferido; V-40). Use em tracker com visibilidade limitada ou no aviso privado de segurança do repositório. Ticket público leva título genérico (por exemplo "Ajuste de autorização em pedidos"), sem passos, payload nem URL afetada. Falha em sistema de terceiro achada por acaso: pare e reporte pelo canal do dono (`security.txt`, RFC 9116); não teste mais.

## Ficha

**Título (restrito):** <componente> - <tipo de falha> - <condição>
**Título público (genérico):** <ajuste de segurança em ...>
**Severidade:** <Alta | Média | Baixa> com justificativa de impacto no negócio. CVSS como referência (v4.0 desde novembro de 2023; v3.1 ainda comum em bases de CVE; faixas 0,1-3,9 baixa, 4,0-6,9 média, 7,0-8,9 alta, 9,0-10,0 crítica, conferidas na especificação CVSS v4.0 do FIRST em 2026-10-10; data e uso das versões: Inferido do brain). Some o impacto de negócio: o CVSS não sabe que o endpoint expõe dados de saúde.
**Estado da evidência:** <hipótese | estático suportado | reproduzido em ambiente autorizado>
**Ambiente, versão e contas de teste:** <...> (dados sintéticos)
**Pré-condição:** <o que o atacante precisa>
**Passos mínimos:** 1. <...> 2. <...>
**Esperado × obtido:** <...>
**Impacto:** <dados, usuários, tenants afetados>
**Evidência (mascarada):** <requisição e resposta com tokens, cookies e dados pessoais removidos; ID de correlação>
**Correção sugerida:** <na defesa primária>
**Teste de regressão:** <que falha antes e passa depois; no mesmo PR da correção>
**Reteste:** <quem, quando, como>

## Regras de manuseio

- Evidência sem token, senha, cookie ou dado pessoal real; HAR e screenshot levam cookies e dados: mascare antes de anexar.
- Quem pode ver: <lista curta>. Não repasse por chat público, e-mail aberto ou issue.
- Se um segredo for parte do achado: revogar e rotacionar primeiro; não reproduzir o valor.
- Divulgação coordenada: publicar aviso depois da correção (ver `security-md.md`).
- Quem recebe o relato de terceiros: confirmar recebimento, não prometer prazo que o time não cumpre, não ameaçar nem culpar quem reportou.
