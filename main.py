from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


SYSTEM_PROMPT = """
You are a helpful assistant. Think through whether the question needs current
information before answering. Use the tavily_search tool whenever the user asks
about real-world events, current or recent facts, frequently changing
information, or information that may be newer than your training data. Always
search for event results and outcomes for a named year or season (for example,
the winner of IPL 2026). Do not guess that an event has not happened based on
your training data; search for evidence first.

For questions that do not need current information, answer directly without
searching. When you search, base current claims on the results and cite relevant
source URLs. If results are insufficient or contradictory, say so. Never invent
facts, dates, or sources.
"""

search = TavilySearch(
    name="tavily_search",
    description=(
        "Search the web for current, recent, or frequently changing information, "
        "including real-world event results and outcomes for a specific year."
    ),
    max_results=5,
    topic="general",
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
)

agent = create_agent(
    model=llm,
    tools=[search],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": "cli-session"}}


def plain_text(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            block["text"]
            for block in content
            if isinstance(block, dict) and isinstance(block.get("text"), str)
        )
    return str(content)


while True:
    query = input("\nUser: ").strip()

    if query.lower() == "quit":
        break

    if not query:
        continue

    try:
        response = agent.invoke(
            {"messages": [{"role": "user", "content": query}]},
            config=config,
        )

        print("\nFinal Answer:")
        print(plain_text(response["messages"][-1].content))

    except Exception as e:
        print(f"Error processing query: {e}")
