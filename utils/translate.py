import enum
import re


class LanguageCode(enum.StrEnum):
    AB = "ab"  # Abkhazian
    AA = "aa"  # Afar
    AF = "af"  # Afrikaans
    AK = "ak"  # Akan
    SQ = "sq"  # Albanian
    AM = "am"  # Amharic
    AR = "ar"  # Arabic
    AN = "an"  # Aragonese
    HY = "hy"  # Armenian
    AS = "as"  # Assamese
    AV = "av"  # Avaric
    AE = "ae"  # Avestan
    AY = "ay"  # Aymara
    AZ = "az"  # Azerbaijani
    BM = "bm"  # Bambara
    BA = "ba"  # Bashkir
    EU = "eu"  # Basque
    BE = "be"  # Belarusian
    BN = "bn"  # Bengali
    BH = "bh"  # Bihari
    BI = "bi"  # Bislama
    BS = "bs"  # Bosnian
    BR = "br"  # Breton
    BG = "bg"  # Bulgarian
    MY = "my"  # Burmese
    CA = "ca"  # Catalan
    CH = "ch"  # Chamorro
    CE = "ce"  # Chechen
    NY = "ny"  # Chichewa
    ZH = "zh"  # Chinese
    CV = "cv"  # Chuvash
    KW = "kw"  # Cornish
    CO = "co"  # Corsican
    CR = "cr"  # Cree
    HR = "hr"  # Croatian
    CS = "cs"  # Czech
    DA = "da"  # Danish
    DV = "dv"  # Divehi
    NL = "nl"  # Dutch
    DZ = "dz"  # Dzongkha
    EN = "en"  # English
    EO = "eo"  # Esperanto
    ET = "et"  # Estonian
    EE = "ee"  # Ewe
    FO = "fo"  # Faroese
    FJ = "fj"  # Fijian
    FI = "fi"  # Finnish
    FR = "fr"  # French
    FF = "ff"  # Fulah
    GL = "gl"  # Galician
    KA = "ka"  # Georgian
    DE = "de"  # German
    EL = "el"  # Greek
    GN = "gn"  # Guarani
    GU = "gu"  # Gujarati
    HT = "ht"  # Haitian
    HA = "ha"  # Hausa
    HE = "he"  # Hebrew
    HZ = "hz"  # Herero
    HI = "hi"  # Hindi
    HO = "ho"  # Hiri Motu
    HU = "hu"  # Hungarian
    IA = "ia"  # Interlingua
    ID = "id"  # Indonesian
    IE = "ie"  # Interlingue
    GA = "ga"  # Irish
    IG = "ig"  # Igbo
    IK = "ik"  # Inupiaq
    IO = "io"  # Ido
    IS = "is"  # Icelandic
    IT = "it"  # Italian
    IU = "iu"  # Inuktitut
    JA = "ja"  # Japanese
    JV = "jv"  # Javanese
    KL = "kl"  # Kalaallisut
    KN = "kn"  # Kannada
    KR = "kr"  # Kanuri
    KS = "ks"  # Kashmiri
    KK = "kk"  # Kazakh
    KM = "km"  # Central Khmer
    KI = "ki"  # Kikuyu
    RW = "rw"  # Kinyarwanda
    KY = "ky"  # Kirghiz
    KV = "kv"  # Komi
    KG = "kg"  # Kongo
    KO = "ko"  # Korean
    KU = "ku"  # Kurdish
    KJ = "kj"  # Kwanyama
    LA = "la"  # Latin
    LB = "lb"  # Luxembourgish
    LG = "lg"  # Ganda
    LI = "li"  # Limburgan
    LN = "ln"  # Lingala
    LO = "lo"  # Lao
    LT = "lt"  # Lithuanian
    LU = "lu"  # Luba-Katanga
    LV = "lv"  # Latvian
    GV = "gv"  # Manx
    MK = "mk"  # Macedonian
    MG = "mg"  # Malagasy
    MS = "ms"  # Malay
    ML = "ml"  # Malayalam
    MT = "mt"  # Maltese
    MI = "mi"  # Maori
    MR = "mr"  # Marathi
    MH = "mh"  # Marshallese
    MN = "mn"  # Mongolian
    NA = "na"  # Nauru
    NV = "nv"  # Navajo
    ND = "nd"  # North Ndebele
    NE = "ne"  # Nepali
    NG = "ng"  # Ndonga
    NB = "nb"  # Norwegian Bokmål
    NN = "nn"  # Norwegian Nynorsk
    NO = "no"  # Norwegian
    II = "ii"  # Sichuan Yi
    NR = "nr"  # South Ndebele
    OC = "oc"  # Occitan
    OJ = "oj"  # Ojibwa
    CU = "cu"  # Church Slavic
    OM = "om"  # Oromo
    OR = "or"  # Oriya
    OS = "os"  # Ossetian
    PA = "pa"  # Panjabi
    PI = "pi"  # Pali
    FA = "fa"  # Persian
    PL = "pl"  # Polish
    PS = "ps"  # Pashto
    PT = "pt"  # Portuguese
    QU = "qu"  # Quechua
    RM = "rm"  # Romansh
    RN = "rn"  # Rundi
    RO = "ro"  # Romanian
    RU = "ru"  # Russian
    SA = "sa"  # Sanskrit
    SC = "sc"  # Sardinian
    SD = "sd"  # Sindhi
    SE = "se"  # Northern Sami
    SM = "sm"  # Samoan
    SG = "sg"  # Sango
    SR = "sr"  # Serbian
    GD = "gd"  # Gaelic
    SN = "sn"  # Shona
    SI = "si"  # Sinhala
    SK = "sk"  # Slovak
    SL = "sl"  # Slovenian
    SO = "so"  # Somali
    ST = "st"  # Southern Sotho
    ES = "es"  # Spanish
    SU = "su"  # Sundanese
    SW = "sw"  # Swahili
    SS = "ss"  # Swati
    SV = "sv"  # Swedish
    TA = "ta"  # Tamil
    TE = "te"  # Telugu
    TG = "tg"  # Tajik
    TH = "th"  # Thai
    TI = "ti"  # Tigrinya
    BO = "bo"  # Tibetan
    TK = "tk"  # Turkmen
    TL = "tl"  # Tagalog
    TN = "tn"  # Tswana
    TO = "to"  # Tonga
    TR = "tr"  # Turkish
    TS = "ts"  # Tsonga
    TT = "tt"  # Tatar
    TW = "tw"  # Twi
    TY = "ty"  # Tahitian
    UG = "ug"  # Uighur
    UK = "uk"  # Ukrainian
    UR = "ur"  # Urdu
    UZ = "uz"  # Uzbek
    VE = "ve"  # Venda
    VI = "vi"  # Vietnamese
    VO = "vo"  # Volapük
    WA = "wa"  # Walloon
    CY = "cy"  # Welsh
    WO = "wo"  # Wolof
    FY = "fy"  # Western Frisian
    XH = "xh"  # Xhosa
    YI = "yi"  # Yiddish
    YO = "yo"  # Yoruba
    ZA = "za"  # Zhuang
    ZU = "zu"  # Zulu


