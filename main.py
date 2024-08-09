from langchain.chains.llm import LLMChain
from langchain.prompts.prompt import PromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from third_parties.linkedin import scrape_linkedin

if __name__ == "__main__":
    load_dotenv()

    summary_template = """
    Given the information about the person I want to create 
    1. A short summary
    2. Two interesting facts about him
    """

    summary_prompt_template = PromptTemplate(input_variable=["information"], template=summary_template)

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = summary_prompt_template | llm

    # Call function to take information from linkedin
    linkedin_data = scrape_linkedin("https://www.linkedin.com/in/luis-von-ahn-duolingo/")

    res = chain.invoke(input={"information": linkedin_data})

    print(res)
