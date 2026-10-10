# Checklist de entrega de mudança de banco

Mudança: [título] · Ambiente/revisão: [commit, versão do SGBD] · Data: [AAAA-MM-DD]
Adaptado de Brain of Agent, `dados-e-migracoes.md` (MIT, © 2026 Brain of Agent contributors).

Marque cada item: Verificado (evidência), Inferido, Suposição, Não verificável ou Não aplicável.

| Item | Estado | Evidência ou limitação |
| --- | --- | --- |
| Schema, consumidores, volume e versão observados | | |
| Constraints e precisão refletem invariantes de negócio (dinheiro em NUMERIC, tempo com fuso) | | |
| Concorrência testada com coordenação e transação efetiva | | |
| Plano/consulta analisado em dados representativos, sem exposição | | |
| Migração suporta versões coexistentes e lote retomável | | |
| Locks, espaço, duração e interrupção têm critério definido | | |
| Backup e restauração validados em ambiente permitido | | |
| Rollback documenta perda potencial e compatibilidade | | |
| Dados pós-migração comparados por contagem e invariantes | | |
| Segurança: SQL parametrizado, papel mínimo, segredos fora do repositório | | |

## Resultado

Entregue: [artefatos e caminhos] · Verificado: [..] · Inferido/Suposição: [..]

## O que falta para concluir

[Itens que dependem de acesso, versão, volume, plano ou decisão do usuário.]
