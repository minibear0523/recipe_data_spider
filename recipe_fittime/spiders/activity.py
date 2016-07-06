# -*- coding: utf-8 -*-
import scrapy
import json
from time import time
from datetime import datetime
from recipe_fittime.items import ActivityItem
from urllib import urlencode
from urlparse import urlparse, parse_qs


HOST = "https://api.rjft.net/social/sticker/%E5%90%83%E5%87%BA%E5%A5%BD%E8%BA%AB%E6%9D%90/hot/activity?"


class ActivitySpider(scrapy.Spider):
    name = "activity"
    allowed_domains = ["rjft.net"]

    def start_requests(self):
        data = {
            'limit': 30,
            'skip': 0,
            'timestamp': int(time())
        }
        url = HOST + urlencode(data)
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        params_dict = parse_qs(urlparse(response.url).query)
        limit = int(params_dict['limit'][0])
        skip = int(params_dict['skip'][0])

        result = json.loads(response.body)['result']
        for data in result:
            item = ActivityItem()
            item['activity_id'] = data['id']
            item['user_id'] = data['user_id']
            item['checkin_id'] = data['checkin_id']
            item['link_id'] = data['link_id']
            item['content'] = data['content']
            item['create_time'] = data['create_time']
            item['update_time'] = data['update_time']
            item['video_url'] = data['video_url']
            item['total_comment'] = data['total_comment']
            item['total_praise'] = data['total_praise']
            item['is_topic_selected'] = data['is_topic_selected']

            # Add Database Create And Update Time For Item
            item['db_create_time'] = datetime.now()
            yield item

        if len(result) != 0:
            data = {
                'limit': 30,
                'skip': limit+skip,
                'timestamp': int(time())
            }
            url = HOST + urlencode(data)
            yield scrapy.Request(url, callback=self.parse)
