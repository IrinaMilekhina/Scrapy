import scrapy
from scrapy.http import HtmlResponse
from booksparser.items import BooksparserItem


class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/novie-knigi/']
    page_number = 2

    def parse(self, response: HtmlResponse):
        # https://book24.ru/novie-knigi/page-3/
        next_page = f'https://book24.ru/novie-knigi/page-{self.page_number}/'
        self.page_number += 1
        yield response.follow(next_page, callback=self.parse)

        books_links = response.xpath("//a[@class='product-card__image-link smartLink']/@href").extract()
        for link in books_links:
            yield response.follow(link, callback=self.books_parse)

    def books_parse(self, response: HtmlResponse):
        item_link = response.url
        item_name = response.xpath("//h1/text()").extract_first()
        item_authors = response.xpath("//a[@itemprop='author']/text()").extract()
        item_old_price = response.xpath("//div[@class='item-actions__price-old']/text()").extract_first()
        item_current_price = response.xpath("//div[@class='item-actions__price']/b/text()").extract_first()
        item_rating = response.xpath("//span[@itemprop='ratingValue']/text()").extract_first()

        item = BooksparserItem(link=item_link, name=item_name, authors=item_authors, old_price=item_old_price,
                               current_price=item_current_price, rating=item_rating)
        yield item
