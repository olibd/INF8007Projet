# La classe doit pouvoir parcourir les pages du site web, vérifier
# les liens externes sans les parcourir (envoyer la requête sans télécharger le contenue)
# et éviter de parcourir en double les pages.

# Avec des liens de départ, les checker un par un, télécharger le contenue
# html des liens qui ont aboutis

# Fonction qui check tout les liens d'une page sans télécharger le contenue
# library : http.client
# Je reçois : ["HTTP://google.com","bl.com"]
# Je retourne : [("google.com", 200), ...], objet http.response

import http.client


class Crawler(object):

    def __init__(self, links):
        self.links = links
        self.checked = bool

    def url_connection(self):
        pass

