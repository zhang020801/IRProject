from re import search
from flask import Flask, request, render_template
from search_index import Query

app = Flask(__name__)

class Email:
    def __init__(self):
        pass

@app.route('/', methods=['GET','POST'])
def index():
  return render_template('index.html')

@app.route('/index', methods=['GET','POST'])
def searcher():
  data = request.values.to_dict()
  keyword = data.get("keywords")
  print(keyword)
  
  q = Query()
  datalist = q.standard_search(keyword)

  le = len(datalist)
  return render_template('index.html',datalist = datalist)

if __name__ == '__main__':
    app.run()