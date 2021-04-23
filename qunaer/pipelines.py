# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import os
import uuid
import pymongo
from scrapy.selector import Selector
from neo4j import GraphDatabase
import numpy as np

logfile_name = uuid.uuid1()
if not os.path.exists('logs/'):
    os.mkdir('logs/')
logging.basicConfig(filename=f'logs/{logfile_name}.log', filemode='a+',
                    format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

class QunaerPipeline:
    # 建立数据库
    db = pymongo.MongoClient("mongodb://127.0.0.1:27017/")["db_travel"]
    db_qunaer = db['db_qunaer']
    db_triples = db['db_qunaerTriples']
    driver = GraphDatabase.driver(
        "bolt://localhost:7687", auth=("neo4j", "123"),encrypted=False)

    def add_node(self, tx, name1, relation, name2):
        tx.run("MERGE (a:Node {name: $name1}) "
               "MERGE (b:Node {name: $name2}) "
               "MERGE (a)-[:"+relation+"]-> (b)",
               name1=name1, name2=name2)

    def process_item(self, item, spider):
        #填入数据库
        self.db_qunaer.insert_one(
            {
                'title': item['title'] ,
                'level': item['level'],
                'area': item['area'],
                'address': item['address'],
                'province' :item['province'],
                'string': item['string'],
                'intro': item['intro'],
                'price': item['price'],
                'hot_num': item['hot_num']
            })

        # 处理三元组
        entity = item['title']
        attrs = ['景区名字','景区等级','地区','地址','省份','热度','简介','价格','月销']
        values = [item['title'],item['level'],item['area'],item['address'],item['province'],item['string'],item['intro'],item['price'],item['hot_num']]
        if len(attrs) != len(values):
            return
        # indexs = list(np.arange(1,len(attrs),1))
        with self.driver.session() as session:
            try:
                for attr, value in zip(attrs, values,):
                    # index = int(index)
                    entity = str(entity)
                    attr = str(attr)
                    value = str(value)
                    try:
                        logging.warning(entity + '_' + attr + '_' + value)
                        self.db_triples.insert_one({
                            "_id": entity + '_' + attr + '_' + value,
                            "entity": entity,
                            "attr": attr,
                            "value": value, }
                        )
                    except pymongo.errors.DuplicateKeyError:
                        pass
                    session.write_transaction(
                        self.add_node, entity, attr, value)
            except Exception:
                logging.error('\n---'.join(attrs) +
                              '\n_________________' + '\n---'.join(values))
        print(item)
        return item
