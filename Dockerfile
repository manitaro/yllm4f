FROM python:3.12 as builder

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Download word embedding if LLM is used
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash \
 && apt-get install -y git-lfs poppler-utils cmake libpoppler-cpp0v5 libpoppler-cpp-dev poppler-utils poppler-data libpopplerkit-dev \
 && git lfs install \
 && git clone https://huggingface.co/BAAI/bge-large-en-v1.5 /embedding_model \
 && rm -rf /embedding_model/.git

# Download and compile fasttext to determine language, if language is not provided
RUN curl -sL https://github.com/facebookresearch/fastText/archive/refs/tags/v0.9.2.tar.gz | tar -xz \
 && cd fastText-0.9.2 \
 && cmake . \
 && make install \
 && curl -O https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin \
 && mv lid.176.bin / \
 && echo "Das ist ein einfacher Test in Deutsch." > /tmp/test.txt \
 && fasttext predict-prob /lid.176.bin /tmp/test.txt 10 \
 && rm /tmp/test.txt \
 && rm -rf /fastText-0.9.2

# Download Wikipedia Word frequency
WORKDIR /wordcorpus/de
RUN curl -sL https://downloads.wortschatz-leipzig.de/corpora/deu_wikipedia_2021_1M.tar.gz | tar -xz \
 && mv /wordcorpus/de/deu_wikipedia_2021_1M/deu_wikipedia_2021_1M-words.txt /wordcorpus/de/words.txt \
 && rm -rf /wordcorpus/de/deu_wikipedia_2021_1M/

WORKDIR /wordcorpus/fr
RUN curl -sL https://downloads.wortschatz-leipzig.de/corpora/fra_wikipedia_2021_1M.tar.gz | tar -xz \
 && mv /wordcorpus/fr/fra_wikipedia_2021_1M/fra_wikipedia_2021_1M-words.txt /wordcorpus/fr/words.txt \
 && rm -rf /wordcorpus/fr/fra_wikipedia_2021_1M/

WORKDIR /wordcorpus/en
RUN curl -sL https://downloads.wortschatz-leipzig.de/corpora/eng_wikipedia_2016_1M.tar.gz | tar -xz \
 && mv /wordcorpus/en/eng_wikipedia_2016_1M/eng_wikipedia_2016_1M-words.txt /wordcorpus/en/words.txt \
 && rm -rf /wordcorpus/en/eng_wikipedia_2016_1M/

WORKDIR /work

# Install python requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Download spacy language models
RUN spacy download de_core_news_lg
RUN spacy download en_core_web_lg
RUN spacy download fr_core_news_lg
RUN spacy download fr

# Add sources
COPY . /work/

ENV PYTHONPATH /work/

# test code and integration
RUN python3 -m doctest *.py
RUN find . -name '*.py' | xargs -I {} python3 -m doctest "{}"

# Allow easy usage
ENTRYPOINT ["python3", "analyze_text.py"]
