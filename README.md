### for environment setup , i followed the following commands

import the environment.yml under our root assignment folder, and create and activate your environment via the setup_tutorial.ipynb.

mamba env create -n cs5293-1 -f environment.yml


mamba activate cs5293-1


### How to Run

Prerequisites: Python 3.10 

Make sure you are in src directory

### To Run:

python ngram.py ../data/training.txt ../data/test.txt ../data/seeds.txt

### Output Files:

ngram-prob.trace: Log probabilities for test sentences.

ngram-gen.trace: Generated sentences for each seed.

### Known Issues

Unseen Words/Bigrams: Logprob = undefined for unseen words/bigrams.

Case Insensitivity: All words are converted to lowercase.

Repetition: Small training data may lead to repetitive outputs.

Sentence Length: Stops at 40 words or punctuation (., ?, !).
