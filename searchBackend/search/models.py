from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion, Keyword, Text, Integer

from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalysis

from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])  # connection可以连接多台服务器


class CustomAnalyzer(_CustomAnalysis):
    def get_analysis_definition(self):
        return {}

ik_analyser = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class FoodmateType(DocType):
    #suggest = Completion(analyzer="ik_max_word")  # 不能直接使用这个，由于源码问题，必须使用CustomAnalyzer
    suggest = Completion(analyzer=ik_analyser)
    title = Text(analyzer="ik_max_word")
    source_detail = Keyword()
    source_url = Keyword()
    introduce = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word")

    class Meta:
        index = "foodmate"
        doc_type = "foodsafe"


if __name__ == "__main__":
    FoodmateType.init()  # 根据类，直接生成mapping，
