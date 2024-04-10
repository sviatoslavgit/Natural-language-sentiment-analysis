import spacy
import requests
from bs4 import BeautifulSoup
import translators as ts
from langdetect import detect


def detect_language(text):
    try:
        language = detect(text)
        return language
    except:
        return "Unable to detect"


def translate_text(text):
    source_language = detect_language(text)
    input_limit = int(1e3)  # Максимальна довжина запиту

    if source_language == 'en':
        translated_text = ""
        for i in range(0, len(text), input_limit):
            translated_text += ts.translate_text(str(text[i:i + input_limit]), translator='bing', from_language="en", to_language="uk")

    elif source_language == 'uk':
        return text
    else:
        translated_text = "Непідтримувана мова. Підтримуються тільки англійська та українська."

    return translated_text


def load_sentiment_dictionary(filename):
    sentiment_dict = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            word, sentiment = line.strip().split('\t')
            sentiment_dict[word.lower()] = float(sentiment)
    return sentiment_dict


def lemmatize_text(text, language):
    nlp = spacy.load(language)
    doc = nlp(text)
    lemmatized_text = " ".join([token.lemma_ for token in doc])
    return lemmatized_text


def get_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        return text
    except Exception as exception:
        return exception


def analyze_text_sentiment(text, sentiment_dict):
    language = 'uk_core_news_sm'
    translated_text = translate_text(text)
    lemmatized_text = lemmatize_text(translated_text, language)
    words = lemmatized_text.split()
    analyzed_words = []
    total_sentiment = 0
    count = 0
    positive_words = 0
    negative_words = 0
    unknown_words = []
    for word in words:
        if word in sentiment_dict:
            total_sentiment += sentiment_dict[word]
            count += 1
            analyzed_words.append(word)
            sentiment = sentiment_dict[word]
            if sentiment >= 0.5:
                positive_words += 1
            else:
                negative_words += 1
        else:
            unknown_words.append(word)
    if count > 0:
        average_sentiment = total_sentiment / count
    else:
        average_sentiment = 0

    return average_sentiment, positive_words, negative_words, analyzed_words
