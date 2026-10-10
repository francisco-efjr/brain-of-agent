# Exemplo: primeiro SLO de `POST /pedidos` a partir de logs do nginx

Cenário ilustrativo (não é medição real): e-commerce pequeno, jornada "criar pedido", sem SLO, um mês de logs de acesso com `request_time`. Produto pediu "100% de disponibilidade" e "tempo médio abaixo de 200 ms". Rótulos: Verificado = visto nesta sessão; Inferido = conhecimento estável, conferir; Suposição = escolha a validar.

## 1. Por que recusar os dois pedidos iniciais

| Pedido | Problema | Contraproposta |
| --- | --- | --- |
| 100% de disponibilidade | Custo cresce sem limite e nenhuma mudança cabe no orçamento zero | Meta abaixo de 100% ancorada na linha de base |
| Tempo médio < 200 ms | A média esconde a cauda: 99 requisições de 100 ms e uma de 10 s dão 199 ms | Percentis: proporção abaixo de dois limiares |

## 2. SLIs (especificação x implementação)

| SLI | Especificação (usuário) | Implementação | Cobertura e limite |
| --- | --- | --- | --- |
| Disponibilidade | Proporção de pedidos criados sem erro de servidor | Linhas do nginx com `POST /pedidos` e status < 500 / total | Não vê falha antes do nginx (DNS, CDN) nem 200 com corpo de erro |
| Latência | Proporção de pedidos criados em até 800 ms (e em até 2 s) | `request_time` das mesmas linhas | `request_time` inclui envio lento do cliente; mede a borda, não o navegador |

Se o pedido for aceito com 202 e processado depois, acrescente um terceiro SLI: tempo até conclusão do pedido (idade da fila). Sem ele, a latência HTTP boa esconde o pedido parado.

## 3. Linha de base com o log (Inferido; ajuste ao seu formato)

Suposição de formato: `combined` do nginx com `$request_time` anexado ao fim da linha. Nesse formato `$6` é `"POST`, `$7` é o caminho e `$9` é o status. Confira com `head -n 3 access.log` antes de rodar.

```bash
# eventos bons = status < 500 e request_time < 0,8 s; um arquivo por semana (janela fixa)
awk '$6=="\"POST" && $7 ~ /^\/pedidos/ { n++; if ($9+0 < 500 && $NF+0 < 0.8) bom++ }
     END { printf "eventos=%d bons=%d razao=%.5f\n", n, bom, bom/n }' access.log-semana1
```

Saída fictícia para ilustrar a leitura: `eventos=182340 bons=181912 razao=0.99765`. Repita por semana. Se as quatro semanas derem 0,9976; 0,9981; 0,9969; 0,9990, a linha de base é o pior caso arredondado para baixo: **99,6%** (Suposição de arredondamento; o time decide). Uma meta de 99,9% exigiria melhorar antes de prometer.

Cauda de latência (p95 das requisições de sucesso):

```bash
awk '$6=="\"POST" && $7 ~ /^\/pedidos/ && $9+0 < 500 { print $NF }' access.log-semana1 \
  | sort -n | awk '{ a[NR]=$1 } END { print "p95=" a[int(NR*0.95)] " s" }'
```

## 4. Orçamento (refazer e colar a saída)

```bash
python -c "print(30*24*60*(1-0.996))"   # meta 99,6% em 30 dias
```

Resultado esperado: `172.8` minutos equivalentes (arredondamento de ponto flutuante pode mostrar `172.80000000000007`). Em eventos, com 180 mil pedidos por semana, 0,4% = cerca de 720 pedidos ruins por semana.

## 5. Trecho da política (a preencher pelo time)

| Campo | Conteúdo |
| --- | --- |
| Serviço/SLO | `POST /pedidos`, 99,6% em 30 dias (Suposição, até haver 3 meses de medição) |
| Consumo acompanhado por | dono do serviço, toda segunda-feira |
| Ação em 50% do orçamento | revisar causas dos erros na reunião semanal (exemplo) |
| Ação ao esgotar | priorizar confiabilidade sobre funcionalidades até recuperar (exemplo; a organização decide) |
| Escalonamento | divergência entre produto e engenharia vai ao diretor técnico (papel) |
| Aprovadores | produto, desenvolvimento, operação (papéis; nomes no documento real) |
| Revisão | trimestral, ou após incidente que consumir mais de 20% do orçamento (exemplo) |

## 6. Dados que faltam (lista a entregar)

- Medição de pelo menos um ciclo completo com a janela escolhida.
- Cobertura das falhas antes do nginx (teste de caixa-preta externo).
- Fonte do tempo até conclusão, se houver processamento assíncrono.
