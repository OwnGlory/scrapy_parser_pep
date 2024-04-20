import re
import scrapy
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        for author_link in response.css('a[href^="pep-"]'):
            yield response.follow(
                author_link, callback=self.parse_pep
            )

    def parse_pep(self, response):
        data = {
            'number': (
                re.search(
                    r'PEP (\d{1,4})',
                    response.css(
                        'section#pep-content h1.page-title::text'
                    ).get()
                ).group(1)),
            'name': (
                re.search(
                    r'PEP \d{1,4} – (.*)',
                    response.css(
                        'section#pep-content h1.page-title::text'
                    ).get()
                ).group(1)),
            'status': response.css(('section#pep-content abbr::text')).get()
        }
        yield PepParseItem(data)
