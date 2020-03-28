import html.parser as h
import re
from urllib.parse import urljoin


class NotHTMLException(Exception):
    pass


class Scraper:

    def extract_links(self, html: str, base_url: str) -> set:
        """
        Parses the HTML string for links, both absolute and relative, located
        in anchor tag and placed randomly in the list. Returns set with
        unique elements

        :param html: HTML page in the form of a string
        :param base_url: use as prefix to relative links identified
        """
        parser = LinkHTMLParser()
        parser.feed(html)

        if not parser.is_html_page:
            raise NotHTMLException()

        absolute_links = set(self.__match_unstructured_links__(html))
        anchor_matches = set(parser.extracted_links)
        relative_links = anchor_matches.difference(absolute_links)

        for relative_link in relative_links:
            absolute_links.add(urljoin(base_url, relative_link))

        return absolute_links

    # Fonction pure
    def __match_unstructured_links__(self, html: str) -> list:
        """
        Find links not located in anchor tags
        :param html: HTML page in the form of a string
        """
        regex = r"\b((http|https|ftp):\/\/)(w{3}\.)?((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|[^-.=\[\]][a-zA-Z0-9_.-]*[" \
                r"^-=\]\[]\.[a-zA-Z]{1,24})(:\d*)?((\/[^\s\"<>\']*)?(\/)?)* "
        pattern = re.compile(regex)
        link_list = [match.group(0) for match in pattern.finditer(html)]
        return link_list


class LinkHTMLParser(h.HTMLParser):
    def __init__(self):
        super().__init__()
        self.switch = {
            "a": self.__handle_anchor__,
            "html": self.__handle_html__
        }
        self.extracted_links = []
        self.is_html_page = False

    def handle_starttag(self, tag: str, attrs: list):
        """
        Method called by HTMLParser when a start tag is encountered
        :param tag:
        :param attrs:
        """
        try:
            link = self.switch[tag](attrs)
            if link is not None:
                self.extracted_links.append(link)
        except:
            print("tag {} not recognized".format(tag))

    # Fonction pure
    def __handle_anchor__(self, attrs) -> str:
        """
        Extracts link from anchor tag
        :param attrs:
        """
        for attr in attrs:
            if attr[0] != "href":
                continue
            else:
                return attr[1]

    def __handle_html__(self, attrs):
        self.is_html_page = True
