from functools import lru_cache as cache
from llama_index.llms.ollama import Ollama


@cache
def configured_llm(language):
    assert language is not None
    llm = Ollama(
        model="mixtral:instruct",
        request_timeout=500.0,
        temperature=0.1,
    )

    return llm.complete


def instruct_llm(language, instruction, text):
    return configured_llm(language=language)(f"[INST]{instruction}[/INST]\n{text}")


def instruct_llm_with_rating(language, instruction, text):
    try:
        response = str(instruct_llm(language, instruction, text))

        return {"rating": int(response.split("\n")[0]), "details": ("\n".join(response.split("\n")[1:])).strip()}
    except ValueError:
        return {"rating": 1, "details": "problems understanding the text"}
