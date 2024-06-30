from metrics.llm import instruct_llm_with_rating


def understandability(text, language):
    return instruct_llm_with_rating(
        language=language,
        instruction="""Rate the text as to whether it can be understood by 13-year-olds.
Rate the text from 1 to 10.
10 means that the text is written simply and can be understood by young people.
1 means that the text is too complicated and 13-year-olds cannot understand it.
Answer with the number only first. Next line should contain your explanation.
It is essential that you answer with the number of the rating in the first line.
This is important.

Example answer:
3
the text is not good understandable. You use double negation, which makes it for the reader difficult.""",
        text=text,
    )
