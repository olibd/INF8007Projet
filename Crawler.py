# La classe doit pouvoir parcourir les pages du site web, vérifier
# les liens externes sans les parcourir (envoyer la requête sans télécharger le contenue)
# et éviter de parcourir en double les pages.

import requests


class Crawler:

    def __init__(self, urls: list = [], checked: dict = {}):
        """
        Initialisation du Crawler

        :param urls: liste des liens dont on veut vérifier la connexion
        :param checked: dictionnaire des liens dont on a déjà vérifier la connexion
        :param base_url: use as prefix to relative links present in the list
        """
        self.links = urls
        self.checked = checked
        self.responses = []

    def get_status_code(self, link: str) -> tuple:
        """
        Retourne le couple lien parcouru et status_code [lien, status_code].
        Si le lien n'existe pas OU s'il n'y a pas d'accés à internet, status_code = 0.
        :param item: rang du lien à vérifier
        """
        try:
            response = requests.head(link)
            return response.status_code
        except requests.exceptions.ConnectionError:
            return link, 0
        except requests.exceptions.InvalidURL:
            return None
        except requests.exceptions.InvalidSchema:
            return None

    @staticmethod
    def get_html(link: str) -> str:
        """
        Retourne le contenu html d'un lien donné

        :param link: Lien https dont on veut récupérer le code html
        """
        html = requests.get(link).text
        return html

    def crawl(self):
        """
        On parcours les liens et on check leur status_code (si cela n'a pas été fait).
        On créé un dictionnaire des liens parcourus, self.checked = {'lien1' : 200, 'lien2' : 404, ...}, pour éviter de parcourir en double.
        """
        for link in self.links:
            if link in self.checked:
                print("already checked out {}, using cached response".format(link))
                self.responses.append((link, self.checked[link]))
            else:
                print("checking: {}".format(link))
                res = self.get_status_code(link)
                self.checked[link] = res

                if res != None:
                    self.responses.append((link, res))

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