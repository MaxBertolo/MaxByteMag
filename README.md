# Tech News Daily (Automatic HTML + PDF Report)

Questo progetto genera automaticamente ogni giorno un report di notizie tecnologiche globali
su Telco, Media, AI, GenAI, Data Center, Satellite, Fiber, ecc.

Il sistema:
- legge feed RSS
- filtra le notizie delle ultime 24 ore
- usa OpenAI per creare un riassunto in 5 punti
- genera un file HTML
- genera un file PDF
- GitHub Actions esegue tutto ogni giorno alle 06:00 UTC

## Output
I report giornalieri si trovano in:
- `reports/html/`
- `reports/pdf/`

## Esecuzione manuale

