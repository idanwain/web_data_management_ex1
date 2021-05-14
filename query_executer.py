import re
import sys
import rdflib

# Ontology Graph
g = rdflib.Graph()
g.parse("ontology.nt", format="nt")

queries = {
    'who directed ([^\s].*[^\s])\?': f'select ?x where {{'
                                     f'{entity1} {relation1} ?x .'
                                     f'}}',
    'who produced ([^\s].*[^\s])\?': f'select ?x where {{'
                                     f'{entity1} {relation1} ?x .'
                                     f'}}',
    'is ([^\s].*[^\s]) based on a book\?': f'select ?x where {{'
                                           f'{entity1} {relation1} ?x .'
                                           f'}}',
    'when was ([^\s].*[^\s]) released\?': f'select ?x where {{'
                                          f'{entity1} {relation1} ?x .'
                                          f'}}',
    'how long is ([^\s].*[^\s])\?': f'select ?x where {{'
                                    f'{entity1} {relation1} ?x .'
                                    f'}}',
    'who starred in ([^\s].*[^\s])\?': f'select ?x where {{'
                                           f'{entity1} {relation1} ?x .'
                                           f'}}',
    'did ([^\s].*[^\s]) star in ([^\s].*[^\s])\?': f'ask where {{'
                                                   f'{entity1} {relation1} {entity2} .'
                                                   f'}}',
    'when was ([^\s].*[^\s]) born\?': f'select ?x where {{'
                                      f'{entity1} {relation1} ?x .'
                                      f'}}',
    'what is the occupation of ([^\s].*[^\s])\?': f'select ?x where {{'
                                                  f'{entity1} {relation1} ?x .'
                                                   f'}}',
    'how many films are based on books\?': f'select distinct * where {{'
                                           f'?film {relation1} ?book .'
                                           f'}}',
    'how many films starring ([^\s].*[^\s]) won an academy award\?': f'select ?x where {{'
                                                                     f'?x {relation1} {entity1}',
    'how many ([^\s].*[^\s]) are also ([^\s].*[^\s])\?': f'select distinct * where {{'
                                                         f' ?x a {relation1} .'
                                                         f' ?x a {relation2} .'
                                                         f'}}'
}

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
    'who directed ([^\s].*[^\s])\?': 'directed_by',
    'who produced ([^\s].*[^\s])\?': 'produced_by',
    'is ([^\s].*[^\s]) based on a book\?': 'based_on',
    'when was ([^\s].*[^\s]) released\?': 'release_date',
    'how long is ([^\s].*[^\s])\?': 'running_time',
    'who starred in ([^\s].*[^\s])\?': 'starring',
    'did ([^\s].*[^\s]) star in ([^\s].*[^\s])\?': 'starring',
    'when was ([^\s].*[^\s]) born\?': 'born',
    'what is the occupation of ([^\s].*[^\s])\?': 'occupation',
    'how many films are based on books\?': 'based_on',
    'how many films starring ([^\s].*[^\s]) won an academy award\?': 'starring',
    'how many ([^\s].*[^\s]) are also ([^\s].*[^\s])\?': 'entities'
}

pattern_type_mapping = {
    "who": "string",
    "is": "boolean",
    "when": "date",
    "how": "int",
    "what": "string",
    "did": "boolean"
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
    res = pattern.split(" ")
    ret_type = pattern_type_mapping[res[0]]
    return ret_type


def replace_spaces(entity1):
    return entity1.replace(" ", "_")


def build_sparql_query(pattern, entities, relations):
    if relations == 'entities':
        relations = entities
    entity1 = ''
    entity2 = ''
    relation1 = ''
    relation2 = ''
    if len(entities) > 0:
        entity1 = entities[0]
    if len(entities) > 1:
        entity2 = entities[1]
    if len(relations) > 0:
        relation1 = relations[0]
    if len(relations) > 1:
        relation2 = relations[1]
    entity1 = replace_spaces(entity1)
    entity2 = replace_spaces(entity2)
    relation1 = replace_spaces(relation1)
    relation2 = replace_spaces(relation2)

    return queries[pattern].format(entity1=entity1, entity2=entity2, relation1=relation1, relation2=relation2)


# TODO: Check for return value from query after building ontology
def get_answer(q, ret_type):
    res = list(q)
    if ret_type == "boolean":
        res = 'Yes' if res[0] else 'No'
    elif ret_type == "int":
        res = len(res)
    return res


def execute(query: str):
    matching_pattern = get_matching_pattern(query.lower())
    if not matching_pattern:
        print('please enter a valid query.')
        sys.exit(0)

    entities = extract_entities(matching_pattern, query)
    relations = extract_relations(matching_pattern)
    ret_type = extract_return_type(matching_pattern)
    sparql_query = build_sparql_query(matching_pattern, entities, relations)
    q = g.query(sparql_query)
    answer = get_answer(q, ret_type)
    print(answer)
