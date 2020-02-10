import functools
import html.parser as h
import operator
import re

class Scraper:
    def __init__(self):
        pass

    def extract_links(self, html: str) -> set:
        parser = LinkHTMLParser()
        parser.feed(html)

        matches = self.__match_unstructured_links__(html)
        unique_set = set(parser.extracted_links)

        for match in matches:
            unique_set.add(self.__reduce_to_string__(match))

        return unique_set

    def __match_unstructured_links__(self, html: str) -> list:
        pattern = re.compile("(((http|https|ftp):\/\/)|)(w{3}\.|)(\w*[\.|-]\w*)(:\d*|)(\/|\S*)*")
        return pattern.findall(html)

    def __reduce_to_string__(self, tuple):
        functools.reduce(operator.add, (tuple))

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
