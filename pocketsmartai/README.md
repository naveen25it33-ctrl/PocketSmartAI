# PocketSmart AI

PocketSmart AI is a budget-aware recommendation assistant for:
- 🏠 Home Interior Planning
- 🎉 Party Planning
- 💎 Jewelry Planning with optional outfit image input

## Project architecture

Browser UI → Flask backend → Gemini AI (optional) → structured recommendations → UI

If `GEMINI_API_KEY` is not configured, the application automatically uses a built-in fallback recommendation engine. This makes the project easy to demo locally.

## Team

- Leader: Mugilan
- Members: Madhusri
- Augustin P.
- Dhanisya V.
- Kavinragav

## 1. Install Python

Install Python 3.11+ and make sure `python --version` works.

## 2. Open the project in VS Code

Extract the ZIP and open the `PocketSmart_AI` folder.

## 3. Create virtual environment

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## 4. Install packages

```powershell
pip install -r requirements.txt
```

## 5. Configure Gemini (optional)

Copy `.env.example` to `.env`.

Add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

Do NOT upload `.env` to GitHub.

If you leave the key empty, fallback/demo mode still works.

## 6. Run

```powershell
python app.py
```

Open:

http://127.0.0.1:5000

## 7. Test

1. Click Home Interior and enter a budget.
2. Click Party Planner and enter guests/event details.
3. Click Jewelry Planner and optionally upload an outfit image.
4. Register or login to test the session flow.

## Render deployment

Create a new Web Service from this GitHub project.

Build command:

```text
pip install -r requirements.txt
```

Start command:

```text
gunicorn app:app
```

Add environment variables:
- `SECRET_KEY`
- `GEMINI_API_KEY`
- `GEMINI_MODEL`

## Important note

The project documentation describes Gemini 1.5 Flash Pro. Model names and API availability can change over time, so the implementation keeps the Gemini model configurable through `GEMINI_MODEL`. The default in this starter project is `gemini-2.5-flash`.

The platform links shown by the demo are illustrative; they are not live product-price feeds. For a production version, connect approved commerce/restaurant APIs or affiliate/catalog APIs instead of pretending to have live prices.
