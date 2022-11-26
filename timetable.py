import srt
import lemma
import difficulty
import pprint
import nltk

with open("out.txt", 'w') as w:
    with open('03.srt', 'r', encoding='utf-8') as f:
        for x in srt.parse(f.read()):
            st = "{}.{:0>6}".format( x.start.seconds-1, x.start.microseconds )
            en = "{}.{:0>6}".format( x.end.seconds+1, x.end.microseconds )
            cn = x.content.replace("\n", " ")
            baseform = lemma.lemmatize_sentence(cn)
            worddiff = difficulty.WordDifficulty()
            df = list( map( worddiff.getDifficulty, baseform ) )

            toks = nltk.word_tokenize(cn)

            txt_html = ""
            for i, x in enumerate(toks):
                txt_html += f"""<span class="{df[i]}">{x}</span> """

            print(f"""<div onclick="video.abLoopPlugin.setStart({st}).setEnd({en}).playLoop()">{txt_html}</div>""", file=w )
