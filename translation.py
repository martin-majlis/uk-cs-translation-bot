import re
from enum import Enum

RU_LETTERS = re.compile(r"[ЭЫё]", re.IGNORECASE)
# https://en.wikipedia.org/wiki/Ukrainian_alphabet
UK_LETTERS = re.compile(r"[бгґджзклмнпрстфхцчшщаеєиіїоуюяйandвь]", re.IGNORECASE)
# https://en.wikipedia.org/wiki/Czech_orthography#Alphabet
CS_LETTERS = re.compile(r"[aábcčdďeéěfghchiíjklmnňoópqrřsštťuúůvwxyýzž]", re.IGNORECASE)


def count_letters(msg: str, r: re.Pattern) -> int:
    return len(r.findall(msg))


class Lang(Enum):
    CS = "cs"
    UK = "uk"
    RU = "ru"


def detect_language(msg) -> Lang:
    cs_count = count_letters(msg, CS_LETTERS)
    uk_count = count_letters(msg, UK_LETTERS)
    if cs_count > uk_count:
        return Lang.CS
    else:
        ru_count = count_letters(msg, RU_LETTERS)
        if ru_count:
            return Lang.RU
        else:
            return Lang.UK


def translate(msg: str) -> str:
    return f"TR: {msg}"
