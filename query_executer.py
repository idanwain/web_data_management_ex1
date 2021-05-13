import re
import sys
import rdflib

# Ontology Graph
g = rdflib.Graph()
g.parse("ontology.nt", format="nt")

patterns = [
    'who directed ([^\s].*[^\s])\?',
    'who produced ([^\s].*[^\s])\?',
    'is ([^\s].*[^\s]) based on a book\?',
    'when was ([^\s].*[^\s]) released\?',
    'how long is ([^\s].*[^\s])\?',
    'who starred in ([^\s].*[^\s])\?',
    'did ([^\s].*[^\s]) star in ([^\s].*[^\s])\?',
    'when was ([^\s].*[^\s]) born\?',
    'what is the occupation of ([^\s].*[^\s])\?',
    'how many films are based on books\?',
    'how many films starring ([^\s].*[^\s]) won an academy award\?',
    'how many ([^\s].*[^\s]) are also ([^\s].*[^\s])\?'
]

relations = {
    'who directed ([^\s].*[^\s])\?': 'directed',
    'who produced ([^\s].*[^\s])\?': 'produced',
    'is ([^\s].*[^\s]) based on a book\?': 'based on',
    'when was ([^\s].*[^\s]) released\?': 'released',
    'how long is ([^\s].*[^\s])\?': None,
    'who starred in ([^\s].*[^\s])\?': 'starred in',
    'did ([^\s].*[^\s]) star in ([^\s].*[^\s])\?': 'star in',
    'when was ([^\s].*[^\s]) born\?': 'born',
    'what is the occupation of ([^\s].*[^\s])\?': 'occupation',
    'how many films are based on books\?': 'based on',
    'how many films starring ([^\s].*[^\s]) won an academy award\?': 'starring',
    'how many ([^\s].*[^\s]) are also ([^\s].*[^\s])\?': 'entities'
}


def get_matching_pattern(query):
    for pattern in patterns:
        if re.match(pattern, query):
            return pattern
    return None


def extract_relations(pattern):
    return relations[pattern]


def extract_entities(pattern, query):
    p = re.compile(pattern)
    res = p.findall(query)
    lst = list(res[0])
    return lst


def extract_return_type(pattern):
    pass


def build_sparql_query(entities, relations, ret_type):
    pass


def execute(query: str):
    matching_pattern = get_matching_pattern(query.lower())
    if not matching_pattern:
        print('please enter a valid query.')
        sys.exit(0)
    #  --------- ADD ENTITIES EXTRACTION HERE ----------
    entities = extract_entities(matching_pattern, query)
    relations = extract_relations(matching_pattern)
    ret_type = extract_return_type(matching_pattern)
    sparql_query = build_sparql_query(entities, relations, ret_type)
    x = g.query(sparql_query)
    print(list(x))

    return None
