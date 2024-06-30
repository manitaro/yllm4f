from metrics.llm import instruct_llm_with_rating


def youth_language(text, language):
    return instruct_llm_with_rating(
        language=language,
        instruction="""Rate the text as to whether it is written in youth language.
Rate the text from 1 to 10.
10 means the text is written entirely in youth language or has many emojis.
1 means that no youth language and no emojis are used.
Answer with the number only first. Next line should contain your explanation.
It is essential that you answer with the number of the rating in the first line.
This is important.

Example answer:
3
the text is not written in youth language and just uses one emoji.""",
        text=text,
    )
