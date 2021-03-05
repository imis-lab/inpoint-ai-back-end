import os
import sys
import time
import spacy
import fasttext
import functools
import ai.config as config

def load_models():
    """
    Function which loads the english & greek 
    NLP models, as well as the language detection model.
    This needs to run once since all models need a few seconds to load.
    """
    return (
        spacy.load('en_core_web_lg'),
        spacy.load('el_core_news_lg'),
        fasttext.load_model(os.path.realpath(
         os.path.join(sys.path[0], 'ai\lid.176.bin')))
    )


def detect_language(model, text):
    """
    Function that detects the language of a given text,
    using the fasttext algorithm.
    """
    language = model.predict(text, k = 1)[0][0]  # Top 1 matching language.
    
    if language == '__label__en':
        return 'english'
    elif language == '__label__el':
        return 'greek'
    else:
        raise Exception('Unsupported natural language detected!')


def remove_greek_accents(text):
    """
    Function which replaces all greek accented characters
    with non-accented ones.
    """
    gr_accents = {'ά': 'α', 'ό': 'ο', 'ύ': 'υ', 'ί': 'ι', 'έ': 'ε', 'ϊ': 'ι'}
    return ''.join(c if c not in gr_accents else gr_accents[c] for c in text)


def preprocess(text, nlp, language):
    """
    Function which removes all stopwords,
    pronouns and punctuation from the text.
    """
    # Create the document from the lowercased text.
    doc = list(nlp.pipe([text], disable = ['parser', 'ner', 'textcat']))

    # Isolate the useful tokens and join them using a single space.
    if language == 'english':
        return ' '.join(
            token.text.lower() for token in doc[0]
            if token.text not in nlp.Defaults.stop_words
            and token.pos_ in ['NOUN', 'PROPN'] and not token.is_punct
        )
    elif language == 'greek':
        return ' '.join(
            remove_greek_accents(token.text.lower()) for token in doc[0]
            if token.text not in nlp.Defaults.stop_words
            and token.pos_ in ['NOUN', 'PROPN'] and not token.is_punct
        )


def remove_stopwords_from_keyphrases(keyphrases, nlp):
    """
    Function which removes all stopwords,
    from the keyphrases after they have been formed.
    """
    return [
        ' '.join(
            word for word in keyphrase.split()
            if word.lower() not in nlp.Defaults.stop_words
        ) for keyphrase in keyphrases
    ]
            

def counter(func):
    """
    Print the elapsed system time in seconds, 
    if only the debug flag is set to True.
    """
    if not config.debug:
        return func
    @functools.wraps(func)
    def wrapper_counter(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f'{func.__name__}: {end_time - start_time} secs')
        return result
    return wrapper_counter
