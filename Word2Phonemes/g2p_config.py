# coding=utf-8
__author__ = "David Guriel"
import json

place = ['labial', 'dental', 'alveolar', 'velarized-alveolar', 'post-alveolar', 'velar', 'uvular', 'glottal', 'palatal'] # 0-8
manner = ['nasal', 'plosive', 'fricative', 'affricate', 'trill', 'tap', 'lateral', 'approximant', 'implosive'] # 9-17
voice = ['voiceless', 'voiced', 'ejective', 'aspirated'] # 18-21
# Vowels features:
height = ['open', 'open-mid', 'mid', 'close-mid', 'close'] # 22-26
backness = ['front', 'back', 'central'] # 27-29
roundness = ['rounded', 'unrounded'] # 30-31
length = ['long'] # only for vowels; no occurence means short vowel # 32
punctuations = [' ', '-', "'", "̇", '.', '*', '?'] # 33-38, '*' is for predictions of non-existent feature bundles (see languages_setup.py)

phon_features = place + manner + voice + height + backness + roundness + length + punctuations
idx2feature = dict(enumerate(phon_features))
feature2idx = {v:k for k, v in idx2feature.items()} # => {'labial':0,...,'nasal':6,...,'front':18,'back':19}

def chain_dictionaries(*dictionaries):
    return {k:v for d in dictionaries for k,v in d.items()}

# for writing the dictionaries, use the command: json.dump({"vowels":p2f_vowels_dict, "consonants":p2f_consonants_dict}, open("phonemes.json","w",encoding='utf8'), indent=2)
phonemes = json.load(open("phonemes.json"))
p2f_consonants = {k:tuple(v) for k,v in phonemes['consonants'].items()}
p2f_vowels     = {k:tuple(v) for k,v in phonemes['vowels'].items()}
p2f_vowels.update({ k+u'ː': v+('long',) for k,v in p2f_vowels.items()}) # account for long vowels (and double their number)
punctuations_g2p_dict = dict(zip(punctuations, punctuations))
p2f_punctuations_dict = dict(zip(punctuations, [tuple(f) for f in punctuations]))
p2f_dict = chain_dictionaries(p2f_vowels, p2f_consonants, p2f_punctuations_dict)
f2p_dict = {v:k for k,v in p2f_dict.items()}
allowed_phoneme_tokens = tuple(p2f_dict.keys())
def feature_in_letter(feature, some_g2p_dict, g): return feature in p2f_dict[some_g2p_dict[g]]

# region definedLangs
# Notes:
# - The structure of lang_components: [lang_g2p_dict, manual_word2phonemes, manual_phonemes2word, lang_clean_sample] - the last is a method for cleaning a line sample.
# - If you wish to add a new language, and a grapheme is mapped to more than a single phoneme (e.g. 'x' -> /ks/), make sure list(grapheme) results in real phonemes.
# region Georgian - kat
kat_alphabet = [u'ა', u'ბ', u'გ', u'დ', u'ე', u'ვ', u'ზ', u'თ', u'ი', u'კ', u'ლ', u'მ', u'ნ', u'ო', u'პ', u'ჟ', u'რ', u'ს', u'ტ', u'უ', u'ფ', u'ქ', u'ღ', u'ყ', u'შ', u'ჩ', u'ც', u'ძ', u'წ', u'ჭ', u'ხ', u'ჯ', u'ჰ']
kat_phonemes = [u'ɑ', u'b', u'ɡ', u'd', u'ɛ', u'v', u'z', u'tʰ', u'i', u'kʼ', u'l', u'm', u'n', u'ɔ', u'pʼ', u'ʒ', u'r', u's', u'tʼ', u'u', u'pʰ', u'kʰ', u'ɣ', u'qʼ', u'ʃ', u't͡ʃʰ', u't͡sʰ', u'd͡z', u't͡sʼ', u't͡ʃʼ', u'x', u'd͡ʒ', u'h']
kat_g2p_dict = dict(zip(kat_alphabet, kat_phonemes))
kat_components = [kat_g2p_dict, None, None, None]
# endregion Georgian - kat


