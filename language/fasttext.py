#!/usr/bin/env python3
from subprocess import check_output
import tempfile


def detect_language(sentence):
    """
    >>> def test(sentence):
    ...     result = detect_language(sentence)
    ...     print(f'German: {result.get("de", 0) * 100:.0f} %, Latin: {result.get("la", 0) * 100:.0f} %')
    >>> test('Ich bin ein Auto.')
    German: 100 %, Latin: 0 %
    >>> test('Caesar sagte oft, veni, vidi, vici. Das bedeutet, ich kam, ich sah, ich siegt.')
    German: 99 %, Latin: 0 %
    >>> test('Alea iacta est bedeutet die Würfel sind gefallen. Ich habe das oft gesagt, wenn die Entscheidungen getroffen waren.')
    German: 100 %, Latin: 0 %
    >>> test('Alea iacta est.')
    German: 0 %, Latin: 100 %
    >>> test('''
    ...     In der lichtdurchfluteten Welt des Tages, quando sol oriri incipit, erwacht die Natur zu neuem Leben.
    ...     Vögel, avi, singen ihre Melodien, während die Blumen, flores, ihre zarten Blütenblätter entfalten.
    ...     Ein sanfter Wind, aura mitis, streicht über die grünen Wiesen, prata viridia. Es ist eine Zeit des Aufbruchs,
    ...     tempus est exordii, und der Hoffnung, et spei, in der jeder Tag die Möglichkeit für neue Abenteuer birgt.
    ...     Lass uns die Schönheit des Augenblicks, pulchritudinem temporis, genießen und die Welt mit offenen Herzen, pectore aperto, erkunden.''')
    German: 94 %, Latin: 0 %
    """

    def split_as_long_as_possible(input_list):
        try:
            for i in range(0, len(input_list), 2):
                end = i + 2
                a, b = input_list[i:end]
                yield (
                    a,
                    b,
                )
        except ValueError:
            return

    with tempfile.NamedTemporaryFile(mode="w") as file:
        file.write(sentence)
        file.flush()
        return {
            label.split("__")[2]: float(probability)
            for label, probability in split_as_long_as_possible(check_output(["fasttext", "predict-prob", "/lid.176.bin", file.name, "10"]).decode("utf-8").replace("\n", " ").split(" "))
        }
