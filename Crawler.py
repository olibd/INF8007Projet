# La classe doit pouvoir parcourir les pages du site web, vérifier
# les liens externes sans les parcourir (envoyer la requête sans télécharger le contenue)
# et éviter de parcourir en double les pages.

import requests


class Crawler:

    def __init__(self, urls=[], checked={}):
        """
        Initialisation du Crawler

        :param urls: liste des liens dont on veut vérifier la connexion
        :param checked: dictionnaire des liens dont on a déjà vérifier la connexion
        """
        self.links = urls
        self.checked = checked
        self.responses = []

    def get_status_code(self, item: int) -> tuple:
        """
        Retourne le couple lien parcouru et status_code [lien, status_code].
        Si le lien n'existe pas OU s'il n'y a pas d'accés à internet, status_code = 0.
        :param item: rang du lien à vérifier
        """
        try:
            response = requests.head(self.links[item])
            return self.links[item], response.status_code
        except requests.exceptions.ConnectionError:
            return self.links[item], 0

    def get_html(self, link: str) -> str:
        """
        Retourne le contenu html d'un lien donné

        :param link: Lien https dont on veut récupérer le code html
        """
        html = requests.get(link).text
        return html

    def crawl(self):
        """
        On parcours les liens et on check leur status_code (si cela n'a pas été fait).
        On créé un dictionnaire des liens parcourus, self.checked = {'lien1' : 0, 'lien2' : 1, ...}, pour éviter les doublons.
        """
        i = 0
        for link in self.links:
            if link in self.checked:
                continue
            else:
                self.checked[link] = i
                res = self.get_status_code(i)
                self.responses.append(res)
            i += 1

    def get_responses(self) -> list:
        """
        Retourne la liste des liens et de leur status : [(lien, status_code),...]
        """
        return self.responses

    def get_checked(self) -> dict:
        """
        Retourne dictionnaire des liens DEJA parcourus
        """
        return self.checked


# Test du Crawler

links = ["https://www.python.org/", "https://www.google.com/", "https://www.CeLienNeMarchePas.com/",
         "http://www.dianping.com/promo/208721#mod=4", "https://www.google.com/"]

crawler1 = Crawler(links)
crawler1.crawl()
print(crawler1.get_responses())

list_checked = crawler1.get_checked()
crawler2 = Crawler(links, list_checked)
print(crawler2.get_responses())

# print(crawler.get_html("https://www.python.org/"))
# print(crawler.get_checked())
