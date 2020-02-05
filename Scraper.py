import html.parser as h


class Scraper:
    def __init__(self):
        pass

    def extract_links(self, html: str):
        parser = LinkHTMLParser()
        parser.feed(html)

class LinkHTMLParser(h.HTMLParser):
    def __init__(self):
        super().__init__()
        self.switch = {
            "a": self.__handle_anchor__
        }
        self.extracted_links = []

    def handle_starttag(self, tag, attrs) -> str:
        try:
            self.extracted_links.append(self.switch[tag])
        except:
            print("tag {} not recognized".format(tag))

    def __handle_anchor__(self, attrs):
        for attr in attrs:
            if (attr[0] != "href"):
                continue
            else:
                return attr[1]
