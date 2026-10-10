---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Propõe separar camada de UI (View e ViewModel, com relação 1:1) e camada de dados (Repository e Service), com camada de domínio apenas se houver regra reutilizada.
2. Diz que o repositório é a fonte de verdade, que repositórios não conhecem uns aos outros, que services não têm estado e que a View não contém lógica de negócio nem parsing de JSON (aponta as telas atuais que chamam `http` e parseiam na tela como o problema).
3. Adapta-se ao que o projeto já usa: mantém o Provider (o ViewModel pode ser um `ChangeNotifier` exposto via Provider) e não impõe troca de gerenciador de estado ou de pacote de rotas; trata a preferência por `provider`, `go_router` ou outro pacote como opinião.
4. Dá um caminho incremental (por exemplo migrar uma tela por vez, começando por um service e um repositório) e uma forma de verificar (`flutter analyze` e `flutter test`, confirmando na versão instalada), sem afirmar que executou.
5. Fica no Flutter e no Dart; não traz termos de SwiftUI ou Swift como se fossem do problema.
FAIL if qualquer um ocorrer: aciona a skill `swift-ios-review`; afirma que `go_router` ou outro pacote é "preferido em 90% dos apps" ou outro número sem fonte; manda reescrever o app inteiro de uma vez; coloca lógica de negócio na View; afirma ter compilado ou testado.
