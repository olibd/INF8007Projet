# La classe doit pouvoir parcourir les pages du site web, vérifier
# les liens externes sans les parcourir (envoyer la requête sans télécharger le contenue)
# et éviter de parcourir en double les pages.

# Avec des liens de départ, les checker un par un, télécharger le contenue
# html des liens qui ont aboutis
# Fonction qui check tout les liens d'une page sans télécharger le contenue
# library : requests
# Je reçois : ["HTTP://google.com","bl.com"]
# Je retourne : [("google.com", 200), ...]

import requests

checked_url = {}  # Définir cette liste comme une variable globale

class Crawler:

    def __init__(self, urls, checked):
        self.links = urls
        self.checked = checked
        self.responses = []

    def get_res(self, item):
        try:
            response = requests.head(self.links[item])
            return self.links[item], response.status_code
        except requests.exceptions.ConnectionError:
            return self.links[item], 0

    def get_html(self, link):
        html = requests.get(link).text
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
links = ["https://www.python.org/", "https://www.google.com/", "https://www.CeLienNeMarchePas.com/",
         "http://www.dianping.com/promo/208721#mod=4", "https://www.google.com/"]
crawler = Crawler(links, checked_url)
crawler.crawl()
print(crawler.responses)
print(crawler.responses)
# print(crawler.get_html("https://www.python.org/"))