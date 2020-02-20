import functools
import html.parser as h
import operator
import re


class Scraper:

    def extract_links(self, html: str) -> set:
        parser = LinkHTMLParser()
        parser.feed(html)

        matches = self.__match_unstructured_links__(html)
        unique_set = set(parser.extracted_links)

        for match in matches:
            unique_set.add(match)

        return unique_set

    def __match_unstructured_links__(self, html: str) -> list:
        regex = r"\b((http|https|ftp):\/\/)?(w{3}\.)?((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|[^-.][a-zA-Z0-9_.-]*[^-]\.[a-zA-Z]{1,24})(:\d*)?((\/\S*)?(\/)?)*"
        pattern = re.compile(regex)
        link_list = [match.group(0) for match in pattern.finditer(html)]
        return link_list


class LinkHTMLParser(h.HTMLParser):
    def __init__(self):
        super().__init__()
        self.switch = {
            "a": self.__handle_anchor__
        }
        self.extracted_links = []

    def handle_starttag(self, tag: str, attrs: list):
        try:
            self.extracted_links.append(self.switch[tag](attrs))
        except:
            print("tag {} not recognized".format(tag))

    def __handle_anchor__(self, attrs) -> str:
        for attr in attrs:
            if attr[0] != "href":
                continue
            else:
                return attr[1]
