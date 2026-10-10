# Ficha de ação externa

Use antes de qualquer ação com efeito fora dos arquivos locais: assinar com certificado, notarizar, publicar release, abrir PR no `winget-pkgs`, aceitar EULA ou termos, criar certificado ou chave, instalar ferramenta de terceiros, rodar instalador ou o app. A fábrica preenche a ficha e para; quem confirma e executa é o usuário. A confirmação vale para esta ficha, não para outras.

| Campo | Valor |
| --- | --- |
| Ação | [o que será feito] |
| Conta ou identidade envolvida | [conta, certificado, repositório; sem colar segredos] |
| Artefato e versão | [arquivo, hash SHA256 se houver, versão] |
| Destino | [Store, GitHub Releases, winget-pkgs, servidor de update] |
| Ambiente | [máquina, SO, shell, versão da ferramenta] |
| Comando exato | [conferido com `--help` ou `/?` da versão instalada; ou "a conferir pelo usuário"] |
| Efeito | [o que muda no mundo] |
| Reversibilidade | [reversível localmente | irreversível na prática (PR público, release publicada, aceite de termos)] |
| Risco | [o que pode dar errado] |
| Pré-condições verificadas | [lista, com evidência] |
| Quem executa | Usuário |
| Confirmação | "confirmado pelo usuário em [AAAA-MM-DD] para esta ação" (preenchido só pelo usuário) |

Segredos: nunca em argumento, nunca na ficha. Use store do sistema, KSP ou nuvem, ou o cofre do CI.

## Exemplo preenchido (notarização)

- Ação: submeter `MeuApp.zip` à notarização da Apple.
- Conta: Apple Developer do titular (credenciais no chaveiro, não coladas aqui).
- Comando: a conferir com `xcrun notarytool --help` (sintaxe não verificada pela fábrica).
- Reversibilidade: o envio fica registrado no serviço; o ticket só existe após aprovação.
- Quem executa: usuário.
