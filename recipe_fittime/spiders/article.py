# -*- coding: utf-8 -*-
import scrapy
import json
from recipe_fittime.items import DietItem
from urllib import unquote, urlencode
from urlparse import urlparse, parse_qs
from time import time
from datetime import datetime


HOST = 'https://api.rjft.net/api/v2/articles?v2&category=diet&'
ARTICLE_LINK = 'https://api.rjft.net/api/v2/articles/%s'

class ArticleSpider(scrapy.Spider):
    name = "article"
    allowed_domains = ["rjft.net"]

    def start_requests(self):
        urls = [
            'https://api.rjft.net/api/v2/articles?v2&category=diet&limit=60&offset=0&tags%5B%5D=%E5%81%A5%E5%BA%B7%E8%8F%9C%E8%B0%B1&',
            'https://api.rjft.net/api/v2/articles?v2&category=diet&limit=60&offset=0&tags%5B%5D=%E9%A5%AE%E9%A3%9F%E6%96%B9%E6%A1%88&',
            'https://api.rjft.net/api/v2/articles?v2&category=diet&limit=60&offset=0&tags%5B%5D=%E8%A1%A5%E5%89%82%E9%80%89%E6%8B%A9&',
        ]
        for url in urls:
            url = url + 'timestamp=' + str(int(time()))
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # parse url query into dict
        params_dict = parse_qs(urlparse(response.url).query)
        limit = int(params_dict['limit'][0])
        offset = int(params_dict['offset'][0])
        tag = unquote(params_dict['tags[]'][0])

        # parse data list into json format with response's body
        data_list = json.loads(response.body)
        for data in data_list:
            item = DietItem()
            # Parse item kind with ```tags[]```
            if tag == '健康菜谱':
                item['kind'] = 'recipe'
            elif tag == '饮食方案':
                item['kind'] = 'plan'
            elif tag == '补剂选择':
                item['kind'] = 'supplement'

            # Parse other item
            item['article_id'] = data['id']
            item['user_id'] = data['user_id']
            item['title'] = data['title']
            item['description'] = data['description']
            item['category'] = data['category']
            item['comment_count'] = data['comment_count']
            item['praise_count'] = data['praise_count']
            item['view_count'] = data['view_count']
            item['collection_count'] = data['collection_count']
            item['create_time'] = data['create_time']
            item['update_time'] = data['update_time']
            item['content_url'] = data['content_url']
            item['contains_video'] = data['is_contains_video']
            item['rank'] = data['rank']
            item['image_url'] = data['image_url']
            item['content'] = data['content']

            # Add Database Create Time For Item
            item['db_create_time'] = datetime.now()

            # Parse article detail
            url = ARTICLE_LINK % item['article_id']
            detail_request = scrapy.Request(url, callback=self.parse_article_detail)
            detail_request.meta['item'] = item
            yield detail_request

        if len(data_list) > 0:
            params = {
                'limit': limit,
                'offset': offset + limit,
                'tags[]': tag,
                'timestamp': int(time())
            }
            url = HOST + urlencode(params)
            yield scrapy.Request(url, callback=self.parse)

    def parse_article_detail(self, response):
        item = response.meta['item']
        data = json.loads(response.body)
        item['content'] = data['content_html']
        yield item
