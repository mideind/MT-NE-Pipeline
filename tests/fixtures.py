import re
from typing import Tuple

import pytest

from greynirseq.ner.ner_extracter import embed_tokens, parse_line


@pytest.fixture
def ner_sentence_pair():
    return (
        "Um <e:0:nvxo>Guðrúnu Helgadóttur</e:0> hefur <e:1:nkxn>Einar</e:1> ort .",
        "<e:1:nkxn>Einar</e:1> has written about <e:0:nvxo>Guðrún Helgadóttir</e:0> .",
    )


@pytest.fixture
def ner_final():
    return (
        (
            "<e:0:nkxe>Einar Jónsson</e:0> was visited by <e:1:nvxn>Guðrún</e:1> .",
            "<e:1:nvxn>Guðrún</e:1> fór í heimsókn til <e:0:nkxe>Einars Jónssonar</e:0> .",
        ),
        (
            "<e:0:nvxn>Anna</e:0> got a gift from <e:1:nkxþ>Pétur</e:1> , <e:2:nkxþ>Páll</e:2> and <e:3:nkxþ>Alexei</e:3> .",  # noqa
            "<e:0:nvxn>Anna</e:0> fékk gjöf frá <e:3:nkxþ>Alexei</e:3> , <e:1:nkxþ>Pétri</e:1> og <e:2:nkxþ>Páli</e:2> .",  # noqa
        ),
    )


@pytest.fixture
def ner_final_simple(ner_final: Tuple[Tuple[str, str], ...]):
    simplified = []
    pos_tag_pattern = ":n.*?>"
    replacement_pattern = ":x>"
    for en_sent, is_sent in ner_final:
        simplified.append(
            (
                re.sub(pos_tag_pattern, replacement_pattern, en_sent),
                re.sub(pos_tag_pattern, replacement_pattern, is_sent),
            )
        )

    return tuple(simplified)


@pytest.fixture
def ner_tagged_sentences_en():
    return (
        "Einar Jónsson was visited by Guðrún .	I-PER I-PER O O O I-PER O	hf",
        "Anna got a gift from Pétur , Páll and Alexei .	I-PER O O O O I-PER O I-PER O I-PER O	hf",
    )


@pytest.fixture
def ner_tagged_sentences_is():
    return (
        "Guðrún fór í heimsókn til Einars Jónssonar .	B-Person O O O O B-Person I-Person O",
        "Anna fékk gjöf frá Alexei , Pétri og Páli .	B-Person O O O B-Person O B-Person O B-Person O",
    )


@pytest.fixture
def embedded_ner_tagged_sentences_is(ner_tagged_sentences_is):
    result = []
    for sent in ner_tagged_sentences_is:
        sent, labels = sent.split("\t")
        result.append(embed_tokens(parse_line(sent.split(), labels.split(), "is"), sent.split()))
    return result


@pytest.fixture
def is_pos_tags():
    return (
        ["nven-s", "sfg3eþ", "ao", "nveo", "ae", "nkee-s", "nkee-s", "p"],
        ["nven-s", "sfg3eþ", "nveo", "aþ", "nkeþ-s", "p", "nkeþ-s", "c", "nkeþ-s", "p"],
    )


@pytest.fixture
def is_ner():
    return "tests/ner/data/is.ner"


@pytest.fixture
def en_ner():
    return "tests/ner/data/en.ner"
