import requests
import lxml.html
import datetime
import rdflib
import lxml.html.clean

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
            print("Contributor: %s" %contributor)
            insert_to_ontology(contributor, contributors_data[contributor])
    g.serialize('ontology.nt', format='nt')


def insert_to_ontology(entity, data):

    ont_entity = rdflib.URIRef(example_url + '/' + entity)
    for relation in data:
        ont_relation = relation.replace('\xa0', '_')
        ont_relation = rdflib.URIRef(example_url + '/' + ont_relation)
        for value in data[relation]:
            value = value.replace('\xa0', '_')
            value = value.replace(' ', '_')
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
    for t in doc.xpath("//table[contains(@class,'infobox')]//tr[position()>1]//*[contains(@class,'infobox-label')]"):
        label = ' '.join(t.itertext()).strip(' ')
        label = label.replace(' ', '_')
        parent = t.getparent()
        relations[label] = [a for a in parent.getchildren()[1].itertext() if a != '\n' and '[' not in a]
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


def get_contributors_info(data: dict):
    producers = data['Produced_by']
    directors = data['Directed_by']
    actors = data['Starring']
    res = dict()
    for people in set(producers + directors + actors):
        people = people.replace(' ', '_')
        info = get_info_from_infobox(wiki_url + '/wiki/' + people)
        if len(info) > 0:
            info['Born'] = format_date(info['Born'])
            res[people] = info
    return res


create()
