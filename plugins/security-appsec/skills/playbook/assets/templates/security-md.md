# Modelo de SECURITY.md e security.txt

Fonte: V-40 (OWASP Vulnerability Disclosure Cheat Sheet, CC BY-SA 4.0, destilado) e RFC 9116 para o `security.txt`. Safe harbor pede orientação jurídica: o texto abaixo é ponto de partida, não parecer. Pareia com o grupo RV do SSDF (V-26). Processo interno de triagem e SLA por severidade não são cobertos pela fonte.

## SECURITY.md

```markdown
# Política de segurança

## Como relatar uma vulnerabilidade
Envie o relato por <canal privado: aviso de segurança privado do repositório ou e-mail <endereço>>. Não abra issue pública com detalhes de exploração.
Inclua: componente e versão, passos mínimos para reproduzir, impacto percebido, evidência com dados mascarados.

## O que esperar
- Confirmação de recebimento em até <N> dias úteis.
- Avaliação inicial e classificação de severidade em até <N> dias úteis.
- Meta de correção por severidade: <alta: N dias; média: N dias; baixa: próxima release> (ajuste à sua realidade).
- Divulgação coordenada: publicamos o aviso depois da correção, com crédito a quem relatou, se desejar.

## Escopo
- No escopo: <aplicações, domínios, repositórios>.
- Fora do escopo: <negação de serviço, engenharia social, testes em dados de terceiros, serviços de fornecedores>.

## Safe harbor
<Texto aprovado pelo jurídico. Exemplo de estrutura: não tomaremos ação legal contra pesquisa feita de boa-fé, dentro do escopo, sem acesso a dados além do mínimo necessário para provar o defeito e sem divulgação antes da correção. Fonte de modelos: disclose.io (revisão jurídica obrigatória).>

## Versões suportadas
<tabela de versões com suporte a correções de segurança>
```

## /.well-known/security.txt (RFC 9116)

```text
Contact: mailto:<endereço-de-seguranca>
Expires: <data ISO 8601 futura, renovada periodicamente>
Preferred-Languages: pt-BR, en
Policy: <URL da política de segurança>
```

`Contact` e `Expires` são os campos mínimos (V-40). Mantenha `Expires` atualizado: arquivo vencido perde a validade. Outros campos: confira o RFC 9116 antes de acrescentar.

## Depois de publicar

- Defina quem monitora o canal e o substituto nas férias.
- Teste o fluxo com um relato fictício antes de divulgar.
- Pedido de relato recebido: use `achado-restrito.md` para registrar sem expor detalhes em canal público.
