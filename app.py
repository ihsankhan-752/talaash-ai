from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain_core.prompts import PromptTemplate
from langchain_classic.agents import create_react_agent, AgentExecutor 
load_dotenv()


GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

template = """You are Talaash AI, a smart autonomous deal-finder assistant.
Your job is to search live stores, compare current prices, verify discounts, and present the best deals with store names, exact prices, and direct links.

You have access to the following tools:
{tools}

Use the following format strictly:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: a clear, structured list of the top deals found (product name, store, price, and link)

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)




llm = ChatGoogleGenerativeAI(api_key = GOOGLE_API_KEY, model = "gemini-3.5-flash-lite", temperature = 0)

search_tool = TavilySearch(max_results= 3)

tools = [search_tool]


agent = create_react_agent(llm=llm, tools=tools,prompt=prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)


response = agent_executor.invoke({
    "input": "Find the best current deals on wireless mechanical keyboards under 5000 PKR."
})
print(response["output"])