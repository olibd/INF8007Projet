import unittest

from INF8007Projet.Scraper import Scraper


class ScraperTest(unittest.TestCase):

    def test_href_link_extraction(self):
        sample_html = open("./url_test_sample.html", "r").read()
        scraper = Scraper()
        links = scraper.extract_links(sample_html, "http://baseurl.com")
        self.assertTrue("http://absolute.com" in links)
        self.assertTrue("http://baseurl.com/relative.html" in links)
        self.assertTrue("http://foo.com" in links)

    def test_unique_link(self):
        sample_html = open("./url_test_sample.html", "r").read()
        scraper = Scraper()
        links = scraper.extract_links(sample_html)
        foolinks = list(filter(lambda link: link == "http://foo.com", links))
        self.assertEqual(len(foolinks), 1)

    def test_valid_regex(self):
        sample_urls = open("./valid_urls.txt", "r").read()
        scraper = Scraper()
        links = scraper.extract_links(sample_urls)
        self.assertEqual(len(links), 20)

    def test_invalid_regex(self):
        sample_urls = open("./invalid_urls.txt", "r").read()
        scraper = Scraper()
        links = scraper.extract_links(sample_urls)
        self.assertEqual(len(links), 0)


if __name__ == '__main__':
    unittest.main()
