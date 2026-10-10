# Fontes e rastreabilidade: da pergunta ao registrador citado

Uso: consulta da skill `datasheet-first`. Fontes: V-23 (checklist "datasheet primeiro", relatos do thread; classe B de 5), V-48 (SVD, CMSIS-SVD e svd2rust), V-47 (embedded-hal 1.0), V-16 (regras STM32 HAL), V-28 (revisão por contexto), lidas em 2026-10-10.

Sumário: [Hierarquia de fontes](#hierarquia-de-fontes) · [Tabela elemento-fonte](#tabela-elemento-fonte) · [Como verificar um nome](#como-verificar-um-nome) · [Divergências](#divergências) · [Ler PDF grande](#ler-pdf-grande) · [Checklist de cinco itens](#checklist-de-cinco-itens)

## Hierarquia de fontes

Ordem de confiança para um fato de hardware (do mais forte ao mais fraco):

1. **Errata** da variante e da revisão do silício: o que o manual não diz ou diz errado.
2. **Reference manual** (mapa de registradores, semântica dos campos, sequência de inicialização).
3. **Datasheet** (características elétricas, pinagem, tempos, limites absolutos).
4. **SVD / header do fabricante** na versão que o projeto usa (nomes, endereços, máscaras). O SVD descreve registradores mapeados, campos de bits e interrupções de dispositivos Arm Cortex e é mantido pelos fabricantes, distribuído em Device Family Packs (V-48).
5. **Documentação do framework** na versão instalada (HAL, ESP-IDF, Zephyr).
6. **Código de exemplo** do fabricante: útil como exemplo de uso, não como fonte de semântica.
7. **Memória do modelo, blog, fórum**: nunca fonte de um nome de registrador, de um endereço ou de um tempo. Serve para levantar hipótese e perguntar.

Regra de precedência: material do projeto vence a memória do modelo (V-62, embedded-systems-architect). Se a fonte do usuário contradiz o que você "sabe", cite a fonte do usuário, rotule "a verificar" se ela mesma for secundária e pergunte.

## Tabela elemento-fonte

Uma linha por elemento de hardware tocado pelo código. Os campos entre `<>` são preenchidos com o que o usuário forneceu; a tabela vazia é válida e mostra o que falta.

| Elemento | Valor usado | Fonte (arquivo) | Seção/página | Versão | Verificação | Rótulo |
| --- | --- | --- | --- | --- | --- | --- |
| Endereço I2C (7 bits) | `<valor>` | `<datasheet do componente>` | `<seção>` | `<rev.>` | pino ADDR0 na placa: esquemático `<sheet>` | Verificado se os dois conferem |
| Registrador `<NOME>` | `<offset>` | `<SVD ou RM>` | `<seção>` | `<versão do SVD>` | `grep -nw` no header: linha colada | Verificado |
| Campo `<CAMPO>` | `<máscara/posição>` | `<RM>` | `<seção>` | `<rev.>` | idem | Verificado |
| IRQ `<NOME>_IRQn` | número | `<header de dispositivo>` | n/a | `<versão do pack>` | `grep -nw` | Verificado |
| Tempo de conversão | `<ms>` | `<datasheet>` | `<tabela>` | `<rev.>` | usado no timeout? | Verificado |
| Erro conhecido | descrição | `<errata>` | `<ID>` | `<rev. silício>` | contorno no código? | Verificado |

Linha sem fonte aberta não entra como fato. Rotule a linha `PENDENTE` e coloque a pergunta no relatório.

## Como verificar um nome

1. Header C do fabricante: `grep -nw "<NOME>" <caminho do header da variante>`; use `-w` para palavra inteira e leia a linha de definição, não só o uso.
2. SVD (XML): `grep -n "<name>NOME</name>" <arquivo>.svd`; depois leia as linhas vizinhas para `<addressOffset>` e `<bitOffset>`/`<bitWidth>`.
3. Crate PAC gerado por svd2rust: o PAC reflete o SVD usado na geração (svd2rust gera as structs de mapa de registradores a partir do SVD; V-48). Registre a versão do PAC e a origem do SVD; PAC desatualizado repete erro de SVD antigo.
4. ESP-IDF: `grep -rn "<NOME>" $IDF_PATH/components/soc/<chip>/include` para registradores; para funções, a documentação da versão instalada. Zephyr: o devicetree e os headers da board/SoC da versão do projeto; devicetree não foi lido nesta rodada (lacuna), então confirme no código-fonte da versão.
5. Nome não encontrado no material fornecido: não use; peça o arquivo certo.

## Divergências

- SVD contra reference manual: **achado**, não decisão do modelo (V-48). Relate as duas fontes, o campo em disputa e a pergunta. Fabricantes corrigem SVD entre versões do pack; manuais têm errata.
- Header contra SVD: idem.
- Código de exemplo contra manual: vale o manual, e o exemplo vira achado se a diferença for funcional.
- Datasheet de uma revisão do silício e placa com outra revisão: a errata da revisão real vale.

## Ler PDF grande

O Claude Code lê PDF por páginas (`Read` com o parâmetro de páginas, no máximo 20 por chamada) e PDFs com mais de 10 páginas exigem o intervalo. Para manuais com milhares de páginas: leia o sumário, localize o capítulo do periférico e leia só ele, e registre as páginas lidas na tabela. Não resuma o manual inteiro de memória. Se existir `pdftotext` na máquina do usuário, a extração para texto permite `Grep` (Suposição: ferramenta instalada pelo usuário; não a instale por conta própria).

## Checklist de cinco itens

Versão reescrita do checklist "datasheet primeiro" (V-23):
1. Nome de registrador e de função HAL vem de header, SVD ou datasheet **citado com seção**.
2. Sem fonte, pare e pergunte.
3. Variante exata do chip e revisão do silício confirmadas.
4. Documento proprietário ou sob NDA não sai da máquina sem decisão do usuário.
5. Relate o que foi compilado, simulado e testado em hardware, separadamente.

Contexto: o thread de origem (V-23) mostra agentes genéricos inventando registradores e chamadas HAL de outra família. Alegações de privacidade feitas no thread sobre um produto comercial não são fato verificado e não devem ser repetidas.
