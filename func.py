import requests
from bs4 import BeautifulSoup
import translators as ts
from langdetect import detect
from gensim.parsing.preprocessing import preprocess_string


def detect_language(text):
    try:
        language = detect(text)
        return language
    except Exception as e:
        print("Language detection error:", e)
        return "Unable to detect"


def translate_text(text):
    source_language = detect_language(text)
    input_limit = int(1e3)  # Максимальна довжина запиту

    if source_language == 'en':
        translated_text = ""
        for i in range(0, len(text), input_limit):
            translated_text += ts.google(text[i:i + input_limit], 'en', 'uk')

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

def get_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        return text
    except Exception as e:
        print("Error retrieving text from URL:", e)
        return None

def analyze_text_sentiment(text, sentiment_dict):
    translated_text = translate_text(text)
    lemmatized_text = ' '.join(preprocess_string(translated_text))
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
