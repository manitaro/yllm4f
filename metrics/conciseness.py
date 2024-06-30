from metrics.llm import instruct_llm_with_rating


def conciseness(text, language):
    return instruct_llm_with_rating(
        language=language,
        instruction="""Rate the text as to whether it is written concisely, interestingly and succinctly.
Rate the text from 1 to 10.
10 means the text is concise, interesting and to the point.
1 means that the text is too long and uninteresting.
Answer with the number only first. Next line should contain your explanation.
It is essential that you answer with the number of the rating in the first line.
This is important.

Example answer:
3
the text is not concise and uses many fill words.""",
        text=text,
    )
