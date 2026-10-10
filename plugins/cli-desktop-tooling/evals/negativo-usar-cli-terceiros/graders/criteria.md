---
type: llm
---

PASS if a resposta final dá um comando da AWS CLI plausível para listar buckets S3 (por exemplo `aws s3api list-buckets` com `--output json`, com filtro por região via a opção da CLI para região do bucket quando disponível na versão instalada, ou via consulta por bucket com `get-bucket-location`), mostra como salvar a saída em arquivo (redirecionamento ou `--query` mais redirecionamento) e pode avisar que a listagem de buckets do S3 é global e que o filtro por região depende da versão da CLI, sugerindo conferir `aws s3api list-buckets help`. A resposta é direta e não revisa design de CLI, nem fala de exit codes, TUI, desktop ou instaladores.
FAIL if a resposta trata o pedido como revisão ou projeto de uma CLI, ou inventa flags inexistentes sem ressalva de conferir a ajuda da versão instalada.
