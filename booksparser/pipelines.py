# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from pymongo import MongoClient


class BooksparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.books_db

    def process_item(self, item, spider):
        if spider.name == 'book24ru':
            print()
            if item.get('old_price'):
                item['old_price'] = re.sub(r"[^0-9]", "", item.get('old_price'))
                item['price_with_discount'] = int(item.get('current_price'))
                item['price'] = int(item.get('old_price'))
            else:
                item['price_with_discount'] = None
                item['price'] = int(item.get('current_price'))
            del item['old_price']
            del item['current_price']
        else:
            item['price_with_discount'] = int(item.get('price_with_discount'))
            item['price'] = int(item.get('price'))
        item['rating'] = float(item.get('rating').replace(',', '.'))
        clear_name = item.get('name').strip()
        item['name'] = clear_name
        collection = self.mongobase[spider.name]
        collection.update_one({'link': item.get('link')}, {'$set': item}, upsert=True)
        print(f'В коллекции {spider.name} документов: {collection.count_documents({})}')
        return item
