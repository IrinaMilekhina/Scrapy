import scrapy
from scrapy.http import HtmlResponse
from booksparser.items import BooksparserItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/novelty/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@title='Следующая']/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)

        books_links = response.xpath("//a[@class='cover']/@href").extract()
        for link in books_links:
            yield response.follow(link, callback=self.books_parse)

    def books_parse(self, response: HtmlResponse):
        item_link = response.url
        item_name = response.xpath("//h1/text()").extract_first()
        item_authors = response.xpath("//a[@data-event-label='author']/text()").extract()
        item_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        item_price_with_discount = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        item_rating = response.xpath("//div[@id='rate']/text()").extract_first()
        item = BooksparserItem(link=item_link, name=item_name, authors=item_authors, price=item_price,
                               price_with_discount=item_price_with_discount, rating=item_rating)
        yield item
