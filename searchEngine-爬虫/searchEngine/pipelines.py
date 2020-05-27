# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter
from searchEngine.models.es_types import FoodmateType
from elasticsearch_dsl.connections import connections

es = connections.create_connection(FoodmateType._doc_type.using)



class SearchenginePipeline(object):
    def __init__(self):
        self.fp = open("fdjc.json","wb")
        self.exporter = JsonLinesItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')


    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
		
    def close_spider(self,spider):
        self.fp.close()

def gen_suggests(index,info_tuple):
    #根据字符串生成搜索建议数据
    #定义为set后面需要去重
    used_words = set()
    suggests = []
    for text,weight in info_tuple:
        if text:
            #调用es的analyze接口分析字符串
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter': ["lowercase"]}, body=text)
            #列表生成式
            analyzed_words = set(r["token"] for r in words["tokens"] if len(r["token"]) > 1)
            new_words = analyzed_words - used_words
        else:
            new_words = set()
        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})
    return suggests

class ElasticsearchPipeline(object):
    # 将数据写入打到es中
    def process_item(self, item, spider):
        # 将 item 转换 为es的数据
        article = FoodmateType()
        article.title = item['title']
        article.source_detail = item['source_detail']
        article.source_url = item['source_url']
        article.introduce = item['introduce']
        article.content = item['content']
        article.suggest = gen_suggests(FoodmateType._doc_type.index,((article.title,10),(article.introduce,7)))
        article.save()
        return item
