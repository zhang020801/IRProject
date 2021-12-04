import sqlite3
from sqlite3.dbapi2 import Date
from typing import ContextManager
from whoosh.fields import Schema, ID, TEXT, NUMERIC
from whoosh.index import create_in, open_dir

class IndexBuilder:
  def __init__(self):
    ## 获取数据库中的数据
    conn = sqlite3.connect('IRData.db')
    cu = conn.cursor()
      
    #获取数据，保存在datalist数据表
    cu.execute("select * from IRData")
    self.datalist = cu.fetchall()
    print(self.datalist)
  def build_index(self):
    # 创建索引模板
    schema = Schema(
      id = ID(stored = True),
      Subject = TEXT(stored = True),
      Message_id = ID(stored = True),
      Date = TEXT(stored = True),
      FromPeople = TEXT(stored = True),
      Content = TEXT(stored = True),  # 文章内容太长了，不存
    )
    # 索引文件相关
    import os.path
    if not os.path.exists('index'):
        os.mkdir('index')
        ix = create_in('index', schema)
        print('未发现索引文件,已构建.')
    else:
        ix = open_dir('index')
        print('发现索引文件并载入....')
    
    # 索引构建
    writer = ix.writer()
    for data in self.datalist:
      writer.add_document(
          id = str(data[0]),
          Subject = data[4],
          Message_id = data[1],
          Date = data[2],
          FromPeople = data[3],
          Content = data[7],
      )
      # the end
      writer.commit()     # 每次构建提交一次
      writer = ix.writer()    # 然后重新打开

    



if __name__ == "__main__":
  id = IndexBuilder()
  id.build_index()