import srt
from jinja2 import Template
from dataclasses import dataclass
import lemma
import difficulty
import nltk
import sys

@dataclass
class TalkSegment:
    start: float
    end: float
    text: str

basename = sys.argv[1]

segments = []

with open( basename + '.srt', 'r', encoding='utf-8') as f:
    for x in srt.parse(f.read()):
        content = x.content.replace("\n", " ")
        baseform = lemma.lemmatize_sentence( content )
        worddiff = difficulty.WordDifficulty()
        df = list(map(worddiff.getDifficulty, baseform))
        toks = nltk.word_tokenize(content)

        txt_html = ""
        for i, tok in enumerate(toks):
            txt_html += f"""<span class="{df[i]}">{tok}</span> """

        segments.append( TalkSegment( x.start.seconds + x.start.microseconds * 0.000001,
                                      x.end.seconds + x.end.microseconds * 0.000001,
                                      txt_html ) )


def join_segments( segments ):
    joined_segments = []

    multi_segment = segments.pop(0)

    for x in segments:
        if x.start - multi_segment.end > 0.1: # 分離する
            joined_segments.append(multi_segment)
            multi_segment = x
        else:
            multi_segment.end = x.end
            multi_segment.text += ( "\n" + x.text )

    joined_segments.append( multi_segment )

    return joined_segments


def find_group_slices( segments ):
    index = [0]

    for i in range(1, len(segments) ):
        if segments[i].start - segments[i-1].end > 0.1: # 分けるべき
            index.append( i )

    index.append(len(segments))

    return index

slices = find_group_slices(segments)

data = {
    'basename' : basename,
    'margin' : 0.5,
    'items' : segments,
    'slices' : slices,
    'slicelen' : len(slices)
}

template = Template(open("template.html").read())

with open( basename + ".html", 'w', encoding='utf-8') as w:
    print (template.render(data), file=w )
