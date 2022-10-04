import scrapy
from scrapy.selector import Selector
import json 

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://quod.lib.umich.edu/e/ecco?key=author;page=browse',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = f'quotes-{page}.html'
        filename = f'books.txt'
        body = response.body
        # print(response.body)
        
        quotes = response.xpath('//tr[@class="browselistitem"]').get()
        
        yield {'quotes': quotes}
 
        with open(filename, 'wb') as f:
            f.write(response.xpath('//tr[@class="browselistitem"]').extract())
        self.log(f'Saved file {filename}')