# region Swahili - swc
swc_alphabet = [u'a', u'e', u'i', u'o', u'u',  u'b', u'ch', u'd', u'dh', u'f', u'g', u'gh', u'h', u'j', u'k', u'kh', u'l', u'm', u'n', u'ng', u"ng'", u'ny', u'p', u'r', u's', u'sh', u't', u'th', u'v', u'w', u'y', u'z']
swc_phonemes = [u'ɑ', u'ɛ', u'i', u'ɔ', u'u',  u'ɓ', u't͡ʃ', u'ɗ', u'ð', u'f', u'ɠ', u'ɣ', u'h', u'ʄ', u'k', u'x', u'l', u'm', u'n', u'ɡ', u'ŋ', u'ɲ', u'p', u'r', u's', u'ʃ', u't', u'θ', u'v', u'w', u'j', u'z']
swc_g2p_dict = dict(zip(swc_alphabet, swc_phonemes))
def swc_word2phonemes(w):
    return word2phonemes_with_trigraphs(w, lang='swc')
swc_components = [swc_g2p_dict, swc_word2phonemes, None, None]
# endregion Swahili - swc


# region Albanian - sqi
sqi_alphabet = [u'a', u'b', u'c', u'ç', u'd', u'dh', u'e', u'ë', u'f', u'g', u'gj', u'h', u'i', u'j', u'k', u'l', u'll', u'm', u'n', u'nj', u'o', u'p', u'q', u'r', u'rr', u's', u'sh', u't', u'th', u'u', u'v', u'x', u'xh', u'y', u'z', u'zh']
sqi_phonemes = [u'a', u'b', u't͡s', u't͡ʃ', u'd', u'ð', u'ɛ', u'ə', u'f', u'ɡ', u'ɟ͡ʝ', u'h', u'i', u'j', u'k', u'l', u'ɫ', u'm', u'n', u'ɲ', u'ɔ', u'p', u'c', u'ɹ', u'r', u's', u'ʃ', u't', u'θ', u'u', u'v', u'd͡z', u'd͡ʒ', u'y', u'z', u'ʒ']
sqi_g2p_dict = dict(zip(sqi_alphabet, sqi_phonemes))
def sqi_word2phonemes(w):
    return word2phonemes_with_digraphs(w, lang='sqi')
def sqi_clean_sample(x):
    return x.replace(u"',", u"") # appears in the data only as part of "për t'u ..." (NFIN)
sqi_components = [sqi_g2p_dict, sqi_word2phonemes, None, sqi_clean_sample]
# endregion Albanian - sqi


# region Latvian - lav
lav_alphabet = [u'a', u'ā', u'e',  u'ē', u'i',  u'ī', u'o', u'u',  u'ū', u'b',  u'c',  u'č', u'd', u'dz', u'dž', u'f', u'g', u'ģ', u'h', u'j', u'k', u'ķ', u'l', u'ļ', u'm', u'n', u'ņ', u'p', u'r', u's', u'š', u't', u'v', u'z', u'ž']
lav_phonemes = [u'ɑ', u'ɑː', u'e', u'eː', u'i', u'iː', u'o', u'u', u'uː', u'b', u't̪͡s̪', u't͡ʃ', u'd̪', u'd̪͡z̪', u'd͡ʒ', u'f', u'ɡ', u'ɟ', u'x', u'j', u'k', u'c', u'l', u'ʎ', u'm', u'ŋ', u'ɲ', u'p', u'r', u's', u'ʃ', u't̪', u'v', u'z', u'ʒ']
lav_g2p_dict = chain_dictionaries(dict(zip(lav_alphabet, lav_phonemes)), punctuations_g2p_dict)
lav_p2g_dict = chain_dictionaries(dict(zip(lav_phonemes, lav_alphabet)), punctuations_g2p_dict)
def lav_phonemes2word(phonemes):
    return phonemes2graphemes_with_doubles(phonemes, lang='lav')
