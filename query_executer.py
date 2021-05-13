import re
import sys

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
    pass


def execute(query):
    matching_pattern = get_matching_pattern(query)
    if not matching_pattern:
        print('please enter a valid query.')
        sys.exit(0)
    return None
