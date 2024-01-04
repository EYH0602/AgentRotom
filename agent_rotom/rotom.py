from langchain.chains import LLMChain, LLMRequestsChain
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain_community.llms import OpenAI  # pylint: disable=no-name-in-module
import os
from pokedex import get_pokemon_data
import fire


def web_search_result(pokemon_name: str) -> str:
    template = """Between >>> and <<< are the raw search result text from google.
    Extract the answer to the question '{query}' or say "not found" if the information is not contained.
    Use the format
    Extracted:<answer or "not found">
    >>> {requests_result} <<<
    Extracted:"""

    prompt = PromptTemplate(
        input_variables=["query", "requests_result"],
        template=template,
    )
    llm = OpenAI(temperature=0)
    chain = LLMRequestsChain(llm_chain=LLMChain(llm=llm, prompt=prompt))
    question = f"details and descriptions about {pokemon_name} in Pokemon"
    inputs = {
        "query": question,
        "url": "https://www.google.com/search?q=" + question.replace(" ", "+"),
    }
    return str(chain(inputs)["output"])


def answer(pokemon_name: str):
    """ask Rotom about a pokemon, and see how Rotom response"""
    stat = get_pokemon_data(pokemon_name)
    search_result = web_search_result(pokemon_name)

    prompt = ChatPromptTemplate.from_template(
        """Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}"""
    )
    llm = OpenAI(temperature=0)

    document_chain = create_stuff_documents_chain(llm, prompt)
    response = document_chain.invoke(
        {
            "input": f"Please describe Pokemon {pokemon_name}'s history, characteristics, and best four moves",
            "context": [Document(page_content=search_result + str(stat))],
        }
    )
    return response


def main(pokemon_name: str):
    print(answer(pokemon_name))


if __name__ == "__main__":
    fire.Fire(main)
