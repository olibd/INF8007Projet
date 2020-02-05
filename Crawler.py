# La classe doit pouvoir parcourir les pages du site web, vérifier
# les liens externes sans les parcourir (envoyer la requête sans télécharger le contenue)
# et éviter de parcourir en double les pages.

# Avec des liens de départ, les checker un par un, télécharger le contenue
# html des liens qui ont aboutis

# Fonction qui check tout les liens d'une page sans télécharger le contenue
# library : http.client
# Je reçois : ["HTTP://google.com","bl.com"]
# Je retourne : [("google.com", 200), ...], objet http.response

import requests
import http

#html = requests.get(url)
#parsed = urlparse(url)

class Crawler(object):

    def __init__(self, links):
        self.links = links
        self.checked = {}
        self.responses = []

    def get_res(self, item):
        #response = http.client.HTTPSConnection(self.links[item])
        try:
            response = requests.get(self.links[item])
            return self.links[item], response.status_code
        except ConnectionError:
            return False

    def get_html(self, item):
        html = (self.links[item].get_res()).text
        return html

    def crawl(self):
        i = 0
        for link in self.links:
            if link in self.checked:
                continue
            else:
                self.checked[link] = i
                res = self.get_res(i)
                self.responses.append(res)
            i += 1


#links = ["www.python.org","www.google.com","www.CeLienNeMarchePas.com"]
links = ["https://www.python.org/","https://www.google.com/","https://www.CeLienNeMarchePas.com/"]
crawler = Crawler(links)
crawler.crawl()
print(crawler.responses)