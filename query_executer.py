import re
import sys
import rdflib

# Ontology Graph
g = rdflib.Graph()
g.parse("ontology.nt", format="nt")
example_url = "<http://example.org/"
invalid_chars = [',', ':']

queries = {
    'Who directed ([^\s].*[^\s])\?': 'select ?x where {{'
                                     '{entity1} {relation1} ?x .'
                                     '}}',
    'Who produced ([^\s].*[^\s])\?': 'select ?x where {{'
                                     '{entity1} {relation1} ?x .'
                                     '}}',
    'Is ([^\s].*[^\s]) based on a book\?': 'select ?x where {{'
                                           '{entity1} {relation1} ?x .'
                                           '}}',
    'When was ([^\s].*[^\s]) released\?': 'select ?x where {{'
                                          '{entity1} {relation1} ?x .'
                                          '}}',
    'How long is ([^\s].*[^\s])\?': 'select ?x where {{'
                                    '{entity1} {relation1} ?x .'
                                    '}}',
    'Who starred in ([^\s].*[^\s])\?': 'select ?x where {{'
                                       '{entity1} {relation1} ?x .'
                                       '}}',
    'Did ([^\s].*[^\s]) star in ([^\s].*[^\s])\?': 'ask where {{'
                                                   '{entity2} {relation1} {entity1} .'
                                                   '}}',
    'When was ([^\s].*[^\s]) born\?': 'select ?x where {{'
                                      '{entity1} {relation1} ?x .'
                                      '}}',
    'What is the occupation of ([^\s].*[^\s])\?': 'select ?x where {{'
                                                  '{entity1} {relation1} ?x .'
                                                  '}}',
    'How many films are based on books\?': 'select distinct ?film where {{'
                                           '?film {relation1} ?book .'
                                           '}}',
    'How many films starring ([^\s].*[^\s]) won an academy award\?': 'select ?x where {{'
                                                                     '?x {relation1} {entity1} .'
                                                                     '}}',
    'How many ([^\s].*[^\s]) are also ([^\s].*[^\s])\?': 'select ?x where {{'
                                                         ' ?x <http://example.org/Occupation> {relation1} .'
                                                         ' ?x <http://example.org/Occupation> {relation2} .'
                                                         '}}',
    'Does ([^\s].*[^\s]) have children\?': 'select ?x where {{'
                                           '{entity1} {relation1} ?x .'
                                           '}}'
}

patterns = [
    'Who directed ([^\s].*[^\s])\?',
    'Who produced ([^\s].*[^\s])\?',
    'Is ([^\s].*[^\s]) based on a book\?',
    'When was ([^\s].*[^\s]) released\?',
    'How long is ([^\s].*[^\s])\?',
    'Who starred in ([^\s].*[^\s])\?',
    'Did ([^\s].*[^\s]) star in ([^\s].*[^\s])\?',
    'When was ([^\s].*[^\s]) born\?',
    'What is the occupation of ([^\s].*[^\s])\?',
    'How many films are based on books\?',
    'How many films starring ([^\s].*[^\s]) won an academy award\?',
    'How many ([^\s].*[^\s]) are also ([^\s].*[^\s])\?',
    'Does ([^\s].*[^\s]) have children\?'
]

relations = {
    'Who directed ([^\s].*[^\s])\?': 'Directed_by',
    'Who produced ([^\s].*[^\s])\?': 'Produced_by',
    'Is ([^\s].*[^\s]) based on a book\?': 'Based_on',
    'When was ([^\s].*[^\s]) released\?': 'Release_date',
    'How long is ([^\s].*[^\s])\?': 'Running_time',
    'Who starred in ([^\s].*[^\s])\?': 'Starring',
    'Did ([^\s].*[^\s]) star in ([^\s].*[^\s])\?': 'Starring',
    'When was ([^\s].*[^\s]) born\?': 'Born',
    'What is the occupation of ([^\s].*[^\s])\?': 'Occupation',
    'How many films are based on books\?': 'Based_on',
    'How many films starring ([^\s].*[^\s]) won an academy award\?': 'Starring',
    'How many ([^\s].*[^\s]) are also ([^\s].*[^\s])\?': 'Entities',
    'Does ([^\s].*[^\s]) have children\?': 'Children'
}

