import re

import streamlit as st
from cutlet import Cutlet

def senter(text):
    """Split long Japanese text into sentences in the most basic way possible.

    The purpose of this function is to avoid dealing with overly long input, so
    it doesn't have to be grammatical sentences.
    """
    sentpunct = r"[\.?!。！？．]"
    offset = 0
    for match in re.finditer(sentpunct, text):
        start, end = match.span()
        yield text[offset:end]
        offset = end
    yield text[offset:]

ZKS = "　" # full width space

def romajify(text, system="hepburn"):
    out = ""
    katsu = Cutlet(system)
    hello = katsu.romaji("こんにち", capitalize=False) + "wa"
    katsu.add_exception("こんにちは", hello)
    for line in text.split("\n"):
        for chunk in line.split(ZKS):
            for sent in senter(chunk):
                out += katsu.romaji(sent) + " "
            out += ZKS
        out += "\n"

    return out

st.set_page_config("cutlet ローマ字変換ツール", 'https://cotonoha.io/android-icon-144x144.png')

st.title("cutlet ローマ字変換")

system = st.radio(
        "ローマ字の種類",
        ("ヘボン式", "訓令式"))

text = st.text_area('変換したいテキストを入力してください', 
        "吾輩は猫である。名前はまだ無い。")


systems = {"ヘボン式": "hepburn", "訓令式": "kunrei"}
system = systems[system]

"# 変換結果"

st.write(romajify(text, system))

st.markdown('<div><a style="width: 200px;margin: 0 auto; display: block" href="https://cotonoha.io"><img src="https://cotonoha.io/cotonoha.png" /></a></div>', unsafe_allow_html=True)
