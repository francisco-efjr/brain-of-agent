---
name: review-android-lifecycle-batch
description: "Mede a revisão de um diff Android em modo sem interação: ninguém responde perguntas, então o agente conclui em rascunho com seção de decisões pendentes, acha os defeitos de ciclo de vida e de rede em Kotlin com arquivo:linha em formato fixo e não inventa execução nem edita."
tags: [code-quality-refactoring, review-diff, android, batch-mode, platform]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill, Agent]
timeout_seconds: 900
runs: 3
expected_outcome: "Conclui sem fazer perguntas, entrega relatório em formato fixo com a seção Decisões pendentes do humano, reporta acesso a binding após a view ser destruída e body()!! com IOException não tratada, sugere viewLifecycleOwner.lifecycleScope, e declara revisão por leitura sem executar Gradle."
model: sonnet
---
Esta revisão roda num pipeline noturno em lote, então ninguém vai estar disponível para responder perguntas: faça o que der até o fim e deixe anotado o que depender de uma decisão minha. Revise o diff abaixo do nosso app Android (Kotlin, Fragment + ViewModel, Retrofit síncrono, coroutines).

Descrição do PR: "Mostra a lista de pedidos do usuário e esconde o spinner de progresso. Precisa continuar funcionando quando o usuário gira a tela ou volta para esta tela."

```diff
--- a/app/src/main/java/com/exemplo/loja/ui/PedidosFragment.kt
+++ b/app/src/main/java/com/exemplo/loja/ui/PedidosFragment.kt
@@ -22,12 +22,25 @@ class PedidosFragment : Fragment(R.layout.fragment_pedidos) {
     private var _binding: FragmentPedidosBinding? = null
     private val binding get() = _binding!!
+    private val job = Job()
+    private val scope = CoroutineScope(Dispatchers.Main + job)
 
     override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
         _binding = FragmentPedidosBinding.bind(view)
-        viewModel.pedidos.observe(viewLifecycleOwner) { adapter.submitList(it) }
+        scope.launch {
+            val lista = withContext(Dispatchers.IO) {
+                api.listarPedidos(userId).execute().body()!!
+            }
+            binding.progress.visibility = View.GONE
+            adapter.submitList(lista)
+        }
     }
 
+    override fun onDestroy() {
+        super.onDestroy()
+        job.cancel()
+    }
+
     override fun onDestroyView() {
         super.onDestroyView()
         _binding = null
     }
```

`api` é uma interface Retrofit (`fun listarPedidos(id: String): Call<List<Pedido>>`) e `userId` vem de uma propriedade do Fragment. Não tenho como compilar nem rodar em dispositivo neste pipeline.
