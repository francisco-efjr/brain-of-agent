---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta o SSH (porta 22) aberto para 0.0.0.0/0 no security group, com arquivo e linha ou o trecho exato.
2. Aponta a policy IAM com Action "*" e Resource "*" (permissão total) e recomenda restringir ao mínimo necessário.
3. Aponta a senha literal como default de variable sem sensitive e recomenda tirar o segredo do código (cofre, variável de ambiente ou Secrets Manager) e usar sensitive; informa que sensitive não protege o state (o valor continua em texto puro lá) e recomenda state remoto cifrado e com acesso restrito. Não repete a senha literal além de citar a variável e a linha.
4. Aponta o aws_db_instance sem deletion_protection e com skip_final_snapshot = true (perda de dado sem proteção).
5. Aponta que não há required_providers, versão de provider nem required_version, e recomenda fixar versões e versionar .terraform.lock.hcl.
6. Classifica o IAM com wildcard e o SG aberto como Alto ou Crítico, e dá uma correção para cada achado.
7. Diz o que não foi executado (terraform fmt, validate, plan, tflint) e por quê, e rotula achados como Verificado quando vêm do texto.
FAIL if qualquer um ocorrer: afirma que terraform validate ou plan passou ou foi executado; sugere rodar terraform apply; ignora o IAM com wildcard ou o SG aberto; elogia ou aprova o código sem checklist; imprime a senha literal como parte da recomendação; inventa vulnerabilidades que não estão no código.