def lav_clean_sample(x):
    return x.replace(u'í', u'ī').replace(u'ŗ', u'r').replace("LgSPEC8", "LGSPEC8") # replace the 3 occurences of 'í' with 'ī', and the 28 occ. of 'ŗ'
lav_components = [lav_g2p_dict, None, lav_phonemes2word, lav_clean_sample]
# endregion Latvian - lav


# region Bulgarian - bul
bul_alphabet = [u'а', u'б', u'в', u'г', u'д', u'е', u'ж', u'з', u'и', u'й', u'к', u'л', u'м', u'н', u'о', u'п', u'р', u'с', u'т', u'у', u'ф', u'х', u'ц', u'ч', u'ш', u'щ', u'ъ', u'ь', u'ю', u'я']
bul_phonemes = [u'a', u'b', u'v', u'ɡ', u'd', u'ɛ', u'ʒ', u'z', u'i', u'j', u'k', u'l', u'm', u'n', u'ɔ', u'p', u'r', u's', u't', u'u', u'f', u'x', u't͡s', u't͡ʃ', u'ʃ', u'ʃt', u'ɤ', u'j', u'ju', u'ja']
bul_g2p_dict = chain_dictionaries(dict(zip(bul_alphabet, bul_phonemes)), punctuations_g2p_dict)
bul_p2g_dict = chain_dictionaries(dict(zip(bul_phonemes, bul_alphabet)), punctuations_g2p_dict)
def bul_word2phonemes(w):
    phonemes = []
    for g in w:
        if g in {u'щ', u'ю', u'я'}:
            target_phoneme = list(bul_g2p_dict[g])
        else:
            target_phoneme = bul_g2p_dict[g]
        phonemes.extend(target_phoneme if type(target_phoneme)==list else [target_phoneme])
    return phonemes
def bul_phonemes2word(phonemes):
    special_mappings = {u'j': u'й'} # just never map /j/ to 'ь' ('ь' - 151 vs 'й' - 7217)
    return phonemes2graphemes_with_doubles(phonemes, lang='bul', special_mappings=special_mappings)
bul_components = [bul_g2p_dict, bul_word2phonemes, bul_phonemes2word, None]
# endregion Bulgarian - bul


# region Hungarian - hun
hun_alphabet = [u'a', u'á', u'b', u'c', u'cs', u'd', u'dz', u'dzs', u'e', u'é', u'f', u'g', u'gy', u'h', u'i', u'í', u'j', u'k', u'l', u'ly', u'm', u'n', u'ny', u'o', u'ó', u'ö', u'ő', u'p', u'r', u's', u'sz', u't', u'ty', u'u', u'ú', u'ü', u'ű', u'v', u'w', u'x', u'y', u'z', u'zs']
hun_phonemes = [u'ɒ', u'aː', u'b', u't͡s', u't͡ʃ', u'd', u'd͡z', u'd͡ʒ', u'ɛ', u'eː', u'f', u'ɡ', u'ɟ', u'h', u'i', u'iː', u'j', u'k', u'l', u'ʎ', u'm', u'n', u'ɲ', u'o', u'oː', u'ø', u'øː', u'p', u'r', u'ʃ', u's', u't', u'c', u'u', u'uː', u'y', u'yː', u'v', u'w', u'ks', u'i', u'z', u'ʒ']
hun_g2p_dict = chain_dictionaries(dict(zip(hun_alphabet, hun_phonemes)), punctuations_g2p_dict)
hun_p2g_dict = chain_dictionaries(dict(zip(hun_phonemes, hun_alphabet)), punctuations_g2p_dict)
def hun_word2phonemes(w):
    return word2phonemes_with_trigraphs(w, 'hun')
def hun_phonemes2word(phonemes):
    special_mappings = {u'i': u'i'} # just never map /i/ to 'y' ('y' - 173k vs 'i' - 628k)
    return phonemes2graphemes_with_doubles(phonemes, lang='hun', special_mappings=special_mappings)
