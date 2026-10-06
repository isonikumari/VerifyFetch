# VerifyFetch

VerifyFetch is an AI-assisted fact-checking app. Enter a claim in the Streamlit
interface to break it into sub-claims, search the web for evidence, and generate
a report with a verdict, reasoning, and source URLs. An optional quality review
asks a critic model to assess the report and revise it when needed.

AI-generated reports can be incomplete or incorrect. Review the cited sources
yourself before relying on or sharing a result.

## Features

- Splits a claim into smaller questions for analysis.
- Searches the web for evidence using Tavily.
- Generates a True, False, Misleading, or Unverifiable report using Gemini.
- Offers an optional critic-and-revision quality review in the web interface.
- Includes a command-line mode for a quick fact check.

## Requirements

- Python 3.11 or later.
- A Google Gemini API key.
- A Tavily API key.

## Setup

1. Clone the repository and open its directory:

   ```powershell
   git clone https://github.com/isonikumari/VerifyFetch.git
   cd VerifyFetch
   ```

2. Create and activate a virtual environment:

   ```powershell
   py -3.11 -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   On macOS or Linux, use:

   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Create a `.env` file in the project directory with your API keys:

   ```dotenv
   GOOGLE_API_KEY=your_google_gemini_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

   Keep this file private. Do not commit API keys or other secrets.

## Run the web app

```bash
streamlit run app.py
```

Streamlit will print a local URL to open in your browser. Enter a claim and
select **Run quality review** if you want the additional review and revision
step.

## Run from the command line

```bash
python main.py
```

Enter a claim when prompted. This mode runs the fact check without the optional
quality review.

## Run with Docker

After creating the `.env` file as described above, build and run the app:

```bash
docker build -t verifyfetch .
docker run --rm -p 8501:8501 --env-file .env verifyfetch
```

Open `http://localhost:8501` in your browser.

## Project structure

- `app.py` — Streamlit user interface.
- `main.py` — Fact-check workflow and command-line entry point.
- `agents.py` — Gemini-powered planning, report, review, and revision chains.
- `tools.py` — Tavily web search tool.
- `assets/` — Background artwork used by the interface.