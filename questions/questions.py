import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 3


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}
    for document in os.listdir(directory):
        path = os.path.join(directory, document)
        f = open(path, "r", encoding="utf8")
        files[document] = f.read()
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    temp = nltk.word_tokenize(document)
    words = []
    for word in temp:
        # filters out punctuation and stopwords and lowercases rest
        if word.lower() not in string.punctuation and word.lower() not in nltk.corpus.stopwords.words("english"):
            words.append(word.lower())
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = {}
    total_documents = len(documents)

    # gets a list of all the unique words
    words = set()
    for x in documents:
        document = set(documents[x])
        words.update(document)

    # computates idfs value for each word
    for word in words:
        appears = 0
        for x in documents:
            if word in documents[x]:
                appears += 1
        idfs[word] = math.log(total_documents/appears)

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    filenames = []

    # creates a dict that keeps track of each file's tf-ifd score
    scores = {
        filename: 0
        for filename in files
    }

    # for each file
    for filename in files:

        # for each word in query
        for word in query:

            # calculates term frequency of word
            tf = files[filename].count(word)

            # updates tf-idf score
            tfidf = tf * idfs[word]
            scores[filename] += tfidf
    
    # returns the top 'n' results
    scores = sorted(scores, key=scores.get, reverse=True)
    for index in range(n):
        filenames.append(scores[index])
    return filenames
       

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_names = []

    # creates a dict that keeps track of each sentence's score
    scores = {
        sentence: 0
        for sentence in sentences
    }

    # for each sentence
    for sentence in sentences:

        # for each word in query
        for word in query:

            # updates score
            if word in sentences[sentence]:
                scores[sentence] += idfs[word]
    
    # returns the top 'n' results
    sorted_scores = sorted(scores, key=scores.get, reverse=True)
    for index in range(n):

        # with preference for higher query term density
        if scores[sorted_scores[index]] == scores[sorted_scores[index + 1]]:
            tie = {}
            score = scores[sorted_scores[index]]
            for n in range(len(sentences)):
                if scores[sorted_scores[index + n]] == score:
                    tie[sorted_scores[index + n]] = 0
                elif scores[sorted_scores[index + n]] < score:
                    break
            
            for sentence in tie.keys():
                term_frequency = len(set(query).intersection(tokenize(sentence))) / len(sentence)
                tie[sentence] = term_frequency
            
            tie = sorted(tie, key=tie.get, reverse=True)
            for n in range(len(tie)):
                sorted_scores[n] = tie[n]

        sentence_names.append(sorted_scores[index])
    return sentence_names


if __name__ == "__main__":
    main()
