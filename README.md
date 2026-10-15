# AI Google Search Agent

A command-line web research assistant that searches the web with Tavily and uses
Google Gemini to answer questions from the search results.

## Requirements

- Python 3.10 or later
- A Google AI API key
- A Tavily API key

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Create a `.env` file in the project directory with your API keys:

   ```dotenv
   GOOGLE_API_KEY=your_google_ai_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

   Keep this file private; it is excluded from Git.

## Run

Start the assistant from the project directory:

```powershell
python main.py
```

Enter a question when prompted. The app searches Tavily for each non-empty
question, then asks Gemini to produce an answer based on those results and
include relevant source URLs. Type `quit` to exit.

## Configuration

The search currently requests up to five general web results. The model is
`gemini-2.5-flash` with temperature set to `0`; these settings are defined in
`main.py`.
