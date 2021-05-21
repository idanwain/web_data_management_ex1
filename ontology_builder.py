import requests
import lxml.html
import datetime
import rdflib
import rdflib.term
import lxml.html.clean
import json

wiki_url = "https://en.wikipedia.org"
example_url = "http://example.org"
suffix = "?redirect=no"
cleaner = lxml.html.clean.Cleaner(style=True)
g = rdflib.Graph()


# TODO: Handle lower-case upper-case problem
def create():
    ### add info of movie and info of contributers to ontology ###
    print("Start to create nt:")
    movies_urls = get_movies_urls()
    for movie in movies_urls:
        movie_name = get_movie_name(movie)
        print("Movie: %s" % movie_name)
        movie_data = get_info_from_infobox(movie)
        contributors_data = get_contributors_info(movie_data)
        insert_to_ontology(movie_name, movie_data)
        for contributor in contributors_data:
            print("Contributor: %s" % contributor)
            insert_to_ontology(contributor, contributors_data[contributor])
    g.serialize('ontology.nt', format='nt')


def insert_to_ontology(entity, data):
    entity = entity.strip()
    entity = entity.replace('"', "%" + format(hex(ord('"'))))
    entity = entity.replace('{', "%" + format(hex(ord('{'))))
    entity = entity.replace('}', "%" + format(hex(ord('}'))))
    entity = entity.replace('\\', "%" + format(hex(ord('\\'))))
    ont_entity = rdflib.URIRef(example_url + '/' + entity)
    for relation in data:
        relation = relation.strip()
        ont_relation = relation.replace('\xa0', '_')
        ont_relation = ont_relation.replace('"', "%" + format(hex(ord('"'))))
        ont_relation = ont_relation.replace('{', "%" + format(hex(ord('{'))))
        ont_relation = ont_relation.replace('}', "%" + format(hex(ord('}'))))
        ont_relation = ont_relation.replace('\\', "%" + format(hex(ord('\\'))))
        ont_relation = rdflib.URIRef(example_url + '/' + ont_relation)
        for value in data[relation]:
            value = value.strip()
            value = value.replace('\xa0', '_')
            value = value.replace(' ', '_')
            value = value.replace('"', "%" + format(hex(ord('"'))))
            value = value.replace('{', "%" + format(hex(ord('{'))))
            value = value.replace('}', "%" + format(hex(ord('}'))))
            value = value.replace('\\', "%" + format(hex(ord('\\'))))
            ont_value = rdflib.URIRef(example_url + '/' + value)
            g.add((ont_entity, ont_relation, ont_value))


def get_movie_name(movie_url):
    return movie_url.split('/')[-1]


def get_movies_urls(url="https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films"):
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)
    urls = []
    for t in doc.xpath("//table//tr//td[2]//*[text()>2009]/../..//td[1]//@href"):
        curr_url = wiki_url + str(t)
        urls.append(curr_url)
    return urls


def get_info_from_infobox(movie_url):
    res = requests.get(movie_url + suffix)
    doc = lxml.html.fromstring(res.content)
    relations = dict()
    for t in doc.xpath(
            "//table[contains(@class,'infobox')]//tr[position()>1]//*[contains(@class,'infobox-label')]"):  # Need to repair this, check https://en.wikipedia.org/wiki/Michael_Potts_(actor)
        label = ' '.join(t.itertext()).strip(' ')
        label = label.replace(' ', '_')
        parent = t.getparent()
        data = parent.getchildren()[1]
        relations[label] = [a for a in data.itertext() if a != '\n' and '[' not in a]
        for i, text in enumerate(relations[label]):
            el = get_element_by_text(doc, text, label)
            for e in el:
                if len(e.xpath("./@href")) > 0:
                    r = e.xpath("./@href")
                    relations[label][i] = truncate_prefix(r[0])
        if label == 'Release_date':
            relations['Release_date'] = format_date(relations['Release_date'])
    return relations


def format_date(release_date):
    dates = []
    for date in release_date:
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            dates.append(date)
        except ValueError:
            pass
    return dates


def get_element_by_text(context, text, label):
    label = label.replace('_', ' ')
    text = text.replace('"', "%" + format(hex(ord('"'))))
    text = text.replace('{', "%" + format(hex(ord('{'))))
    text = text.replace('}', "%" + format(hex(ord('}'))))
    s = f'//table[contains(@class,"infobox")]//tr[position()>1 and .//*[text()="{label}"]]//*[text()="{text}"]'
    return context.xpath(s)


def truncate_prefix(text, prefix='/wiki/'):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def get_contributors_info(data: dict):
    producers, directors, actors = [], [], []
    if 'Produced_by' in data.keys():
        producers = data['Produced_by']
    if 'Directed_by' in data.keys():
        directors = data['Directed_by']
    if 'Starring' in data.keys():
        actors = data['Starring']
    res = dict()
    for people in set(producers + directors + actors):
        people = people.replace(' ', '_')
        info = get_info_from_infobox(wiki_url + '/wiki/' + people)
        if len(info) > 0:
            try:
                info['Born'] = format_date(info['Born'])
                res[people] = info
            except KeyError:
                print(people + " has no 'born' field, skipping.")
    return res


create()
