from re import search
from flask import Flask, request, render_template
from search_index import Query
from search_dict import Search

app = Flask(__name__)

class Email:
    def __init__(self):
        pass

@app.route('/', methods=['GET','POST'])
def index():
  return render_template('index.html')

@app.route('/index', methods=['GET','POST'])
def searcher():
  result = []
  data = request.values.to_dict()
  keyword = data.get("keywords")
  print(keyword)
  
  q = Query()
  datalist = q.standard_search(keyword)


  data_bool = request.values.to_dict()
  bool_sentence = data_bool.get("boolsearch")
  if(bool_sentence):
    p = Search()
    file_url = p.getURL()
    file_subject = p.getSubject()
    p.createIndex(file_url,file_subject)
    result = p.do_search(bool_sentence) 
  return render_template('index.html',datalist = datalist,result = result)

if __name__ == '__main__':
    app.run()