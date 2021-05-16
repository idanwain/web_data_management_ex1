import requests
import lxml.html

base_url = "https://en.wikipedia.org"

def create():
    pass


def get_movies_url(url="https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films"):
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)
    urls = []
    for t in doc.xpath("//table//tr//td[2]//*[text()>2009]/../..//td[1]//@href"):
        curr_url = base_url + str(t)
        urls.append(curr_url)
    return urls


def get_info_from_infobox(movie_url):
    res = requests.get(movie_url)
    doc = lxml.html.fromstring(res.content)
    relations = dict()
    for t in doc.xpath("//table[contains(@class,'infobox')]//tr[position()>1]//*[contains(@class,'infobox-label')]"):
        label = ' '.join(t.itertext())
        parent = t.getparent()
        relations[label] = [a for a in parent.getchildren()[1].itertext() if a != '\n' and '[' not in a]
    return relations


def main():
    movies_urls = get_movies_url()
    for url in movies_urls:
        print(get_info_from_infobox(url))


if __name__ == "__main__":
    main()
