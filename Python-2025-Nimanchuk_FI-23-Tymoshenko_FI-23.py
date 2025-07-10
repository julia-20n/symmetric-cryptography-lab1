import re, math, chardet
from collections import Counter

file_path = "Kennan_Kochevaya-zhizn-v-Sibiri_RuLit_Me.txt"

with open(file_path, "rb") as f:
    raw_data = f.read()
encoding_info = chardet.detect(raw_data)
detected_encoding = encoding_info["encoding"]
print(f"Detected encoding: {detected_encoding}")

def load_text(filename, remove_spaces=False):
    with open(filename, "r", encoding=detected_encoding, errors="replace") as file:
        text = file.read().lower()
    text = text.replace("ё", "е").replace("ъ", "ь")
    text = re.sub(r'[^а-я ]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    if remove_spaces:
        text = text.replace(" ", "")
    return text

def count_freq(text, step=1, size=1):
    items = [text[i:i+size] for i in range(0, len(text) - size + 1, step)]
    counts = Counter(items)
    total = sum(counts.values())
    return {key: val / total for key, val in counts.items()}

def entropy(freqs, size):
    return -sum(p * math.log2(p) for p in freqs.values() if p > 0) / size

def redundancy(entropy_value, alphabet_size):
    H_0 = math.log2(alphabet_size)  # Максимальна можлива ентропія
    return (1 - entropy_value / H_0)   # Перетворюємо у відсотки

def print_results(title, freqs, size, alphabet_size, results):
    print(f"\n{title}:")
    sorted_freqs = sorted(freqs.items(), key=lambda x: x[1], reverse=True)
    for key, prob in sorted_freqs:
        print(f"{key}: {prob:.6f}")

    H = entropy(freqs, size)
    R = redundancy(H, alphabet_size)
    print(f"Ентропія: {H:.4f}")
    print(f"Надлишковість: {R:.2f}")
    results.append(R)

def analyze_text(filename):
    results = []

    print("\n--- Аналіз тексту з пробілами ---")
    text = load_text(filename, remove_spaces=False)
    letters = count_freq(text, step=1, size=1)
    bigrams_overlap = count_freq(text, step=1, size=2)
    bigrams_n_overlap = count_freq(text, step=2, size=2)
    print_results("Частоти літер", letters, 1, 33, results)
    print_results("Частоти біграм (з перекриттям)", bigrams_overlap, 2, 33**2, results)
    print_results("Частоти біграм (без перекриття)", bigrams_n_overlap, 2, 33**2, results)

    print("\n--- Аналіз тексту без пробілів ---")
    text_no_spaces = load_text(filename, remove_spaces=True)
    letters_no_spaces = count_freq(text_no_spaces, step=1, size=1)
    bigrams_overlap_no_spaces = count_freq(text_no_spaces, step=1, size=2)
    bigrams_n_overlap_no_spaces = count_freq(text_no_spaces, step=2, size=2)
    print_results("Частоти літер (без пробілів)", letters_no_spaces, 1, 32, results)
    print_results("Частоти біграм (з перекриттям, без пробілів)", bigrams_overlap_no_spaces, 2, 32**2, results)
    print_results("Частоти біграм (без перекриття, без пробілів)", bigrams_n_overlap_no_spaces, 2, 32**2, results)

    avg_redundancy = sum(results) / len(results) * 100
    print(f"\nСумарна середня надлишковість: {avg_redundancy:.2f}%")

analyze_text(file_path)
