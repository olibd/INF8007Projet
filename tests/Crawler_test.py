# Test du Crawler
from INF8007Projet.Crawler import Crawler

links = ["https://www.python.org/", "https://www.google.com/", "https://www.CeLienNeMarchePas.com/",
         "http://www.dianping.com/promo/208721#mod=4", "https://www.google.com/"]

crawler1 = Crawler(links)
crawler1.crawl()
print(crawler1.get_responses())

list_checked = crawler1.get_checked()
crawler2 = Crawler(links, list_checked)
print(crawler2.get_responses())

#print(crawler.get_html("https://www.python.org/"))
#print(crawler.get_checked())