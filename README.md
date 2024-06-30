# yllm4f - Youth-Large-Language-Models-4-Freedom

## Motivation

Crafting a message without considering your target audience will fail to connect effectively. It is essential to tailor your writing to the specific needs and preferences of your audience.

Large Language Models (LLMs) are prevalent and trained predominantly on internet text created by adults, which does not align with the communication style of younger audiences. Consequently, LLMs often fail to engage youth effectively.

To address this, I aim to develop LLMs that communicate like a peer to young audiences:

* Using shorter sentences
* Employing simpler vocabulary
* Adopting youth language

The more these models can mimic youth communication styles, the more they will be utilized.

This hypothesis has been validated through a German/Latin-learning bot named Jules-Celestia. This bot, which impersonates Julius Caesar, communicates like a 13-year-old German student learning Latin—informal yet friendly, akin to a schoolmate. Jules-Celestia's success demonstrates the viability of this approach, leading to the broader project yllm4f, which aims to generalize this concept to other languages such as English and French.

## Idea

Large Language Models (LLMs) generate text but rarely verify its accuracy or suitability for specific audiences. In the professional realm, tools like [Ragas](https://github.com/explodinggradients/ragas) exist to evaluate the correctness and potential falsification of LLM responses. However, Ragas and similar tools do not assess whether an answer resonates with its intended audience, particularly the younger generation.

To address this gap, it would be beneficial to develop Ragas-like tools that evaluate whether LLM-generated answers are appropriate for a youthful audience.

To achieve this, I propose combining three powerful language tools:
* [spaCy](https://github.com/explosion/spaCy): An industrial-strength Natural Language Processing (NLP) library in Python.
* LLMs / mixtral: A free-to-use, local LLM trained on languages spoken in the EU.
* Wikipedia word frequency: A tool to assess which words might be unfamiliar to the target audience.

By integrating these tools, we can establish metrics to determine if an LLM-generated answer is compatible with the youth. If the answer does not meet these criteria, the system can then reformulate it to ensure better alignment with the younger generation's preferences and understanding.

## Flesch-Reading-Ease

One straightforward method to assess readability is the Flesch Reading Ease score, a formula developed by linguist Dr. Rudolf Flesch. This formula evaluates a text by counting its sentences, words, and syllables, then calculating a score based on these factors. Younger audiences tend to prefer words with fewer syllables, whereas more academic texts typically use words with more syllables. The following table illustrates how the Flesch Reading Ease score corresponds to various school grade levels.

| Score	| School level | Notes |
| ----- | ------------ | ----- |
| 100.00-90.00 | 5th grade | Very easy to read. Easily understood by an average 11-year-old student. |
| 90.0–80.0 | 6th grade | Easy to read. Conversational English for consumers. |
| 80.0–70.0 | 7th grade | Fairly easy to read. |
| 70.0–60.0 | 8th & 9th grade | Plain English. Easily understood by 13- to 15-year-old students. |
| 60.0–50.0 | 10th to 12th grade | Fairly hard to read. |
| 50.0–30.0 | College | Hard to read. |
| 30.0–0.0 | College graduate | Very hard to read. Best understood by university graduates. |

There are multiple Reading scores, but languages in Europe are quite different. So German for example loves longer words, so would need a different formula. Flesch-Reading-Ease has for this especially a formula for German. Other Reading scores focus just on German (e.g: Wiener Sachtextformel) or just on English (e.g: Dale–Chall formula)

## Languages

The following languages are supported for now. Others will also work, but the following languages can use all metrics.

* German
* English
* French

If your language is not included, please add an Issue. If you could do a Pull-Request, it would be very appreciated.

## Metrics

Once the target audience is identified, it is essential to evaluate whether the texts are appropriate for that audience. The following metrics have been developed for this purpose.
All metrics work for all languages. If the language of the text is not provided, the language will be determined.

### Natural-Language-Processing-based Metrics

These metrics are determined by spaCy - a Natural-Language-Processing Toolkit.

The key metrics include:

* Flesch-Reading-Ease: to determine which school grade the text is for
* word / sentence / syllabel statictics: to focus on short sentences or simple words
* complicated words: to inform which words are maybe too complicated for the audience

### LLM-based Metrics

Large Language Models (LLMs) are proficient in understanding text. The [Ragas](https://github.com/explodinggradients/ragas) project has demonstrated that LLMs can also be utilized to self-evaluate and regulate their own responses. The evaluation metrics employed by Ragas are based on LLM capabilities and assess various aspects of text quality, including readability and conciseness. Additionally, these metrics offer suggestions for improvement.

The key metrics include:

* Conciseness: Evaluates how succinctly the text is written and provides tips for making it more concise.
* Understandability: Assesses how easily the text can be comprehended.
* Youth Language: Identifies the use of language commonly associated with younger demographics.

### Wikipedia-word-frequency-based Metrics

Wikipedia is a vast repository of knowledge, with numerous articles authored in all languages spoken within the European Union. A commonly held assumption is that the frequency of a word's usage correlates with its familiarity; in other words, words that appear more frequently are generally more well-known. Conversely, words that are used only once or twice across the entire Wikipedia database are considered rare and are likely more difficult for readers to understand.

An important metric in this context is:

* Unusual Words: Identifies words in the text that are rarely used in Wikipedia, indicating that they may be difficult for the audience to comprehend.

## Show Case

### Jules Celestia - A young, youth-friendly Julius Caesar

[Jules Celestia](https://github.com/manitaro/jules.celestia) is an LLM-based chatbot designed to assist German Latin students by enabling them to interact with a virtual young Julius Caesar, engaging with him as a peer. This innovative tool promotes the learning of Latin and a deeper understanding of Roman culture. Jules Celestia served as the proof-of-concept for a broader initiative, which is now realized in yllm4f.

yllm4f generalizes the principles validated by Jules Celestia, allowing users to create youth-friendly chatbots that act as friends rather than distant, impersonal entities. This platform ensures that these chatbots communicate in a relatable and familiar manner, enhancing the user experience and fostering more effective learning and interaction.

## Usage

To simplify the setup process, a Docker image is provided for yllm4f. This image includes spaCy, Wikipedia, and LLMs, which are necessary for the tool’s functionality. Bundling these dependencies within a Dockerfile eases the installation requirements.

To build the Docker image, use the following command:
```
docker build --tag yllm4f .
```

This command will create the Docker image. Once built, the image can be used to analyze texts for readability, ensuring they are suitable for a younger audience. For example, you can integrate it into your LLM pipelines to tailor responses appropriately:
```
echo "provide your text you want to analyze for readability here" | docker run -i yllm4f --output text
```

If you are running Ollama, preferably with *mixtral:instruct*, you can further analyze the text using your LLM. Start Ollama with ollama serve, then add --net=host and --enable-llm to the command line:
```
docker run -i --net=host yllm4f --output text --enable-llm
```

### Usage in an LLM pipeline

If you intend to integrate yllm4f into an LLM or RAG pipeline, you can utilize the output json option to obtain all metrics in a machine-readable JSON format:

```
docker run -i --net=host yllm4f --output json --enable-llm
```

This command ensures that the output is structured in JSON, facilitating seamless integration and further analysis within your pipeline environment.

### Usage help

For comprehensive usage instructions, invoke the command with `--help`.
```
docker run -i --net=host yllm4f --help
```

```
usage: Text Analyzer [-h] [--language LANGUAGE] [--output {json,text}]
                     [--enable-llm]

Check how readable your text is - especially for young people

options:
  -h, --help            show this help message and exit
  --language LANGUAGE   the language the text is written in. If not provided
                        language is determined.
  --output {json,text}  FOO!
  --enable-llm          use an LLM to analyze the text
  ```

## Examples

### Readability

In this example, we evaluate a sentence expressed in two different levels of complexity, but conveying the same meaning. This demonstrates yllm4f's ability to accurately assess language and readability. The tool correctly identifies that the simpler version is comprehensible to a 5th grader, whereas the more complex version requires college-level comprehension.

*Caesar küsst Cleo zu Hause.*

```
language                      : de
flesch-reading-ease
  score                       : 93.10
  grade                       : 5th grade
```

*Caesar osculierte die Pharaonin Cleopatra zwischen den Pyramiden affektiv.*

```
language                      : de
flesch-reading-ease
  score                       : 15.00
  grade                       : college
```

### Ratings

Here is a text written in youth language and yllm4f detects this and rates this accordingly.

*Hey Bro. Wie ist die Lage bei dir? Alles gechilled? Kommst du später vorbei?*

```
  rating                      : 8
  details                     : The text contains several words that are commonly used in youth language, such as "hey," "bro," and "gechilled." It also includes an informal invitation to come over later. However, there are no emojis or other visual elements typically associated with digital youth communication.
understandability
  rating                      : 1
  details                     : This text uses a lot of slang and abbreviations that are not commonly used in English, making it very difficult for 13-year-olds to understand. The use of informal language and the lack of proper punctuation also make it challenging for young people to comprehend the message being conveyed.
conciseness
  rating                      : 2
  details                     : The text is written in informal language with slang, which may not be appealing or understandable to everyone. The message does not seem concise, interesting, or relevant as it only asks if the person will come later without providing any context or purpose for the meeting.
```

### Further Examples:

To provide a deeper understanding, the following texts were used for demonstration purposes:

* A simple text ("The Very Hungry Caterpillar")
* A medium text ("Moby Dick")
* A difficult text (EU AI Act)

All texts are analyzed by the yllm4f. The results could be found here.
* [German](https://github.com/manitaro/yllm4f/blob/main/showcases/German.md)
* [English](https://github.com/manitaro/yllm4f/blob/main/showcases/English.md)
* [French](https://github.com/manitaro/yllm4f/blob/main/showcases/French.md)

## Further work

* More support and testing for languages apart from English / German / French.
* Find more readability indices that work on multiple languages
* Simpler Python

## References / Literature

* https://en.wikipedia.org/wiki/Readability
  to get an overview over what readability is and what different formulas could be applied. Note that not many readability formulas work with multiple languages.
* R. Flesch: Art of Readable Writing. Hungry Minds Inc,U.S.; Reissue Edition (1. April 1962)
  Dr. Flesch is an expert in readability.
* W. H. DuBay: The Principles of Readability. Impact Information, Costa Mesa, California 2004
* https://github.com/explosion/spaCy
  the standard tool for language analysis
* https://ollama.com/library/mixtral:instruct
  this LLM model is used. It could be simply deployed within ollama, so it could run locally
* https://github.com/explodinggradients/ragas
  Ragas is a Framework for LLMs to evaluate relevancy, faithfulness, correctness, ... for LLM answers
