import sys
import math
import random
from collections import defaultdict

def read_training_file(training_file):
    unigram_counts = defaultdict(int)
    bigram_counts = defaultdict(int)
    sentence_count = 0
    total_words = 0

    with open(training_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            sentence_count += 1
            tokens = line.split()
            tokens = [token.lower() for token in tokens]
            for token in tokens:
                unigram_counts[token] += 1
                total_words += 1
            modified_tokens = ['<s>'] + tokens
            for i in range(len(modified_tokens) - 1):
                prev = modified_tokens[i]
                curr = modified_tokens[i + 1]
                bigram_counts[(prev, curr)] += 1

    V = len(unigram_counts)
    return unigram_counts, bigram_counts, sentence_count, total_words, V

def compute_unigram_logprob(tokens, unigram_counts, total_words):
    logprob = 0.0
    for token in tokens:
        count = unigram_counts.get(token, 0)
        if count == 0:
            return None
        prob = count / total_words
        logprob += math.log2(prob)
    return logprob

def compute_bigram_logprob(tokens, bigram_counts, unigram_counts, sentence_count):
    modified_tokens = ['<s>'] + tokens
    logprob = 0.0
    for i in range(len(modified_tokens) - 1):
        prev = modified_tokens[i]
        curr = modified_tokens[i + 1]
        if prev == '<s>':
            denom = sentence_count
        else:
            denom = unigram_counts.get(prev, 0)
        numer = bigram_counts.get((prev, curr), 0)
        if denom == 0 or numer == 0:
            return None
        prob = numer / denom
        logprob += math.log2(prob)
    return logprob

def compute_smoothed_bigram_logprob(tokens, bigram_counts, unigram_counts, sentence_count, V):
    modified_tokens = ['<s>'] + tokens
    logprob = 0.0
    for i in range(len(modified_tokens) - 1):
        prev = modified_tokens[i]
        curr = modified_tokens[i + 1]
        if prev == '<s>':
            denom = sentence_count + V
        else:
            denom = unigram_counts.get(prev, 0) + V
        numer = bigram_counts.get((prev, curr), 0) + 1
        prob = numer / denom
        logprob += math.log2(prob)
    return logprob

def process_test_sentences(test_file, unigram_counts, bigram_counts, sentence_count, total_words, V, output_file):
    with open(test_file, 'r', encoding='utf-8') as f:
        for line in f:
            original_sentence = line.strip()
            if not original_sentence:
                continue
            tokens = original_sentence.split()
            tokens_lower = [token.lower() for token in tokens]

            uni_logprob = compute_unigram_logprob(tokens_lower, unigram_counts, total_words)
            bi_logprob = compute_bigram_logprob(tokens_lower, bigram_counts, unigram_counts, sentence_count)
            smoothed_bi_logprob = compute_smoothed_bigram_logprob(tokens_lower, bigram_counts, unigram_counts, sentence_count, V)

            output_file.write(f"S = {original_sentence}\n\n")
            uni_str = f"{uni_logprob:.4f}" if uni_logprob is not None else "undefined"
            bi_str = f"{bi_logprob:.4f}" if bi_logprob is not None else "undefined"
            smoothed_bi_str = f"{smoothed_bi_logprob:.4f}" if smoothed_bi_logprob is not None else "undefined"
            output_file.write(f"Unigrams: logprob(S) = {uni_str}\n")
            output_file.write(f"Bigrams: logprob(S) = {bi_str}\n")
            output_file.write(f"Smoothed Bigrams: logprob(S) = {smoothed_bi_str}\n\n")

def generate_sentence(seed, bigram_counts):
    sentence = [seed]
    current_word = seed
    stop_punct = {'.', '?', '!'}
    max_words = 40  

    for _ in range(max_words):
        possible_bigrams = [ (prev, curr) for (prev, curr) in bigram_counts if prev == current_word ]
        if not possible_bigrams:
            break
        next_words = [ curr for (prev, curr) in possible_bigrams ]
        counts = [ bigram_counts[(prev, curr)] for (prev, curr) in possible_bigrams ]
        selected_next = random.choices(next_words, weights=counts, k=1)[0]
        sentence.append(selected_next)
        if selected_next in stop_punct:
            break
        current_word = selected_next

    return ' '.join(sentence)

def process_seeds(seeds_file, bigram_counts, output_file):
    with open(seeds_file, 'r', encoding='utf-8') as f:
        for line in f:
            seed = line.strip().lower()
            if not seed:
                continue
            output_file.write(f"Seed = {seed}\n\n")
            for i in range(10):
                sentence = generate_sentence(seed, bigram_counts)
                output_file.write(f"Sentence {i+1}: {sentence}\n")
            output_file.write("\n")

def main():
    if len(sys.argv) != 4:
        print("Usage: python ngram.py <training file> <test file> <seeds file>")
        sys.exit(1)

    training_file, test_file, seeds_file = sys.argv[1], sys.argv[2], sys.argv[3]

    unigram_counts, bigram_counts, sentence_count, total_words, V = read_training_file(training_file)

    with open('ngram-prob.trace', 'w', encoding='utf-8') as prob_file:
        process_test_sentences(test_file, unigram_counts, bigram_counts, sentence_count, total_words, V, prob_file)

    with open('ngram-gen.trace', 'w', encoding='utf-8') as gen_file:
        process_seeds(seeds_file, bigram_counts, gen_file)

if __name__ == "__main__":
    main()