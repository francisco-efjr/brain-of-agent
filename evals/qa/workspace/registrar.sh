#!/bin/sh
# uso: registrar.sh <dir-iteracao> <eval-dir-prefixo> <config> <tokens> <duration_ms>
d=$(ls -d "$1"/eval-"$2"-* | head -1)/"$3"
python3 -c "import json,sys; t=int(sys.argv[2]); ms=int(sys.argv[3]); json.dump({'total_tokens':t,'duration_ms':ms,'total_duration_seconds':round(ms/1000,1)}, open(sys.argv[1]+'/timing.json','w'))" "$d" "$4" "$5"
echo "ok $d"
