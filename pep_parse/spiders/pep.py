import scrapy
from pep_parse.items import PepParseItem
from pep_parse.constant import ALLOWED_DOMAINS_PEP


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ALLOWED_DOMAINS_PEP
    start_urls = ['https://' + allowed_domains[0]]

    def parse(self, response):
        for author_link in response.css('a[href^="pep-"]'):
            yield response.follow(
                author_link, callback=self.parse_pep
            )

    def parse_pep(self, response): 
        title_text = response.css('section#pep-content h1.page-title::text').get()
        title_parts = title_text.split(' – ')

        data = { 
            'number': title_parts[0].replace('PEP ', ''), 
            'name': title_parts[1], 
            'status': response.css('section#pep-content abbr::text').get() 
        } 
        yield PepParseItem(data)
