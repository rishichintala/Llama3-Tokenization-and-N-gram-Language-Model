import os
from transformers import AutoTokenizer

def save_tokenizer_to_local(remote_model_name: str, local_model_path: str):
    tokenizer = AutoTokenizer.from_pretrained(remote_model_name)
    print(f"tokenizer loaded from {remote_model_name}")
    tokenizer.save_pretrained(local_model_path)
    print(f"tokenizer saved at {local_model_path}")
    return tokenizer

def save_vocab(tokenizer: AutoTokenizer, vocab_path: str):
    vocab_dict = tokenizer.get_vocab()
    sorted_items = sorted(vocab_dict.items(), key=lambda item: item[1])
    print("start saving")
    with open(vocab_path, "w") as f:
        for word, value in sorted_items:
            #print(word, value)
            f.write(word + "\n")
    print(f"vocab.txt saved at {vocab_path}")
    return tokenizer

def load_local_tokenizer(local_model_path: str):
    tokenizer = AutoTokenizer.from_pretrained(local_model_path)
    print(f"tokenizer loaded from {local_model_path}")
    return tokenizer