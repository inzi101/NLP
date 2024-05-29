from flask import Flask, render_template, request
import pickle
import re
import os

app = Flask(__name__)

# Load the bigram model from the file
def load_bigram_model(model_file):
    with open(model_file, 'rb') as file:
        bigram_model = pickle.load(file)
    return bigram_model

# Function to count common letters between two words
def count_common_letters(word1, word2):
    return len(set(word1) & set(word2))

# Function to create a dictionary of suggestions based on common letters
def create_suggestions_dictionary(mistake, bigram_model, check_word, first_word):
    suggestions_dict = {}
    for next_word in bigram_model:
        if any(char in next_word for char in mistake):  # Check if there's at least one common letter
            common_letters = count_common_letters(mistake, next_word)
            if first_word:
                perplexity = bigram_model[next_word].get(check_word, float('inf'))
            else:
                perplexity = bigram_model[check_word].get(next_word, float('inf'))
            suggestions_dict[next_word] = (common_letters, perplexity)
    # Sort suggestions based on the number of common letters and take top 30
    sorted_suggestions = sorted(suggestions_dict.items(), key=lambda item: (item[1][0], item[1][1]), reverse=True)[:30]
    return dict(sorted_suggestions)

# Function to remove punctuations from text
def remove_punctuations(text):
    return re.sub(r'[^\w\s]', '', text)

# Function to remove punctuations from suggestions
def remove_punctuations_from_suggestions(suggestions):
    return [remove_punctuations(suggestion) for suggestion in suggestions]

# Function to rank suggestions based on the absolute difference of their lengths
def rank_suggestions(mistake, suggestions):
    return sorted(suggestions, key=lambda suggestion: abs(len(suggestion) - len(mistake)))

# Checkpoint function
def checkpoint(sentence):
    bigram_model = load_bigram_model('bigram_model.pkl')

    # Step 2: Find the mistake(s)
    mistakes = [(word, i) for i, word in enumerate(sentence.split()) if word not in bigram_model]

    # Step 3: Remove punctuations from the mistakes
    mistakes = [(remove_punctuations(mistake), index) for mistake, index in mistakes]

    # Step 4: Find suggestions and store them
    replacements = {}
    for mistake, mistake_index in mistakes:
        if mistake_index == 0:
            first_word = True
            check_word = sentence.split()[mistake_index + 1]
        else:
            first_word = False
            check_word = sentence.split()[mistake_index - 1]
        if check_word in bigram_model:
            suggestions = create_suggestions_dictionary(mistake, bigram_model, check_word, first_word)
            replacements[mistake] = suggestions

    # Step 7: Further filter suggestions based on perplexity and rank them
    for mistake, suggestions in replacements.items():
        replacements[mistake] = list(suggestions.keys())[:10]  # Taking top 10 suggestions

    # Step 8: Remove punctuations from suggestions
    for mistake, suggestions in replacements.items():
        replacements[mistake] = remove_punctuations_from_suggestions(suggestions)

    # Step 9: Rank suggestions based on the absolute difference of their lengths
    for mistake, suggestions in replacements.items():
        replacements[mistake] = rank_suggestions(mistake, suggestions)[:10]  # Taking top 10 suggestions

    return replacements

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/text', methods=['GET', 'POST'])
def upload_text():
    if request.method == 'POST' and 'textupload' in request.form:
        sen = request.form['textupload']
        replacements = checkpoint(sen)
        return render_template('index.html', replace=replacements)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
