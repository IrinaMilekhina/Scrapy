# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksparserItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    authors = scrapy.Field()
    current_price = scrapy.Field()
    old_price = scrapy.Field()
    price_with_discount = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
