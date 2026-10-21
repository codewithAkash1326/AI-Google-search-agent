# AI Google Search Agent

A command-line assistant that uses Google Gemini to answer questions and
Tavily to search the web when current information is needed.

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

Enter a question when prompted. Gemini can use Tavily when it determines that
current, frequently changing, or post-cutoff information is needed. It is
instructed to search for real-world event results and outcomes, including
questions about a named year or season, and to cite relevant source URLs.
Because search is selected by the model, it may not search for every
time-sensitive question. Type `quit` to exit.

Conversation history is kept in memory for the `cli-session` thread, so
follow-up questions can use earlier turns. This memory is cleared when the
program exits.

## Configuration

The search tool requests up to five general web results. The model is
`gemini-2.5-flash` with temperature set to `0`. The thread ID and in-memory
checkpointer are configured in `main.py`.
