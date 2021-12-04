import os
import re
import sqlite3

## 正则匹配文件中的数据
findMessageID = re.compile(r'Message-ID: (.*?)\n',re.S)
findDate = re.compile(r'Date: (.*?)\n',re.S)
findFrom = re.compile(r'From: (.*?)\n',re.S)
findSubject = re.compile(r'Subject: (.*?)\n',re.S)
findContent_type = re.compile(r'Content-Type: (.*?)\n',re.S)
findXFrom = re.compile(r'X-From: (.*?)\n',re.S)


## 获取数据表的长度
def getDBLength(dbpath):
  conn = sqlite3.connect(dbpath)
  cursor = conn.cursor()
  cursor.execute("select * from IRData")
  results = cursor.fetchall()
  return len(results)

## 获取文件中的数据
def getDataList(id):
  Id = id
  for file in files: #遍历文件夹
    data = []
    position = path+'\\'+ file #构造绝对路径，"\\"，其中一个'\'为转义符
    print (position)           
    with open(position, "r",encoding='utf-8') as f:    #打开文件
      fileDetail = f.read()   #读取文件
      # print(fileDetail)
      data.append(Id)
      Id = Id + 1

      Message_id = re.findall(findMessageID,fileDetail)[0]
      # print(Message_id)
      data.append(Message_id)  

      Date = re.findall(findDate,fileDetail)[0]
      Date = Date.replace('"',"'")
      # print(Date)
      data.append(Date)

      From = re.findall(findFrom,fileDetail)[0]
      From = From.replace('"',"'")
      # print(From)
      data.append(From) 

      Subject = re.findall(findSubject,fileDetail)[0]
      Subject = Subject.replace('"',"'")
      # print(Subject)
      data.append(Subject)  

      ContentType = re.findall(findContent_type,fileDetail)[0]
      ContentType = ContentType.replace('"',"'")
      # print(ContentType)
      data.append(ContentType)  

      XFrom = re.findall(findXFrom,fileDetail)[0]
      XFrom = XFrom.replace('"',"'")
      # print(XFrom)
      data.append(XFrom)

      Content = re.split(r"\n\n",fileDetail)[-1]
      Content = Content.replace('"',"'")
      # print(Content)
      data.append(Content)

      print(data)

      datalist.append(data)
  return datalist

## 将数据保存到sqlite数据库中
def saveData(dbpath,datalist):
    # init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            sql = '''
              insert into IRData(
              id, Message_id, Date, FromPeople, Subject, ContentType, XFrom, Content)
              values ("%s","%s","%s","%s","%s","%s","%s","%s")'''%(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
        print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()
def init_db(dbpath):
    sql = '''
    create table IRData
    (
    id INTEGER primary key autoincrement,
    Message_id text ,
    Date text,
    FromPeople text,
    Subject text,
    ContentType text,
    XFrom text,
    Content text
    )
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


if __name__ == "__main__":

  ## 定义文件目录
  path = "D:\\Users\\31156\\Desktop\\information-retrieval\\IR\\hyatt-k\\projects\\tsunami" #文件夹目录
  files= os.listdir(path) #得到文件夹下的所有文件名称
  dbpath = "IRData.db"
  
  ## 获取数据表长度
  id = getDBLength(dbpath) + 1


  ## 获取数据
  datalist = []
  datalist = getDataList(id)

  ## 保存数据
  saveData(dbpath,datalist)


    

