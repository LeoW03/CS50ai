import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.`
    """
    
    distribution = {}
    # total number of pages in corpus
    total = len(corpus)
    # number of pages current page has
    links = len(corpus[page])
    
    # if page has no outgoing links
    if links == 0:
        for filename in corpus:
            distribution[filename] = (1/total)
        return distribution

    # determines probability distribution
    for filename in corpus:
        # if page is linked to on current page
        if filename in corpus[page]:
            distribution[filename] = damping_factor/links + (1 - damping_factor)/total
        else:
            distribution[filename] = (1 - damping_factor)/total
    return distribution

        

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank = {}
    
    # creates dict to count samples
    samples = {}

    # picks a random page to start
    sample = str(random.choice(list(corpus.keys())))

    # loops through pages according to page probabilities:)
    for page in range(n):
        distribution = transition_model(corpus, sample, damping_factor)
        keys = list(distribution.keys())
        weights = list(distribution.values())
        sample = random.choices((keys), weights = weights)[0]
        samples[sample] = samples.get(sample, 0) + 1

    # converts to estimated PageRank (times visited/total)
    for sample in samples:
        samples[sample] = samples[sample]/n 

    return samples


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """  
    
    # assigns each page a starting rank of 1/(# of pages in corpus)
    ranks = {}
    N = len(corpus)
    for page in corpus:
        ranks[page] = 1/N
    
    # calculates number of links on each page
    links = {}
    for page in corpus:
        if len(corpus[page]) == 0:
            links[page] = len(corpus)
        else:
            links[page] = len(corpus[page])

    # creates a dict to keep track of if PageRank values are accurate enough
    accuracy = {}
    for page in corpus:
        accuracy[page] = False
    counter = 0
    accurate = False

    # recusrivly calclutates new ranks 
    while not accurate:

        # caluates new rank
        sum_other_pages = 0
        current_page = str(random.choice(list(corpus.keys())))
        for page in corpus:
            if page != current_page and current_page in corpus[page]:
                sum_other_pages += ranks[page]/links[page]
        new_rank = (1-damping_factor)/N + damping_factor*sum_other_pages

        # returns ranks once each rank is accurate to within 0.001
        if abs(new_rank - ranks[current_page]) < 0.001:
            accuracy[current_page] = True
        else:
            accuracy[current_page] = False
        if all(page == True for page in accuracy.values()):
            counter += 1 
            if counter > 100:
                accurate = True
        else:
            accurate = False
            counter = 0

        ranks[current_page] = new_rank

    # normalizes PageRanks to add up to 1
    total = 0
    for rank in ranks:
        total += ranks[rank]
    a = 1/total
    for rank in ranks:
        ranks[rank] *= a
    return ranks

if __name__ == "__main__":
    main()
