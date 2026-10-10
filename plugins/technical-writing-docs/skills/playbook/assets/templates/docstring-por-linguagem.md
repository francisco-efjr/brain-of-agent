# Template: docstrings por linguagem

Fontes: V-33 (Python), V-34 (JS/TS), V-35 (Rust), V-36 (Java; página do JDK 21). Em redação própria; confira a versão da linguagem e o dialeto que as ferramentas do projeto leem. Todo exemplo de documentação pública é teste (doctest, `cargo test --doc`): execute com autorização do usuário ou marque "não executado". Detalhes e armadilhas: `references/codigo-e-api.md`.

## Python (estilo Google, PEP 257)

````python
def funcao(param: tipo) -> retorno:
    """Resumo de uma linha com até 80 caracteres e ponto final.

    Descrição só do que a assinatura e os tipos não dizem.

    Args:
        param: O que é e restrições.

    Returns:
        O que volta (omita a seção se só retorna None).

    Raises:
        ValueError: Quando [condição da interface, não de uso incorreto].

    Examples:
        >>> funcao(entrada)
        saida_esperada
    """


class Exemplo:
    """Resumo da classe.

    Attributes:
        nome: O que guarda.
    """

    def __init__(self) -> None:
        ...
````

Linha em branco depois da docstring de classe (PEP 257).

## TypeScript (TSDoc; confira se o projeto usa TSDoc ou JSDoc)

````ts
/**
 * Resumo em uma frase.
 *
 * @remarks Detalhes que o tipo não diz.
 * @typeParam T - O que o genérico representa.
 * @param nome - Só para o que o tipo não diz.
 * @returns O que o tipo de retorno não diz.
 * @example
 * funcao(entrada); // saida
 * @deprecated Use `outraFuncao`.
 */
````

## JavaScript (JSDoc)

````js
/**
 * Resumo em uma frase.
 * @param {string} titulo - O título do livro.
 * @returns {number} O que volta.
 */
````

Somente `/**` é reconhecido; `/*` e `/***` são ignorados.

## Rust (rustdoc)

````rust
/// Resumo em uma linha (o texto antes da primeira linha em branco vira resumo em buscas).
///
/// # Examples
///
/// ```
/// let r = minha_crate::funcao(2);
/// assert_eq!(r, 4);
/// ```
///
/// # Errors
///
/// [Quando retorna Err, se aplicável.]
pub fn funcao(x: u32) -> u32 { x * 2 }
````

Atributos de bloco: `no_run` (rede, efeitos), `ignore` (só com motivo), `should_panic`, `compile_fail`. `?` em exemplo exige `# Ok::<(), E>(())` no fim do bloco. Rodar: `cargo test --doc`.

## Java (Javadoc; confira a versão do JDK)

````java
/**
 * Resumo na primeira frase.
 *
 * @param itens lista de itens; não nula
 * @return o total em centavos
 * @throws IllegalArgumentException se a lista for vazia
 * @since 2.1
 */
public long total(java.util.List<Item> itens) { /* ... */ }
````

`{@return ...}` em linha existe desde o JDK 16.