pattern_type_mapping = {
    "Who": "string",
    "Is": "boolean",
    "When": "date",
    "How": "int",
    "What": "string",
    "Did": "boolean",
    "Does": "boolean"
}


def get_matching_pattern(query):
    for pattern in patterns:
        if re.match(pattern, query):
            return pattern
    return None


def extract_relations(pattern):
    return [relations[pattern]]


def extract_entities(pattern, query):
    p = re.compile(pattern)
    res = p.findall(query)
    if type(res[0]) == tuple:
        return res[0]
    return res


def extract_return_type(pattern):
    res = pattern.split(" ")
    ret_type = pattern_type_mapping[res[0]]
    if ret_type == 'int' and res[1] == 'long':
        ret_type = 'string'
    return ret_type


def replace_spaces(entity1):
    return entity1.replace(" ", "_")


def build_sparql_query(pattern, entities, relations):
    if 'Entities' in relations:
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

    return queries[pattern].format(entity1=example_url + entity1 + ">", entity2=example_url + entity2 + ">",
                                   relation1=example_url + relation1 + ">", relation2=example_url + relation2 + ">")


# TODO: Check for return value from query after building ontology
def get_answer(q, ret_type, matching_pattern):
    res = list(q)
    # print(res)
    if ret_type == "boolean":
        res = 'Yes' if len(res) > 0 and res[0] else 'No'
        return res
    elif ret_type == "int":
        res = len(res)
        return res
    else:
        answer_list = []
        for answer in res:
            answer = answer[0].split('/')[-1].replace('_', ' ')
            if answer and answer not in invalid_chars:
                answer_list.append(answer)
        if matching_pattern == 'What is the occupation of ([^\s].*[^\s])\?':
            answer_list = [a.lower().strip(',').strip() for a in answer_list]
            if len(answer_list) > 0 and ',' in answer_list[0]:
                answer_list = answer_list[0].split(', ')
        answer_list.sort()
        return ', '.join(answer_list)


def execute(query: str):
    matching_pattern = get_matching_pattern(query)
    if not matching_pattern:
        print('please enter a valid query.')
        sys.exit(0)
    entities = extract_entities(matching_pattern, query)
    # print(entities)
    relations = extract_relations(matching_pattern)
    # print(relations)
    ret_type = extract_return_type(matching_pattern)
    # print(ret_type)
    sparql_query = build_sparql_query(matching_pattern, entities, relations)
    # print(sparql_query)
    q = g.query(sparql_query)
    answer = get_answer(q, ret_type, matching_pattern)
    # print(answer)
    return str(answer)


# execute("did Leonardo star in Titanic?")
# execute("When was Nicolas Cage born?")
# execute("Who directed Bao (film)?")
# execute("Who produced 12 Years a Slave (film)?")
# execute("Is The Jungle Book (2016 film) based on a book?")
# execute("When was The Great Gatsby (2013 film) released?")
# execute("How long is Coco (2017 film)?")
# execute("Who starred in The Shape of Water?")
# execute("Did Octavia Spencer star in The Shape of Water?")
# execute("When was Chadwick Boseman born?")
# execute("What is the occupation of Emma Watson?")
# execute("How many films starring Meryl Streep won an academy award?")
# execute("Who produced Brave (2012 film)?")
# execute("Is Brave (2012 film) based on a book?")
# execute("How many films are based on books?")
# execute("How many actor are also film director?")
# execute("What is the occupation of Florian Zeller?")
# execute("Does Thomas Bo Larsen have children?")
# execute("What is the occupation of Darius Marder?")
#
with open('./questions_test.txt', 'r', encoding='utf-8') as questions_file, open('./answers_test.txt', 'r',
                                                                              encoding='utf-8') as answers_file:
    con = True
    while con:
        question = questions_file.readline()
        if question != '':
            question = question.rstrip()
            expected_answer = answers_file.readline().rstrip()
            actual_answer = execute(question)
            try:
                assert expected_answer == actual_answer, f'Question "{question}"\nreceived answer: "{actual_answer}"\ninstead of the expected answer: "{expected_answer}"'
            except AssertionError as e:
                print(f"**************** {e}")
        else:
            con = False