from functools import cached_property
from settings import ROOT_DIR
from pathlib import Path

import pydantic as _p
import typing as _t
import hashlib
import json


class SavedTranslates(_p.BaseModel):
    file_name: _t.ClassVar[str] = "saved_translates.json"
    root_dir: _t.ClassVar[Path] = ROOT_DIR
    path: _t.ClassVar[Path] = root_dir / file_name

    _translates = _p.PrivateAttr()

    if not path.exists():
        path.touch()

    text: str

    def __init__(self, **data):
        super(SavedTranslates, self).__init__(**data)
        self._translates = self.get_file_json

    @property
    def translates(self) -> dict[str, dict[str, str]]:
        return self._translates

    @cached_property
    def get_file_json(self):
        with open(self.path, "r") as f:
            f.seek(0)
            content = f.read()
            data = content if content else "{}"
            return json.loads(data)

    @cached_property
    def encoded_base64_text(self):
        return hashlib.sha256(self.text.encode("utf-8")).hexdigest()

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.translates, f)

    def get(self, language_code: LanguageCode):
        translates = self.translates.get(self.encoded_base64_text, None)
        if not translates:
            return
        return translates.get(language_code)

    def get_translates(self):
        translates = self.translates.get(self.encoded_base64_text, None)
        if translates is None:
            self.translates[self.encoded_base64_text] = {}
            translates = self.translates.get(self.encoded_base64_text)
        assert translates is not None
        return translates

    def set(self, language_code: LanguageCode, text: str):
        translates = self.get_translates()
        translates[language_code] = text
        self.save()


from spy.commands import private, group
from gpytranslate import Translator


t = Translator()


class TranslateStr(str):

    def __new__(cls, *args, **_):
        instance = super(TranslateStr, cls).__new__(cls, *args)
        return instance

    def __init__(self, *str_args, source_language_code: LanguageCode = LanguageCode.EN):
        self.string, *self.args = str_args
        self.source_language_code = source_language_code

    @cached_property
    def bot_commands(self):
        data = list(private) + list(group)
        return ["/" + i.command for i in data]

    @cached_property
    def to_translate(self):
        if (length := len(self)) > (step := 15_000):
            return [self[i : i + step] for i in range(0, length, step)]
        return self

    async def __call__(self, to_lang: LanguageCode, *, exclude: tuple[str] = ()):
        if self.source_language_code == to_lang:
            return self

        saved = SavedTranslates(text=self.string)

        saved_translate = saved.get(to_lang)
        if saved_translate:
            return saved_translate

        to_translate = self

        exclude = list(exclude) + self.formated_parts + self.bot_commands

        for index, text in enumerate(exclude):
            to_translate = to_translate.replace(text, f"__{index}__")

        translated = await t.translate(
            to_translate.to_translate,
            self.source_language_code,
            to_lang,
        )

        if isinstance(translated, list):
            txt = "".join([i.text for i in translated])
        else:
            txt = str(translated.text)

        for index, text in enumerate(exclude):
            txt = txt.replace(f"__{index}__", text)

        saved.set(to_lang, txt)
        return TranslateStr(txt, source_language_code=to_lang)

    def _new(self, text: str):
        return self.__class__(
            text, *self.args, source_language_code=self.source_language_code
        )

    def lower(self) -> "TranslateStr":
        text = super(TranslateStr, self).lower()
        return self._new(text)

    def format(self, *args, **kwargs) -> "TranslateStr":
        text = super(TranslateStr, self).format(*args, **kwargs)
        return self._new(text)

    def replace(self, old: str, new: str, count: int = -1, /):
        text = super(TranslateStr, self).replace(old, new, count)
        return self._new(text)

    @cached_property
    def formated_parts(self):
        return re.findall(r"(\{.*?\})", self)

    def add(self, text: str):
        return self._new(self.string + text)
