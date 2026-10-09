# Uso e integração

## Conhecimento portável

Forneça `brains/qa/SKILL.md` e as referências relevantes à IA. Para anexos,
os links locais não disponibilizam automaticamente os arquivos. Sem execução,
a base permite produzir planos, casos e revisão; informe essa limitação.
Helpers Python são opcionais; a auditoria axe exige Playwright.

## Exportar fontes para um projeto

```bash
python3 tools/export_project.py --host claude --target /caminho/do/projeto
# Ou, em outro projeto:
python3 tools/export_project.py --host codex --target /outro/projeto
```

O exportador exige projeto existente e destinos novos. Copia todos os brains próprios disponíveis e o gstack para
`.claude/skills/gstack`, origem de projeto reconhecida pelo setup. Os brains vão para
`.claude/skills/<nome>` no Claude, ou `.agents/skills/<nome>` no Codex;
QA e fullstack ficam adjacentes para suas referências cruzadas. Cada brain
recebe cópias de contexto, guia de integração e catálogo em `assets/contexto/`
quando disponíveis na origem; `availability.json` registra disponibilidade
e o CLI avisa quando faltam recursos. O SKILL.md exportado é a entrada;
o router da raiz original não é obrigatório nessa cópia.
O catálogo copiado conserva caminhos da origem e é inventário de intenção;
para abrir workflows exportados, use o gstack instalado e seus caminhos reais. Destinos existentes
são recusados antes da cópia; não há `--force`. Os diretórios de destino não
podem apontar para fora do projeto por symlinks.

## Preparar runtime após exportar

O exportador imprime a próxima etapa. No projeto exportado:

```bash
cd /caminho/do/projeto/.claude/skills/gstack
./setup --host claude --prefix
# Alternativa para o projeto exportado para Codex:
./setup --host codex --prefix
```

Execute somente o comando do host pretendido. `--prefix` separa `gstack-qa`
do nosso `qa`. O setup instala/builda e pode oferecer configuração adicional;
confira as mensagens e os documentos do fornecedor. Codex é classificado
como experimental nessa versão.

O requisito efetivo do `package.json` é Bun >= 1.4.0. O README original cita
um mínimo mais antigo; use o pacote ao preparar esta revisão. Navegador,
integração de agentes e iOS têm requisitos específicos nos documentos gstack.

O runtime não foi instalado/executado automaticamente durante a importação.
Os fontes e as instruções estão disponíveis; isso não equivale a testes
funcionais no seu projeto.

Exemplos: “Use QA para planejar limites”; “Use QA e gstack-qa-only para avaliar
homologação”; “Investigue com gstack-investigate”; “Revise arquitetura e testes
com gstack-plan-eng-review”. A invocação nativa depende do host.

## Atualização

Não execute `gstack-upgrade`, `git pull` ou setup diretamente em `vendor/gstack`:
isso modifica o snapshot ou usa Git/configuração do repositório pai. Atualize
com [upstream.md](upstream.md) e revise explicitamente instalações exportadas.

## Invocação no projeto exportado

Peça explicitamente `FULLSTACK-COMPLETO` para desenvolvimento ou
`QA-COMPLETO` para validação integral. Indique objetivo e escopo. Se o host
não descobrir a skill automaticamente, aponte para o SKILL.md da pasta
exportada; a keyword por si só não instala nem carrega arquivos sem acesso.
Em exportações antigas sem contexto compartilhado, registre cobertura parcial
ou exporte para novo destino; o exportador não sobrescreve instalações.
