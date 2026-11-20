# Padrões e antipadrões — índice

Os antipadrões estão nas seções **Proibido** de cada `regras-*.md` (IDs com `-P`) e os sinais de alerta nas seções **Sinais de alerta** (IDs com `-S`). Os mais caros, com o padrão que os substitui:

| Antipadrão | Padrão no lugar | Regras |
| --- | --- | --- |
| Aceitar "pronto" pelo relato do agente ou pelo verde da ferramenta | Medir na fonte e pelo comportamento real | VER-03, VER-04, VER-P02 |
| Teste e mock escritos por quem fez o código | Verificador independente do autor | VER-02, VER-P01 |
| Pedido vago ou de uma frase para trabalho grande | Quatro partes e o que a máquina não sabe | PED-01, PED-02, PED-P01 |
| Exclusão com lista de proteção vazia | G4 com contagem esperada e aborto | SEG-19, SEG-P05 |
| Modo sem confirmações fora da jaula | Jaula e permissões em três colunas | SEG-06, SEG-07, SEG-P01 |
| Memória só no contexto ou no fornecedor | Três gavetas em arquivos versionados | CTX-04, CTX-11, CTX-P01 |
| Vários agentes para ganhar velocidade | Um agente no caminho crítico; paralelo só em lote independente | ENG-18, ENG-P08 |
| Concluir com uma rodada de benchmark | Teste próprio, repetido e às cegas | AVA-02, AVA-03, VER-P03 |
| Erro engolido como sucesso | Registro técnico e alerta visível | OPS-10 |
| IA no processo quebrado | Ciclos curtos e travas antes de acelerar | ORG-P02, OPS-04 |
