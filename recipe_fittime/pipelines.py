# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from recipe_fittime.items import DietItem, ActivityItem
from scrapy.exceptions import DropItem
from datetime import datetime
import psycopg2
import logging

InsertDietItemSql = """INSERT INTO fittime_recipe (article_id, user_id, title, description, category, comment_count,
praise_count, view_count, collection_count, create_time, update_time, content, content_url, contains_video, rank,
image_url, kind, db_create_time)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

InsertActivityItemSql = """INSERT INTO fittime_activity (activity_id, user_id, checkin_id, link_id, content, create_time,
update_time, video_url, total_comment, total_praise, is_topic_selected, db_create_time)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

DATE_FORMAT = '%Y-%m-%d'


def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime(DATE_FORMAT)


def format_item_sql(item):
    if isinstance(item, DietItem):
        return item['article_id'], item['user_id'], item['title'], item['description'], item['category'], \
               item['comment_count'], item['praise_count'], item['view_count'], item['collection_count'], \
               format_timestamp(item['create_time']), format_timestamp(item['update_time']), item['content'], \
               item['content_url'], bool(item['contains_video']), item['rank'], item['image_url'], item['kind'], \
               item['db_create_time']

    elif isinstance(item, ActivityItem):
        return item['activity_id'], item['user_id'], item['checkin_id'], item['link_id'], item['content'], \
               format_timestamp(item['create_time']), format_timestamp(item['update_time']), item['video_url'],\
               item['total_comment'], item['total_praise'], bool(item['is_topic_selected']), item['db_create_time']
    else:
        return None

logger = logging.getLogger()


class DBPipeline(object):
    def __init__(self):
        self.connection = psycopg2.connect('dbname=fit_data user=MiniBear')
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        if isinstance(item, DietItem):
            if item['kind'] in ['recipe', 'plan', 'supplement']:
                try:
                    self.cursor.execute(InsertDietItemSql, format_item_sql(item))
                except psycopg2.DatabaseError as e:
                    logger.error('Database Error: %s', e)
                    self.connection.rollback()

                self.connection.commit()
                return item
            else:
                logger.error('Incorrect item kind')
                raise DropItem('Item: %s kind is incorrect' % item)
        elif isinstance(item, ActivityItem):
            try:
                self.cursor.execute(InsertActivityItemSql, format_item_sql(item))
            except psycopg2.DatabaseError as e:
                logger.error('Database Error: %s', e)
                self.connection.rollback()

            self.connection.commit()
            return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.recipe = set()
        self.plan = set()
        self.supplement = set()
        self.activity = set()

    def process_item(self, item, spider):
        if isinstance(item, DietItem):
            if item['kind'] == 'recipe':
                if item['article_id'] in self.recipe:
                    raise DropItem('Duplicate item found: %s' % item)
                else:
                    self.recipe.add(item['article_id'])
                    return item
            elif item['kind'] == 'plan':
                if item['article_id'] in self.plan:
                    raise DropItem('Duplicate item found: %s' % item)
                else:
                    self.plan.add(item['article_id'])
                    return item
            elif item['kind'] == 'supplement':
                if item['article_id'] in self.supplement:
                    raise DropItem('Duplicate item found: %s' % item)
                else:
                    self.supplement.add(item['article_id'])
                    return item
            else:
                raise DropItem('Item: %s kind is incorrect' % item)
        elif isinstance(item, ActivityItem):
            if item['activity_id'] in self.activity:
                raise DropItem('Duplicate item found: %s' % item)
            else:
                self.activity.add(item['activity_id'])
                return item
        else:
            raise DropItem('Item: %s class is incorrect' % item)
