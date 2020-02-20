import html.parser as h
import re


class Scraper:

    def extract_links(self, html: str) -> set:
        """
        Parses the HTML string for links, both absolute and relative, located
        in anchor tag and placed randomly in the list. Returns set with
        unique elements

        :param html: HTML page in the form of a string
        """
        parser = LinkHTMLParser()
        parser.feed(html)

        matches = self.__match_unstructured_links__(html)
        unique_set = set(parser.extracted_links)

        for match in matches:
            unique_set.add(match)

        return unique_set

    def __match_unstructured_links__(self, html: str) -> list:
        """
        Find links not located in anchor tags
        :param html: HTML page in the form of a string
        """
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
        """
        Method called by HTMLParser when a start tag is encountered
        :param tag:
        :param attrs:
        """
        try:
            self.extracted_links.append(self.switch[tag](attrs))
        except:
            print("tag {} not recognized".format(tag))

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
