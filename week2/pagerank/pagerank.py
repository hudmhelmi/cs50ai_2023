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
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Calc the total number of sites in the corpus
    num_sites = len(corpus)

    # Init a dictionary to store site probabilities
    prob_dist = {}

    # Check if the current page is not in the corpus
    if page not in corpus:
        # Assign equal probability to all sites in the corpus
        for site in corpus:
            prob_dist[site] = 1 / num_sites
    else:
        # Assign initial probability to all sites in the corpus
        for site in corpus:
            prob_dist[site] = (1 - damping_factor) / num_sites

        # Calc the number of links on the current page
        links = corpus[page]
        num_links = len(links)

        # Update probabilities for links on the current page
        for link in links:
            prob_dist[link] += damping_factor / num_links

    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Init a dictionary to store PageRank values
    pr = {}

    # Choose a random site to start with
    current_site = random.choice(list(corpus.keys()))

    # Init site counters
    site_counts = {site: 0 for site in corpus}

    # Sample `n - 1` times since first sample has already been done
    for i in range(n - 1):
        # Update site count for the current page
        site_counts[current_site] += 1

        # Calc the probability distribution for the current page
        prob_dist = transition_model(corpus, current_site, damping_factor)

        # Get the list of sites and weights from probability distribution
        site_list = list(prob_dist.keys())
        weight_list = list(prob_dist.values())

        # Choose the next page based on the probability distribution
        next_site = random.choices(site_list, weights=weight_list)[0]

        # Update the current page
        current_site = next_site

    # Calc and normalise PageRank values
    total_site_count = sum(site_counts.values())
    for site, count in site_counts.items():
        pr[site] = count / total_site_count

    return pr


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Get the total number of sites in the corpus
    num_sites = len(corpus)

    # Init equal PageRank values for each site
    pr = {site: 1 / num_sites for site in corpus}

    # Set threshold for convergence
    threshold = 0.001

    # Loop until PageRank values converge
    while True:
        # Create a new dictionary to store updated PageRank values
        new_pr = {}

        # Calculate PageRank for each site in the corpus
        for site in corpus:
            # Calculate backlink PageRank from backlinks to the current site
            backpr = 0
            for backlink in corpus:
                if site in corpus[backlink]:
                    backpr += pr[backlink] / len(corpus[backlink])

            # Update PageRank using the PageRank formula
            new_pr[site] = ((1 - damping_factor) / num_sites) + damping_factor * backpr

        # Check if PageRank values have converged
        has_converged = True
        for site in corpus:
            if abs(new_pr[site] - pr[site]) >= threshold:
                has_converged = False
                break

        # Update PageRank values with the new values
        pr = new_pr

        # If convergence is achieved, exit the loop
        if has_converged:
            break

    # Return the calculated PageRank values for each page
    return pr


if __name__ == "__main__":
    main()
