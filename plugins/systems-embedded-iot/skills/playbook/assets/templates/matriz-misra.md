# Matriz de configuração MISRA / análise estática - <projeto>

Fontes: V-14 (MISRA C:2023 reference da MathWorks; CERT SIG31-C), V-58 (cppcheck), V-09 (Zephyr). **O texto da MISRA é pago e não é reproduzido aqui**: a matriz registra decisões, não regras. Não cite número de regra sem reler a versão. O plugin não afirma conformidade.

- **Edição adotada:** [MISRA C:2012 (com corrigenda e emendas) / MISRA C:2023, que consolida a 2012 com corrigenda 1 e 2 e emendas 1 a 4]
- **Categorias consideradas:** [mandatory / required / advisory] · **Diretivas e regras listadas separadamente:** [sim]
- **Ferramentas e versões:** cppcheck [versão] com addon MISRA [comando conferido na documentação instalada]; compilador [GCC/Clang versão]; clang-tidy [versão; toolchain cruzado: Não verificável até testar]
- **Regras que o cppcheck não trata (1.1 e 1.2) -> verificadas pelo compilador do alvo:** [confirmado? sim/não]

| Regra / diretiva (ID da edição adotada) | Categoria | Coberta por (cppcheck / compilador / clang-tidy / revisão manual / nenhuma) | Estado (conforme / desvio / não aplicável) | Razão do desvio ou NA | Aprovador | Evidência |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

## Regras do projeto não derivadas da MISRA (política própria)

| Política | Origem | Verificação |
| --- | --- | --- |
| Sem alocação dinâmica após init (ISR nunca aloca) | P-09 / V-16 | grep + revisão |
| `volatile` não é atomicidade | V-14 | revisão |
| Sem código comentado/inalcançável | V-09 | revisão |

## Observações

- Zephyr se descreve como subconjunto de MISRA-C 2012 e declara IEC 61508 como **meta**, não certificação (V-60).
- Desvios têm razão escrita e aprovador; "ignorar aviso" sem razão é achado.
- Análise estática confirma propriedades estáticas, não comportamento temporal nem de hardware.
