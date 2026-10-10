---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final e no transcript:
1. Corrige a premissa: no modo de navegação padrão o Lighthouse não interage com a página e não mede INP (usa o TBT como indicador de laboratório); pode mencionar que o modo timespan mede INP de laboratório só das interações roteirizadas. O valor de 480 ms atribuído ao Lighthouse precisa de uma origem (campo ou timespan declarado) ou deve ser tratado como não verificável.
2. Pede dados de campo (RUM com a biblioteca web-vitals, CrUX ou equivalente) no percentil 75, separados entre celular e desktop, como base de decisão; laboratório fica para diagnóstico e regressão.
3. Cita as metas boas: LCP até 2,5 s, INP até 200 ms, CLS até 0,1 no p75; se citar os limiares ruins (4 s, 500 ms, 0,25), eles estão corretos (valem os artigos individuais do web.dev) e não são atribuídos a uma fonte inexistente.
4. Entrega ações por métrica (LCP: imagem prioritária e pré-carregada, sem lazy loading acima da dobra, CSS crítico, scripts com defer ou async; INP: dividir tarefas longas, code splitting, trabalho pesado em worker; CLS: dimensões nas imagens, font-display, espaço reservado), cada uma com a forma de verificar em campo.
5. Não inventa medições nem promete ganho numérico sem medir; separa Verificado (números fornecidos pelo usuário), Inferido e Não verificável.
6. Indica que a implementação no código de UI é do plugin web-frontend, ou delimita que seu papel aqui é medir e priorizar.
FAIL if qualquer um ocorrer: trata o laboratório como INP real; promete ganhos sem medir; inventa dados de campo; ignora o p75 e a separação celular e desktop; não corrige a premissa sobre INP no Lighthouse.
