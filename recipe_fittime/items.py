# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class DietItem(Item):
    article_id = Field()
    user_id = Field()
    title = Field()
    description = Field()
    category = Field()
    comment_count = Field()
    praise_count = Field()
    view_count = Field()
    collection_count = Field()
    create_time = Field()
    update_time = Field()
    content = Field()
    content_url = Field()
    contains_video = Field()
    rank = Field()
    image_url = Field()
    kind = Field() # Recipe, Plan, Supplement
    db_create_time = Field()


class ActivityItem(Item):
    activity_id = Field()
    user_id = Field()
    checkin_id = Field()
    link_id = Field()
    content = Field()
    create_time = Field()
    update_time = Field()
    video_url = Field()
    total_comment = Field()
    total_praise = Field()
    is_topic_selected = Field()
    db_create_time = Field()