def hun_clean_sample(x):
    # the " |or| " is a bug of the scraping from Wiktionary. It can appear at the end of a form
    # (search in the data for "jósolj|or|") or between 2 forms (search for "jóslok |or| jósolok").
    # There are also pipes ("|"), alone or preceded by a space " |".
    # The input is in format of ','.join(input), so the cleaning patterns follow this method.
    chars_to_remove = [','+','.join(" |or| "), ','+','.join("|or|"), ", ,|", ",|"]
    for p in chars_to_remove: x = x.replace(p, "")
    return x
hun_components = [hun_g2p_dict, hun_word2phonemes, hun_phonemes2word, hun_clean_sample]
# endregion Hungarian - hun


# region Turkish - tur
tur_alphabet = [u'a', u'b', u'c', u'ç', u'd', u'e', u'f', u'g', u'ğ', u'h', u'ı', u'i', u'j', u'k', u'l', u'm', u'n', u'o', u'ö', u'p', u'r', u's', u'ş', u't', u'u', u'ü', u'v', u'y', u'z', u'w', u'x' , u'â', u'î', u'û']
tur_phonemes = [u'a', u'b', u'd͡ʒ', u't͡ʃ', u'd', u'ɛ', u'f', u'ɡ', u'j', u'h', u'ɯ', u'i', u'ʒ', u'k', u'l', u'm', u'n', u'o', u'œ', u'p', u'ɾ', u's', u'ʃ', u't', u'u', u'y', u'v', u'j', u'z', u'w', u'ks', u'aː', u'iː', u'uː']
tur_g2p_dict = chain_dictionaries(dict(zip(tur_alphabet, tur_phonemes)), punctuations_g2p_dict)
tur_p2g_dict = chain_dictionaries(dict(zip(tur_phonemes, tur_alphabet)), punctuations_g2p_dict)
def lengthen_last_item(phonemes_list):
    phonemes_list[-1]+='ː'
    return phonemes_list

turkish_vowels = {u'a', u'e', u'i', u'o', u'u', u'ı', u'ö', u'ü', u'â', u'î', u'û'}
turkish_vowels_phonemes = set([tur_g2p_dict[g] for g in turkish_vowels])
def is_tur_vowel(c): return c in turkish_vowels
def is_tur_vowel_phoneme(c): return c in turkish_vowels_phonemes
# [aeiouıöüâîû]ğ
def tur_word2phonemes(graphemes):
    # Turkish has no digraphs, but the conversion of 'ğ' is a little complex, so we don't use word2phonemes_with_digraphs
    phonemes, i = [], 0
    while i < len(graphemes):
        g, resulted_phoneme = graphemes[i], ['']
        if g == u'ğ': # the previous character must be a vowel -- they must obey the regex [aeiouıöüâîû]ğ
            if i==len(graphemes)-1 or graphemes[i+1]==' ': # last letter before whitespace
                phonemes = lengthen_last_item(phonemes)
            else:
                trigraph = graphemes[i - 1: i + 2]
                if is_tur_vowel(trigraph[0]) and is_tur_vowel(trigraph[2]):
                    if trigraph[0] == trigraph[2]:
                        phonemes = lengthen_last_item(phonemes)
                        i += 1
                    # resulted_phoneme = [''] # unnecessary
                elif trigraph[0] == u'e': # i.e. trigraph[2] is not a vowel
                    resulted_phoneme = [u'j']
                else:
                    phonemes = lengthen_last_item(phonemes)
        elif g == u'x':
            resulted_phoneme = [u'k', u's'] # there are only 48 'x' occurences, so will be inversed to ['k', 's']!
        else:
            resulted_phoneme = [tur_g2p_dict[g]]
        if resulted_phoneme != ['']:
            phonemes.extend(resulted_phoneme)
        i += 1
    return phonemes

