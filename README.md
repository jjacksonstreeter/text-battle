
# Text Battle (Streamlit) — with Top 10 Scoreboard

Play a turn-based text battle in your browser. Save your score and view the **Top 10 scoreboard**.

## Live Links
- Repo: https://github.com/jjacksonstreeter/text-battle
- Portfolio (GitHub Pages): https://jjacksonstreeter.github.io/text-battle/
- Streamlit App: *(add your Streamlit Cloud URL after you deploy)*

## Run locally
```bash
python -m venv .venv
# Windows
.venv\Scriptsctivate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Scoreboard persistence
- Local runs: scores are saved to `scoreboard.json` and a CSV copy in `docs/demo/scoreboard.csv`.
- Streamlit Cloud: files are ephemeral (not committed back to GitHub).
- You can always download the scoreboard via the Download button.

## Deploy (Streamlit Community Cloud)
1. Push this repo to GitHub (https://github.com/jjacksonstreeter/text-battle).
2. Streamlit Cloud → New app → pick this repo → main file: `app.py` → Deploy.
3. Copy the live URL and paste it above and in `docs/index.md`.

## Portfolio (GitHub Pages)
1. Ensure `docs/index.md` exists (included).
2. Repo Settings → Pages → Source: `main` / Folder: `/docs`.
3. Your page will be live at https://jjacksonstreeter.github.io/text-battle/.
