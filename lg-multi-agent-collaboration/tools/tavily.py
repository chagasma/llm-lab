from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults

load_dotenv()

tavily_tool = TavilySearchResults(max_results=5)