def tur_phonemes2word(phonemes):
    special_mappings = {u'j': u'y', u'aː': u'â', u'iː': [u'i', u'ğ', u'i'], u'uː': [u'u', u'ğ', u'u'], u'ɛː': [u'e', u'ğ']}
    graphemes, i = [], 0
    while i < len(phonemes):
        p = phonemes[i]
        if p in special_mappings:
            g = special_mappings[p]
        elif 'ː' in p: # a long vowel
            g = [tur_p2g_dict[p[0]], u'ğ']
            if i < len(phonemes)-1 and phonemes[i+1] != u' ':
                g += tur_p2g_dict[p[0]] # add the other grapheme only if it's not the last phoneme.
        elif is_tur_vowel_phoneme(p) and i < len(phonemes)-1 and is_tur_vowel_phoneme(phonemes[i+1]): # p and its follower are distinct vowels
            g = [tur_p2g_dict[p], u'ğ', tur_p2g_dict[phonemes[i+1]]]
            i += 1
        else:
            g = tur_p2g_dict[p]
        graphemes.extend(g if type(g)==list else [g])
        i += 1
    return graphemes
def tur_clean_sample(x):
    return x.replace(u'İ', u'i')
tur_components = [tur_g2p_dict, tur_word2phonemes, tur_phonemes2word, tur_clean_sample]
# endregion Turkish - tur


# region Finnish - fin
fin_alphabet = [u'a', u'è', u'é', u'e', u'i', u'o', u'u', u'y', u'ä', u'ö', u'b', u'c', u'd', u'f', u'g', u'ng', u'nk', u'h', u'j', u'k', u'l', u'm', u'n',
                u'p', u'q', u'r', u's', u'š', u't', u'v', u'w', u'x', u'z', u'ž', u'å', u'aa', u'ee', u'ii', u'oo', u'uu', u'yy', u'ää', u'öö']
fin_phonemes = [u'ɑ', u'e', u'e', u'e', u'i', u'o', u'u', u'y', u'a', u'ø', u'b', u's', u'd', u'f', u'ɡ', u'ŋŋ', u'ŋ', u'h', u'j', u'k', u'l', u'm', u'n',
                u'p', u'k', u'r', u's', u'ʃ', u't', u'v', u'v', u'ks', u't͡s', u'ʒ', u'oː', u'ɑː', u'eː', u'iː', u'oː', u'uː', u'yː', u'aː', u'øː']
fin_g2p_dict = chain_dictionaries(dict(zip(fin_alphabet, fin_phonemes)), punctuations_g2p_dict)
fin_p2g_dict = chain_dictionaries(dict(zip(fin_phonemes, fin_alphabet)), punctuations_g2p_dict)
def fin_word2phonemes(w):
    return word2phonemes_with_digraphs(w, 'fin')
def fin_phonemes2word(phonemes):
    special_mappings = {
        u'e': u'e', # ignore 'é' and 'è'
        u'oː': [u'o', u'o'], # ignore 'å'
        u'k': u'k', # ignore 'q'
        u's': u's', # ignore 'c'
        u'v': u'v',} # ignore 'w'
    result = phonemes2graphemes_with_doubles(phonemes, lang='fin', special_mappings=special_mappings)
    result = list(''.join(result).replace(u'x',u'ks'))
    return result
def fin_clean_sample(x):
    chars_to_remove = [u'\xa0', u":", u"/"]
    for p in chars_to_remove: x = x.replace(p, u"")
    x = x.replace(u"á", u"a").replace(u"â", u"a").replace(u"û", u"u").replace(u"ü", u"u")
    return x
fin_components = [fin_g2p_dict, fin_word2phonemes, fin_phonemes2word, fin_clean_sample]
# endregion Finnish - fin
# endregion definedLangs

langs_properties = {'bul': bul_components, 'fin': fin_components, 'hun': hun_components, 'kat': kat_components,
                    'lav': lav_components, 'sqi': sqi_components, 'swc': swc_components, 'tur': tur_components}
for k in langs_properties:
    if langs_properties[k][3] is None:
        langs_properties[k][3] = lambda x: x

