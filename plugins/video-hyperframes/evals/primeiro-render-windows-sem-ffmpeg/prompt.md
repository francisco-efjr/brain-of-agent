---
name: primeiro-render-windows-sem-ffmpeg
description: "Windows sem FFmpeg: o usuário pede para renderizar o MP4 final agora. Mede se o plugin não renderiza antes de resolver FFmpeg e ffprobe, propõe build portátil com confirmação, variáveis só na sessão (sem winget, setx nem PATH) e aponta o Chrome do sistema para evitar o download do Chrome gerenciado."
tags: [video-hyperframes, playbook, windows, ffmpeg, render]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Não renderiza antes de resolver FFmpeg e ffprobe; propõe FFmpeg portátil em pasta do usuário com origem, tamanho e conferência de SHA-256, pedindo o sim; usa HYPERFRAMES_FFMPEG_PATH e HYPERFRAMES_FFPROBE_PATH só na sessão, sem winget, setx nem PATH; aponta HYPERFRAMES_BROWSER_PATH para o Chrome do sistema depois de Test-Path; não afirma ter renderizado."
model: sonnet
---
Estou no Windows 11, com Node 24 e o Chrome instalados, mas sem FFmpeg. Meu projeto HyperFrames está em C:\Users\<usuario>\videos\demo\projeto e eu já aprovei no preview. Renderiza o MP4 final agora.
