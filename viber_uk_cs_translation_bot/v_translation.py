# COPY - DO NOT MODIFY
import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

import requests

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


@dataclass
class Translation:
    error: Optional[str] = None
    translation: Optional[List[str]] = None


def translate_to(lng: Lang) -> Lang:
    if lng == Lang.CS:
        return Lang.UK
    elif lng == Lang.UK:
        return Lang.CS
    raise ValueError(f"Unsupported language {lng}")


def translate(msg: str, client_name: Optional[str] = None) -> Translation:
    lang = detect_language(msg)
    is_russian = False
    if lang == Lang.RU:
        lang = Lang.UK
        is_russian = True

    frontend = "uk-cs-translation-bot"
    if client_name:
        frontend += f"--{client_name}"

    r = requests.post(
        (
            "https://lindat.cz/translation/api/v2/languages/?"
            f"src={lang.value}&"
            f"tgt={translate_to(lang).value}&"
            f"frontend={frontend}"
        ),
        data={
            "input_text": msg,
        },
        headers={
            "Accept": "application/json",
        },
    )

    if r.status_code == 200:
        res = []
        if is_russian:
            res.append("Je to rusky. / Це по-російськи.")
        res.extend(r.json())
        return Translation(translation=res)
    else:
        return Translation(error=f"Translation failed: {r.reason}")
