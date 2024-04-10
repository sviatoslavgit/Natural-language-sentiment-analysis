import tkinter as tk
from PIL import Image, ImageTk
from func import load_sentiment_dictionary, get_text_from_url, analyze_text_sentiment


def main():
    sentiment_dict = load_sentiment_dictionary('tone-dict-uk-auto.tsv')

    # Створити вікно
    window = tk.Tk()
    window.title("Аналіз тексту")

    # Створити поле для введення URL
    url_label = tk.Label(text="Введіть URL:", master=window)
    url_entry = tk.Entry(width=70, master=window)

    # Створити кнопку для запуску аналізу
    analyze_button = tk.Button(text="Аналізувати", command=lambda: analyze_text(url_entry.get()))

    # Створити рамки для виведення результатів
    results_frame = tk.Frame(master=window)
    sentiment_frame = tk.Frame(master=results_frame)
    words_frame = tk.Frame(master=results_frame)

    # Створити підписи та поля для результатів
    sentiment_label = tk.Label(text="Середнє значення семантичного відтінку тексту:", master=sentiment_frame)
    sentiment_text = tk.Text(height=1, width=20, master=sentiment_frame)

    positive_words_label = tk.Label(text="Кількість позитивних слів:", master=words_frame)
    positive_words_text = tk.Text(height=1, width=20, master=words_frame)

    negative_words_label = tk.Label(text="Кількість негативних слів:", master=words_frame)
    negative_words_text = tk.Text(height=1, width=20, master=words_frame)

    analyzed_words_label = tk.Label(text="Проаналізовані слова:", master=window)
    analyzed_words_text = tk.Text(height=5, width=80, master=window)

    sad_image = ImageTk.PhotoImage(Image.open("sad.png"), width=50, height=50)
    neutral_image = ImageTk.PhotoImage(Image.open("neutral.png"), width=50, height=50)
    happy_image = ImageTk.PhotoImage(Image.open("happy.jpg"), width=50, height=50)

    # Створити мітку для зображення
    image_label = tk.Label(master=results_frame)

    # Розмістити елементи на вікні
    window.geometry("800x450")  # Задати фіксований розмір вікна

    url_label.pack(pady=10)
    url_entry.pack(pady=10)
    analyze_button.pack(pady=10)

    results_frame.pack(fill=tk.BOTH, expand=True)

    sentiment_frame.pack(side=tk.LEFT)
    sentiment_label.pack()
    sentiment_text.pack()

    image_label.pack(padx=10, pady=10)

    words_frame.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
    positive_words_label.pack()
    positive_words_text.pack()
    negative_words_label.pack()
    negative_words_text.pack()
    analyzed_words_label.pack()
    analyzed_words_text.pack()

    def analyze_text(url):
        # Отримати текст з URL
        text = get_text_from_url(url)

        # Проаналізувати текст
        average_sentiment, positive_words, negative_words, analyzed_words = analyze_text_sentiment(text, sentiment_dict)

        # Вивести результати
        sentiment_text.delete("1.0", "end")
        sentiment_text.insert("1.0", "{}".format(average_sentiment))

        positive_words_text.delete("1.0", "end")
        positive_words_text.insert("1.0", "{}".format(positive_words))

        negative_words_text.delete("1.0", "end")
        negative_words_text.insert("1.0", "{}".format(negative_words))

        analyzed_words_text.delete("1.0", "end")
        for word in analyzed_words:
            analyzed_words_text.insert("end", word + " ")

        if average_sentiment >= 0.55 and average_sentiment <= 1:
            image_label.configure(image=happy_image)
        elif average_sentiment >= 0.45 and average_sentiment <= 0.55:
            image_label.configure(image=neutral_image)
        else:
            image_label.configure(image=sad_image)

    # Запустити головне вікно
    window.mainloop()


if __name__ == "__main__":
    main()