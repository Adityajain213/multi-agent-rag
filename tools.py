from langchain.tools import tool
from dotenv import load_dotenv
load_dotenv()
 
import os
import requests
from bs4 import BeautifulSoup
from rich import print
from tavily import TavilyClient


tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Return titles, URLs, and snippets."""

    result = tavily_client.search(
        query=query,
        max_results=5
    )

    out = []

    for r in result["results"]:
        out.append(
            f"Title: {r['title']}\n"
            f"URL: {r['url']}\n"
            f"Snippet: {r['content'][:300]}\n"
        )

    return "\n----\n".join(out)


@tool
def scrape(url:str)->str:
    """scrape and return clean text content from a given url for deeper reading"""
    try:
        resp = requests.get(url,timeout=8,headers={"User-Agent":"Mozilla/5.0"})
        soup = BeautifulSoup(resp.text,"html.parser")
        for tag in soup(["script","style","nav","footer"]):
            tag.decompose()
        return soup.get_text(separator=" ",strip=True)[:3000]
    except Exception as e:
        print(e)
