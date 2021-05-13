import re
import sys
import rdflib

# Ontology Graph
g = rdflib.Graph()
g.parse("graph.nt", format="nt")

patterns = [
    'who directed [^\s].*[^\s]\?',
    'who produced [^\s].*[^\s]\?',
    'is [^\s].*[^\s] based on a book\?',
    'when was [^\s].*[^\s] released\?',
    'how long is [^\s].*[^\s]\?',
    'who starred in [^\s].*[^\s]\?',
    'did [^\s].*[^\s] star in [^\s].*[^\s]\?',
    'when was [^\s].*[^\s] born\?',
    'what is the occupation of [^\s].*[^\s]\?',
    'how many films are based on books\?',
    'how many films starring [^\s].*[^\s] won an academy award\?',
    'how many [^\s].*[^\s] are also [^\s].*[^\s]\?',
]


def get_matching_pattern(query):
    for pattern in patterns:
        if re.match(pattern, query):
            return pattern
    return None


def extract_relation(pattern):
    pass


def execute(query: str):
    matching_pattern = get_matching_pattern(query.lower())
    if not matching_pattern:
        print('please enter a valid query.')
        sys.exit(0)
    #  --------- ADD ENTITIES EXTRACTION HERE ----------
    relations = extract_relation(matching_pattern)
    sparql_query = build_sparql_query()
    x1 = g.query(sparql_query)
    print(list(x1))

    return None
