import requests
import matplotlib.pyplot as plt
from collections import defaultdict

# Функція мапінгу
def map_function(text):
    words = text.split()
    return [(word, 1) for word in words]

# Функція шафлінгу
def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

# Функція редукції
def reduce_function(shuffled_values):
    reduced = {}
    for key, values in shuffled_values:
        reduced[key] = sum(values)
    return reduced

# Виконання MapReduce
def map_reduce(text):
    # Крок 1: Мапінг
    mapped_values = map_function(text)

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Крок 3: Редукція
    reduced_values = reduce_function(shuffled_values)

    return reduced_values

# Функція для візуалізації топ слів
def visualize_top_words(word_counts, top_n=10):
    # Сортуємо за кількістю появи слів
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]

    words = [word for word, count in sorted_words]
    counts = [count for word, count in sorted_words]

    # Створення графіка
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='skyblue')
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.show()

if __name__ == '__main__':
    # URL для завантаження тексту
    url = 'https://gutenberg.net.au/ebooks01/0100021.txt'

    # Завантажуємо текст з URL
    response = requests.get(url)
    text = response.text

    # Виконання MapReduce на вхідному тексті
    word_counts = map_reduce(text)

    # Отримуємо топ-10 найбільш поширених слів
    top_n = 10
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Виведення топових слів та їх кількості
    print("Топ-10 найбільш поширених слів:")
    for word, count in sorted_words:
        print(f"{word}: {count}")

    # Підрахунок загальної кількості слів
    total_words = sum(word_counts.values())
    print(f"\nЗагальна кількість слів: {total_words}")

    # Візуалізація топ-10 найпоширеніших слів
    visualize_top_words(word_counts, top_n)
