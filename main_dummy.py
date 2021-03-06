# coding=utf-8
def Vocab_example():
    from vocabulary import Vocab
    # obj = Vocab()
    s = u'ფიდოსაფჯი იოა ფიდჯ საიოჯ ფჯასიოჯფ იდოსაჰგუბწეიონ რეწოი ოოიოიდ'
    obj = Vocab.from_list(list(s))
    obj.printer()

    print(obj[u'f'])
    print(obj[u'f'])
    print(obj[u'f'])

    obj.printer()

def dataset_example():
    from datasets import EditDataSet, EditVocab
    import os
    from aligners import cls_align
    kwargs = {'sigm2017format': False, 'aligner': cls_align, 'param-tying': True, 'language': 'kat'}
    train_data = EditDataSet.from_file(os.path.join('.data', 'Reinflection', 'CleanedData', 'kat.V', 'kat.V.form.dev.txt'), EditVocab(), **kwargs)
    print(u"\n\nPrinting info about the dataset")
    print(u"train_data.vocab = {}".format(train_data.vocab))
    print(u"train_data.training_data = {}".format(train_data.training_data))
    print(u"train_data.length = {}".format(train_data.length))
    print(u"train_data.filename = {}".format(train_data.filename))
    print(u"type(train_data.samples) = {}".format(type(train_data.samples)))
    print(u"train_data.samples[5] = {}".format(train_data.samples[5]))
    print(u"train_data.tag_wraps = {}".format(train_data.tag_wraps))
    print(u"train_data.verbose = {}\n".format(train_data.verbose))

    def print_object(o): # use carefully, might print lots of ...
        from pprint import pprint
        pprint(vars(o))

def phonology_example():
    # This example is taken from the baseline model implementation (PhonologyReinflection), as sanity checks.
    from Word2Phonemes.g2p_config import p2f_dict, langs_properties
    from Word2Phonemes.languages_setup import LanguageSetup

    # made-up words to test the correctness of the g2p/p2g conversions algorithms (for debugging purposes):
    example_words = {'kat': u'არ მჭირდ-ებოდყეტ', 'swc': u"magnchdhe-ong jwng'a", 'sqi': u'rdhëije rrçlldgj-ijdhegnjzh', 'lav': u'abscā t-raķkdzhēļšanģa',
                     'bul': u'най-ясюногщжто', 'hun': u'hűdályiokró- l eéfdzgycsklynndzso nyoyaxy', 'tur': u'yığmalılksar mveğateğwypûrtâşsmış', 'fin': u'ixlmksnngvnk- èeé aatööböyynyissä'}
    for language in example_words:
        # language = 'kat'
        print(u"language = {}".format(language))
        word = example_words[language]

        phon_use_attention = False
        max_feat_size = max([len(p2f_dict[p]) for p in langs_properties[language][0].values() if p in p2f_dict])  # composite phonemes aren't counted in that list

        converter = LanguageSetup(language, langs_properties[language][0], max_feat_size, phon_use_attention, langs_properties[language][1], langs_properties[language][2])

        print(u"word = {}".format(word))
        features_word = converter.word2phonemes(word, 'features')
        # print(u"g -> f => {}".format(features_word))
        reconstructed_word = converter.phonemes2word(features_word, 'features')
        print(u"f -> g => {}".format(reconstructed_word))

        if word == reconstructed_word: print(u"Perfect conversion!")
        # Note: for the last 3 languages, the conversion is not perfect. I specifically chose such
        # problematic examples, but most of the words *are* properly converted.


if __name__ == '__main__':
    # Vocab_example()
    dataset_example()
    # phonology_example()