
from dotenv import load_dotenv
load_dotenv()

import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field


class CustomResponse(BaseModel):
    output: str = Field(
        description="Answer based on the web search results, including relevant sources."
    )



search = TavilySearch(
    max_results=5,
    topic="general"
)


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

structured_llm = llm.with_structured_output(CustomResponse)


SYSTEM_PROMPT = """
You are a web research assistant.

Rules:
1. Answer using the provided web search results.
2. Prioritize recent and credible sources.
3. Never invent facts or dates.
4. If results are contradictory or insufficient, explain uncertainty.
5. Include relevant source URLs in your answer.
6. Do not claim something has not happened without evidence.
"""


while True:
    query = input("\nUser: ").strip()

    if query.lower() == "quit":
        break

    if not query:
        continue

    try:
        
        print("\nSearching Tavily...")

        search_results = search.invoke({"query": query})

         
        messages = [
            ("system", SYSTEM_PROMPT),
            (
                "human",
                f"""
                User question: {query}

                Web search results:
                {json.dumps(search_results, ensure_ascii=False, default=str)}

                Answer the user's question using these results.
                """
            )
        ]

        
        response = structured_llm.invoke(messages)

        print("\nFinal Answer:")
        print(response.output)

    except Exception as e:
        print(f"Error processing query: {e}")
