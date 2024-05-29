from nltk import bigrams
from collections import defaultdict
import pickle

# Function to provide default value for defaultdict
def default_value():
    return defaultdict(int)

# Function to create a bigram model from a corpus
def build_bigram_model(corpus):
    # Tokenize the corpus into words
    tokens = corpus.split()
    
    # Generate bigrams
    bi_grams = list(bigrams(tokens))
    
    # Create a defaultdict to store the bigram frequencies
    bigram_model = defaultdict(default_value)
    
    # Count frequencies of bigrams in the corpus
    for word1, word2 in bi_grams:
        bigram_model[word1][word2] += 1
    
    # Convert the frequencies to probabilities
    for word1 in bigram_model:
        total_count = float(sum(bigram_model[word1].values()))
        for word2 in bigram_model[word1]:
            bigram_model[word1][word2] /= total_count
    
    return bigram_model

# Read the corpus from file
with open('Spell Check Bigram\Spell Check Bigram\corpus.txt', 'r', encoding='utf-8') as file:
    corpus_text = file.read()

# Build the bigram model
bigram_model = build_bigram_model(corpus_text)

# Save the bigram model to a file
with open('bigram_model.pkl', 'wb') as file:
    pickle.dump(dict(bigram_model), file)
