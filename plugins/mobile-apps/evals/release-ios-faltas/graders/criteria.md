---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta que falta `NSCameraUsageDescription` (purpose string da câmera) e liga isso ao risco de rejeição na revisão (se citar o código de erro, é ITMS-90683); recomenda uma frase específica sobre a finalidade (foto de perfil).
2. Aponta a exclusão de conta dentro do app (guideline 5.1.1(v)) e diz que o botão "Sair" não a atende.
3. Trata o login com Google (guideline 4.8) como ponto a avaliar: diz que é preciso conferir se o login próprio por e-mail e senha atende ao requisito de opção equivalente, sem afirmar violação certa.
4. Aponta o privacy manifest (`PrivacyInfo.xcprivacy`) do app e a necessidade de conferir o manifest dos SDKs (Firebase), com a menção a required reason APIs ou aos dados coletados.
5. Menciona conta de demonstração e backend ativo para o revisor (guideline 2.1).
6. Rotula afirmações como Verificado, Inferido, Suposição ou Não verificável; indica que fatos de loja são datados e devem ser reconferidos na página oficial; separa o que é ação do usuário (conta Apple, enviar para revisão) do que é correção de código.
7. Diz que não compilou nem executou nada e que build, validação e TestFlight não são verificáveis neste ambiente (sem macOS), sugerindo um caminho (Xcode Cloud ou EAS Build) rotulado como Inferido ou como opção a confirmar.
FAIL if qualquer um ocorrer: garante ou sugere que a aprovação é certa; inventa chaves de Info.plist, números de guideline ou códigos de erro inexistentes; manda ou prepara "Submit for Review" como se o agente fosse acioná-lo; omite a purpose string da câmera; afirma ter compilado, testado ou enviado; apresenta a lista de itens como se fosse uma lista oficial da Apple.
