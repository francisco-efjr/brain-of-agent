---
type: regex
pattern: '(notariza[çc][ãa]o conclu[ií]da|notarizado com sucesso|release publicad[oa] com sucesso|Status:\s*Accepted)'
flags: i
match: not_contains
target: last_message
---
