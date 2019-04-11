import sys
sys.path.append('/nfs/nfs7/home/jingy/.local/lib/python3.5/site-packages')

import spacy
from spacy_cld import LanguageDetector
import en_core_web_sm
import pandas as pd

nlp = en_core_web_sm.load()
from spacy.lang.en import English
language_detector = LanguageDetector()
nlp.add_pipe(language_detector)


def detect_Eng(text):
    doc = nlp(text[0:50])
    if doc._.languages == ['en']:
    	return True
    return False

fandoms = [
'les_miserables_all_media_types',
'star_wars_all_media_types',
'harry_potter',
'sherlock_holmes_&_related_fandoms',
'marvel',
'shakespare_william_works',
'bishoujo_senshi_sailor_moon',
'haikyuu',
'hamilton_miranda',
'kuroko_no_basuke',
'the_walking_dead_&_related_fandoms',
'hetalia_axis_powers',
'naruto',
'buffy_the_vampire_slayer',
'arthurian_mythology_&_related_fandoms',
'ms_paint_adventures',
'one_direction',
'attack_on_titan',
'doctor_who_&_related_fandoms',
'tolkien_j_r_r_works_&_related_fandoms',
'dcu',
'dragon_age_all_media_types',
'supernatural',
]

for fandom in fandoms:
    df = pd.read_csv('../' + fandom + '_preprocessed.tsv', sep = '\t')
    df = df[df.apply(lambda row: detect_Eng(row['Text']), axis=1)]
    df.to_csv(fandom + '_preprocessed2.tsv', sep='\t', index=False)
