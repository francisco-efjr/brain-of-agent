# Checklists de arquitetura por plataforma

Verificado em 2026-10-10. Fontes: V-07 e V-59 (Android, oficiais), V-10 e V-11 e V-12 (Compose), V-26 (Flutter, oficial), V-27 e V-47 (Flutter, com ressalvas), V-23 e V-19 (SwiftUI), V-31 e V-33 e V-81 (RN/Expo). Redação própria. Os trechos de código são esboços originais deste plugin, marcados **Inferido**: confirme APIs na versão do projeto.

Regra geral: cada item vira achado só com evidência (`arquivo:linha`). Item sem evidência de violação não é relatado. "Convenção local do repositório" vence preferência de autor.

## Android (Kotlin, Compose)

### Camadas e estado (V-07, oficial)

1. **Separação de responsabilidades.** Activity/Fragment/Composable só tratam UI e interação com o SO.
2. **Fonte única de verdade com dono único** para cada tipo de dado.
3. **Fluxo unidirecional.** Estado desce, eventos sobem.
4. **Pelo menos duas camadas**: UI e dados; domínio é opcional (use case só quando houver lógica reutilizada).
5. **Repositório por tipo de dado**, expondo leitura observável; a UI não chama API de rede direto.
6. **Main-safe.** Chamadas bloqueantes saem da thread principal (dispatcher injetado, para testar).
7. **`Context` fora da regra de negócio.** `Context` só em componentes do app (V-07); string de UI vem de recurso resolvido na camada de UI.
8. **Hilt** é a DI recomendada pela página; se o projeto usa Koin ou DI manual, siga o projeto.
9. Offline-first: banco local como fonte de verdade "tipicamente" (V-07) → detalhe em [offline-sync.md](offline-sync.md).

### Compose: estado e efeitos (V-10, autor reconhecido, classe B)

- **Um dono por estado**, o mais baixo possível na árvore; mudar o dono só com evidência.
- **Efeito com chave semântica** e ciclo de vida do dono. Erro típico: `LaunchedEffect(Unit)` que deveria depender de um ID.
- **Tela em três partes**: ligação de dados (Route), state holder (ViewModel ou classe de estado) e conteúdo imutável com callbacks.

```kotlin
@Composable
fun NotesRoute(viewModel: NotesViewModel = hiltViewModel()) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    NotesScreen(state = state, onAddClick = viewModel::onAddClick)
}

@Composable
fun NotesScreen(state: NotesUiState, onAddClick: () -> Unit) { /* só renderiza e emite eventos */ }

// efeito com chave semântica: recarrega quando o ID muda
LaunchedEffect(noteId) { viewModel.load(noteId) }
```

Sem evidência, não relate anti-padrão inferido (V-10): "sem achados" é resposta válida.

### Layouts adaptativos (V-12, skill oficial `android/skills`)

Pré-requisitos da skill: projeto em Compose e Navigation 3 (senão, ela sugere skills de migração). `NavigationSuiteScaffold` para navegação; multipainel via `SceneStrategy`, e a skill proíbe `ListDetailPaneScaffold`/`SupportingPaneScaffold` nesse fluxo; `Grid` experimental só com confirmação do usuário (depende de Compose recente); testes de screenshot não têm referência atualizada sem revisão humana. Conferir tudo contra as versões do projeto.

## Flutter (V-26, oficial)

1. Camadas **UI** (View, ViewModel) e **dados** (Repository, Service); domínio opcional.
2. **View ↔ ViewModel 1:1**; a View não tem lógica de negócio.
3. **Repositório é a fonte de verdade**; repositórios não conhecem uns aos outros; **services sem estado**.
4. Trabalho fora de `build()`, `setState` na menor subárvore (V-29): detalhes em `mobile-performance-diagnosis`.

Processo de 8 passos de V-27 (B, 7; use só o processo): modelos imutáveis → services → repository → use case (opcional) → ViewModel (a skill usa `ChangeNotifier`) → View (a skill usa `ListenableBuilder`) → registro em DI → testes. Critério de parada para o passo 8: todos os testes novos passam e nenhum teste existente foi enfraquecido ou removido.

Cache de repositório corrigido (o exemplo de V-27 ignorava o ID):

```dart
class UserRepository {
  UserRepository(this._api);
  final UserApiClient _api;
  final _cache = <String, User>{};

  Future<User> getUser(String id) async {
    final cached = _cache[id];
    if (cached != null) return cached;
    final user = await _api.fetchUser(id); // erro propaga; trate no ViewModel
    _cache[id] = user;
    return user;
  }

  void invalidate(String id) => _cache.remove(id);
}
```

V-47 (instruções da comunidade, B, 5) serve de checklist de PR, não de norma: modelos imutáveis (`freezed`/`built_value`, com aviso de build lento), testes de serviço, repositório e ViewModel, fakes por entrada e saída. Descarte "go_router é preferido por 90% dos apps" (sem fonte) e trate `provider` como preferência pessoal.

## SwiftUI / iOS (V-23 e V-19, classe B e A)

1. **Ordem de membros** consistente no arquivo; a **convenção local prevalece**.
2. **Subviews como tipos `View`** (não funções soltas retornando views gigantes); **ações fora do `body`**; raiz de `body` estável.
3. **`@Observable` em `@State`** no iOS 17+; `@StateObject`/`ObservableObject` no iOS 16 ou inferior: **leia o deployment target antes**.
4. Divida arquivos de view acima de ~300 linhas (guia, não lei).
5. "MV antes de MVVM" é opinião do autor de V-23. Se o repositório usa MVVM ou TCA, siga-o (S-08). TCA aparece em V-43 (classe C): só o padrão de subagentes e arquivo de plano por feature.
6. Revisão de código SwiftUI e concorrência: use a skill `swift-ios-review`.

## React Native e Expo (V-31, V-33, V-36, V-81)

- Prioridades da skill Vercel (B, 7; licença conflitante, destilado): listas **crítico**; animação, navegação e UI **alto**; estado, renderização e monorepo **médio**; configuração **baixo**. Preferência da skill, não erro: `Pressable` em vez de `TouchableOpacity`.
- Expo Router (V-33): rotas só em `app/` (ou `src/app/` no template, V-36; siga o projeto); rota para `/` obrigatória (pode estar em grupo); nomes kebab-case; `presentation: "modal"` para modais; no **SDK 56+** importar de `expo-router/react-navigation` e usar `headerLargeTitleEnabled` no lugar de `headerLargeTitle` (depreciado). Confirme o SDK instalado antes de aplicar.
- Sem Expo Router (V-81): `@react-navigation/native` com `react-native-screens` e `react-native-safe-area-context`; em Expo, `npx expo install` casa versões com o SDK; Android: `react-native-screens` exige configurar `RNScreensFragmentFactory` em `MainActivity.onCreate`; gesto de voltar preditivo ainda não suportado (`android:enableOnBackInvokedCallback="false"`); mínimos RN 0.72.0, Expo 52, TypeScript 5.0.0. Reconfira na versão atual.
- Estado e dados em RN fora do Expo Router: **sem fonte validada** (lacuna 12); rotule Inferido.
- Não edite `ios/` nem `android/` à mão em projeto Expo gerenciado; módulo nativo exige development build (V-36).

## O que não relatar

- Estilo ou preferência pessoal sem regra de plataforma.
- Migração de arquitetura "porque é mais moderno".
- Problema que só existe se a versão for diferente da lida no projeto.
