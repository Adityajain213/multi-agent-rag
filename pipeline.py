from agents import deep , build_search_agent , writer_chain , critic_chain
from rich import print

def run_research(topic:str)->dict:
    state = {}

    print("\n"+" ="*50)
    print("step 1 - search agent is working ...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages":[("user",f"find recent and relaible and detailed information about {topic}")]
    })

    state["search_results"] = search_result['messages'][-1].content

    print("\n search result ",state['search_results'])


    #reader agent
    print("\n"+" ="*50)
    print("step 2 - reader agent is working ...")
    print("="*50)

    reader_agent = deep()

    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })

    state['scraped_content'] = reader_result['messages'][-1].content

    print("\nscraped content: \n", state['scraped_content'])

    #writer chain 

    print("\n"+" ="*50)
    print("step 3 - writer is working on report ...")
    print("="*50)

    research_combined = (
        f"search result: \n {state['search_results']}\n\n"
        f"detailed scaped content : \n {state['scraped_content']}\n\n"
    )

    state["report"] = writer_chain.invoke({
        "topic":topic,
        "research":research_combined
    })

    print("\n final report \n ",state['report'])

    #4 critic chain

    print("\n"+" ="*50)
    print("step 4 - critic is working on report ...")
    print("="*50)
    
    state["feedback"] = critic_chain.invoke({
        "report":state['report']
    })
    print("\n critic report \n", state['feedback'])

    return state
    
if __name__== "__main__":
    topic=input("enter a research topic")
    run_research(topic)
