"""
CPE 202 Project 4
Author: Micah Jeffries
"""

import os
import sys
import math
from hashtables import HashTableLinear as HashMap
from hashtables import import_stopwords
from hashtables import hash_string

class SearchEngine:
    """class for search engine
    Attributes:
        directory (str): a directory name
        stopwords (HashMap): a hash table containing stopwords
        doc_length (HashMap): a hash table containing the total number of words in each document
        term_freqs (HashMap): a hash table of hash tables for each term. Each hash table contains
        the frequency of the term in documents
    """
    def __init__(self, directory, stopwords):
        self.doc_length = HashMap()
        self.term_freqs = HashMap()
        self.stopwords = stopwords
        self.index_files(directory)

    def read_file(self, infile):
        """A helper function to read a file
        Args:
            infile (str) : the path to a file
        Returns:
            list : a list of str read from a file
        """
        # Use the with block to read an input file
        # Seperate the input file into seperate lines and return those lines
        data = []
        with open(infile, 'r') as f:
            for info in f:
                data.append(info.split('\n'))
        lines = []
        for line in data:
            if line[0] != '':
                lines.append(line[0])
        return lines

    def parse_words(self, lines):
        """split strings into words
        Convert words to lower cases and remove new line chars.
        Exclude stopwords.
        Args:
            lines (list) : a list of strings
        Returns:
            list : a list of words
        """
        # Join the list of lines into one string
        # Remove unecessary punctuation such as parenthesis, periods, and commas
        # Return a list of words excluding stopwords using a helper function
        lines = ''.join(lines)
        lines = lines.lower()
        lines = lines.strip('\n')
        lines = lines.replace('(', '')
        lines = lines.replace(')', '')
        lines = lines.replace(',', '')
        lines = lines.replace('.', ' ')
        lines = lines.split(' ')
        return self.exclude_stopwords(lines)

    def exclude_stopwords(self, terms):
        """exclude stopwords from the list of terms
        Args:
            terms (list) :
        Returns:
            list : a list of str with stopwords removed
        """
        # Return the same input list excluding words that are in the stopwords Hash table
        return [term for term in terms if term not in self.stopwords and term != '']
    
    def count_words(self, filename, words):
        """count words in a file and store the frequency of each
        word in the term_freqs hash table. The keys of the term_freqs hash table shall be
        words. The values of the term_freqs hash table shall be hash tables (term_freqs
        is a hash table of hash tables). The keys of the hash tables (inner hash table) stored
        in the term_freqs shall be file names. The values of the inner hash tables shall be
        the frequencies of words. For example, self.term_freqs[word][filename] += 1;
        Words should not contain stopwords.
        Also store the total count of words contained in the file in the doc_length hash table.
        Args:
            filename (str) : the file name
            words (list) : a list of words
        """
        # For every word in the list of words
            # Count the amount of times that word occurs in a given input file
            # Store the filename and frequency as a key-value pair inside an inner hash table
            # Store this inner hash table as the value of another hash table with word as the key
        # Store the length of the document in the doc_length hashtable
        ht = self.term_freqs
        for word in words:
            frequency = words.count(word)
            if word in ht.keys:
                ht[word].put(filename, frequency)
            else:
                ht.put(word)
                inner_hash = HashMap()
                inner_hash.put(filename, frequency)
                self.term_freqs[word] = inner_hash
        self.doc_length.put(filename, len(words))

    def index_files(self, directory):
        """index all text files in a given directory
        Args:
            directory (str) : the path of a directory
        """
        # For each file in a given input directory
            # Join the file and the directory
            # For each item that is a file and not a directory
                # Split the item to determine if it is a text file
                # If the item is a text file
                    # Count the words for the given text file and index them in term_freqs
        for item in os.listdir(directory):
            item = os.path.join(directory, item)
            if os.path.isfile(item):
                parts = os.path.splitext(item)
                if parts[1] == '.txt':
                    filename = item.split('/')
                    filename = filename[-1]
                    self.count_words(filename, self.parse_words(self.read_file(filename)))

    def get_wf(self, tf):
        """comptes the weighted frequency
        Args:
            tf (float) : term frequency
        Returns:
            float : the weighted frequency
        """
        # Calculate the weighted frequency of a term frequency using the log function
        # Return the new weighted frequency
        if tf > 0:
            wf = 1 + math.log(tf)
        else:
            wf = 0
        return wf

    def get_scores(self, terms):
        """creates a list of scores for each file in corpus
        The score = weighted frequency / the total word count in the file.
        Compute this score for each term in a query and sum all the scores.
        Args:
            terms (list) : a list of str
        Returns:
            list : a list of tuples, each containing the filename and its relevancy score
        """
        # Create a new hash table to keep track of the scores of the search
        # Insert each document from the doc_length hash table into the score hash table
        # For each term in the input terms
            # Retrieve the inner hash table from the term_freqs hash table and assign it as word
            # For each file in the word hash table
                # Retrieve the frequency from the word hash table
                # Calculate the new weighted frequency and insert it into the scores hash table
        # For each file in the scores hash table
            # Retrieve the frequency from the score hash table
            # Normalize the frequency by dividing itself by the length of the document
            # Assign this new value in this scores hash table
        # For each score in the scores hash table
            # Append the score along with the filename in a tuple to a score list
        # Return this score list
        self.term_freqs['adt']['hash_table.txt'] = None
        scores = HashMap()
        documents = self.doc_length.keys
        for document in documents:
            scores.put(document)
        for term in terms:
            term = term.lower()
            try:
                word = self.term_freqs[term]
                for filename in word.keys:
                    if filename and word[filename]:
                        frequency = word[filename]
                        new_freq = self.get_wf(frequency)
                        scores[filename] += new_freq
            except:
                print('Not Found')

        for filename in scores.keys:
            if filename and scores[filename]:
                frequency = scores[filename]
                frequency /= self.doc_length[filename]
                scores[filename] = frequency

        score_list = []
        for filename in scores.keys:
            if filename and scores[filename] != 0:
                score_list.append((filename, scores[filename]))
        #print(score_list)
        return score_list

    def rank(self, scores):
        """ranks files in the descending order of relevancy
        Args:
            scores(list) : a list of tuples: (filename, score)
        Returns:
            list : a list of tuples: (filename, score) sorted in descending order of relevancy
        """
        # Return a sorted list in descending order of relevancy by comparing scores of each file
        return sorted(scores, key=lambda x:x[1], reverse=True)

    def search(self, query):
        """ search for the query terms in files
        Args:
            query (str) : query input
        Returns:
            list : list of files in descending order or relevancy
        """
        # Parse the words from the user input
        # Calculate the relevancy score for each word and rank them based on their score
        # Return this sorted list of relevancy scores along with their filenames
        words = self.parse_words(query)
        return self.rank(self.get_scores(words))

def main():

    stopwords = HashMap()
    import_stopwords('stop_words.txt', stopwords)
    directory = sys.argv[1]
    SE = SearchEngine(directory, stopwords)
    user_input = input("\n(S:)earch or (q)uit: ")
    while user_input != 'q':
        results = SE.search(user_input[2:])
        for result in results:
            result = os.path.join(directory, result[0])
            print(result)
        user_input = input("\n(S:)earch or (q)uit: ")
    

if __name__ == '__main__':
    main()
