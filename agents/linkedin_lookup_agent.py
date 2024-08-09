import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# Library to use tools, tools are function to communicate LLM with the exterior
from langchain_core.tools import Tool

from langchain.agents import (
    create_react_agent,
    AgentExecutor
)

# Library to import to import tools made by users
from langchain import hub
load_dotenv()

def lookup(name: str) -> str:
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",

    )
    template = """
    Given the full name {name_of_person} I want you to get me a link to their LinkedIn profile page.
    Your answer should contain only a URL.
    """

    prompt_tempalte = PromptTemplate(
        template=template, input_variable=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func="?",
            description="Useful when you need to get a LinkedIn page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools_for_agent,
        verbose=True
    )

    result = agent_executor.invoke(
        input={"input": prompt_tempalte.format_prompt(name_of_person=name)}
    )

    linkedin_profile_url = result["output"]
    return linkedin_profile_url


if __name__ == '__main__':
    linkedin_profile_url = lookup(name="Gerson Alexander Ramirez Conoz")
    print(linkedin_profile_url)