def word2phonemes_with_digraphs(w, lang, allowed_phoneme_tokens = allowed_phoneme_tokens):
    # Convert the graphemes to a list of phonemes according to the langauge's digraphs
    g2p_mapping = langs_properties[lang][0]
    digraphs = list(filter(lambda g: len(g) == 2, g2p_mapping.keys()))
    phonemes, i, flag = [], 0, False
    while i < len(w):
        if i < len(w)-1 and w[i]+w[i+1] in digraphs:
            phoneme_token = g2p_mapping[w[i] + w[i + 1]]
            i += 1
        else:
            phoneme_token = g2p_mapping[w[i]]
        if phoneme_token not in allowed_phoneme_tokens: # need to decompose to real phonemes
            phoneme_token = list(phoneme_token)
        phonemes.extend(phoneme_token if type(phoneme_token) == list else [phoneme_token])
        i += 1
    return phonemes

def word2phonemes_with_trigraphs(w, lang, allowed_phoneme_tokens = allowed_phoneme_tokens):
    # Convert the graphemes to a list of phonemes according to the langauge's trigraphs & digraphs
    g2p_mapping = langs_properties[lang][0]
    digraphs = list(filter(lambda x: len(x)==2, g2p_mapping.keys()))
    trigraphs = list(filter(lambda x: len(x)==3, g2p_mapping.keys()))
    phonemes, i, flag = [], 0, False
    while i < len(w):
        if i < len(w)-2 and w[i]+w[i+1]+w[i+2] in trigraphs:
            phoneme_token = g2p_mapping[w[i]+w[i+1]+w[i+2]]
            i += 2
        elif i < len(w)-1 and w[i]+w[i+1] in digraphs:
            phoneme_token = g2p_mapping[w[i] + w[i + 1]]
            i += 1
        else:
            phoneme_token = g2p_mapping[w[i]]
        if phoneme_token not in allowed_phoneme_tokens: # need to decompose to real phonemes
            phoneme_token = list(phoneme_token)
        phonemes.extend(phoneme_token if type(phoneme_token) == list else [phoneme_token])
        i += 1
    return phonemes

def phonemes2graphemes_with_doubles(w, lang, special_mappings = None):
    # Convert the phonemes to a list of graphemes according to the langauge's double-phonemes.
    # special_mappings is a dictionary that intentionally ignores other possible graphemes at the g2p dictionary.
    p2g_mapping = {v:k for k,v in langs_properties[lang][0].items()}
    phoneme_doubles = list(filter(lambda x: len(x) > 1 and x not in allowed_phoneme_tokens, p2g_mapping.keys()))
    graphemes, i, flag = [], 0, False
    while i < len(w):
        if i < len(w)-1 and w[i]+w[i+1] in phoneme_doubles:
            grapheme_token = p2g_mapping[w[i] + w[i + 1]]
            i += 1
        else:
            if special_mappings is not None and w[i] in special_mappings: # assuming the sepcial mappings occur only in single real phonemes.
                grapheme_token = special_mappings[w[i]]
            else:
                grapheme_token = p2g_mapping[w[i]]
        grapheme_token = list(grapheme_token)
        graphemes.extend(grapheme_token)
        i += 1
    return graphemes

# for further debugging purposes:
def is_g2p_1to1(d): return len(d.values())==len(set(d.values()))
def are_there_phonemes_unincluded_intheJSON(lang_phonemes): return [p for p in lang_phonemes if p not in p2f_dict.keys()]

# region manually inserting g-p pairs
# (copy that section to the console and insert; once done, copy back to the script.
# k,v, d = 'a', 'ɑ', {} # initial pair
# while (k,v)!=('',''):
#     d[k]=v
#     k,v = input("insert k"), input("insert v")
# endregion manually inserting g-p pairs:
# region analyze characters in the data
# def analyze_characters_in_data(lang):
#     from os.path import join
#     vocab = list(set(list(open(join(".data", "RawData", f"{lang}.txt"), encoding='utf8').read())))
#     vocab.sort()
#     print(f'Characters in {lang} data:')
#     print(vocab, '\n')
# for l in ['kat', 'swc', 'sqi', 'lav', 'bul', 'hun', 'tur', 'fin']:
#     analyze_characters_in_data(l)
# endregion analyze characters in the data
