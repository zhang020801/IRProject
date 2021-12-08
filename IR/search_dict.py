import sqlite3

import re
import sys
from textblob import TextBlob
from textblob import Word
from collections import defaultdict


file_url = []
file_subject = []
postings = defaultdict(dict)
class Search:
    def __init__(self, mydir=None):
      conn = sqlite3.connect('IRData.db')
      cu = conn.cursor()
      
      #获取数据，保存在datalist数据表
      cu.execute("select * from IRData")
      self.datalist = cu.fetchall()
      # print(self.datalist)
    def getURL(self):
      for item in self.datalist:
        file_url.append(item[-1])
      return file_url

    def getSubject(self):
      for temp in self.datalist:
        file_subject.append(temp[4])
      return file_subject

    def createIndex(self,file_url,file_subject):

      docu_set = {}
      for i in range(0,1502):
        docu_set[file_url[i]] = file_subject[i]
      # print(docu_set)
      
      all_words = []
      for i in docu_set.values():
          #    cut = jieba.cut(i)
          cut = i.split()
          all_words.extend(cut)
          # print(cut)
      
      set_all_words = set(all_words)
      print('分割后的单词词典：',set_all_words)
      # print(len(set_all_words))
          
      self.invert_index = dict()
      for b in set_all_words:
          temp = []
          for j in docu_set.keys():
      
              field = docu_set[j]
              # print(field)
      
              split_field = field.split()
      
              if b in split_field:
                # print(j)
                temp.append(j)
          self.invert_index[b] = temp
          # print(b,invert_index[b])
      # print('倒排索引表：',invert_index)
      return self.invert_index


    def merge2_and(self,term1,term2):
      answer = []  
      if (term1 not in self.invert_index) or (term2 not in self.invert_index):
          return answer      
      else:
          i = len(self.invert_index[term1])
          j = len(self.invert_index[term2])
          x=0
          y=0
          while x<i and y<j:
              if self.invert_index[term1][x]==self.invert_index[term2][y]:
                  answer.append(self.invert_index[term1][x])
                  x+=1
                  y+=1
              elif self.invert_index[term1][x] < self.invert_index[term2][y]:
                  x+=1
              else:
                  y+=1            
          return answer     

    def merge2_or(self,term1,term2):
      answer=[]
      if (term1 not in self.invert_index)and(term2 not in self.invert_index):
          answer = []      
      elif term2 not in self.invert_index:
          answer = self.invert_index[term1]
      elif term1 not in self.invert_index:
           answer = self.invert_index[term2]
      else:
          answer = self.invert_index[term1]
          for item in self.invert_index[term2]:
              if item not in answer:
                  answer.append(item)              
      return answer

    def merge2_not(self,term1,term2):
        answer=[]
        if term1 not in self.invert_index:
            return answer      
        elif term2 not in self.invert_index:
            answer = self.invert_index[term1]
            return answer

        else:
            answer = self.invert_index[term1]
            ANS = []
            for ter in answer:
                if ter not in self.invert_index[term2]:
                    ANS.append(ter)
            return ANS

    def merge3_and(self,term1,term2,term3):
        Answer = []
        if term3 not in self.invert_index:
            return Answer   
        else:
            Answer = self.merge2_and(term1,term2)
            if Answer==[]:
                return Answer
            ans = []
            i = len(Answer)
            j = len(self.invert_index[term3])
            x=0
            y=0
            while x<i and y<j:
                if Answer[x]==self.invert_index[term3][y]:
                    ans.append(Answer[x])
                    x+=1
                    y+=1
                elif Answer[x] < self.invert_index[term3][y]:
                    x+=1
                else:
                    y+=1

            return ans

    def merge3_or(self,term1,term2,term3):
        Answer = []
        Answer = self.merge2_or(term1,term2);
        if term3 not in self.invert_index:
            return Answer
        else:
            if Answer ==[]:
                Answer = self.invert_index[term3]
            else:
                for item in self.invert_index[term3]:
                    if item not in Answer:
                        Answer.append(item)
            return Answer

    def merge3_and_or(self,term1,term2,term3):
        Answer = []
        Answer = self.merge2_and(term1,term2)
        if term3 not in self.invert_index:
            return Answer
        else:
            if Answer==[]:
                Answer = self.invert_index[term3]
                return Answer
            else:
                for item in self.invert_index[term3]:
                    if item not in Answer:
                        Answer.append(item)
                return Answer

    def merge3_or_and(self,term1,term2,term3):
        Answer = []
        Answer = self.merge2_or(term1,term2)
        if (term3 not in self.invert_index) or (Answer==[]):
            return Answer
        else:
            ans = []
            i = len(Answer)
            j = len(self.invert_index[term3])
            x=0
            y=0
            while x<i and y<j:
                if Answer[x]==self.invert_index[term3][y]:
                    ans.append(Answer[x])
                    x+=1
                    y+=1
                elif Answer[x] < self.invert_index[term3][y]:
                    x+=1
                else:
                    y+=1       
            return ans       
    def do_rankSearch(self,terms):
      Answer = defaultdict(dict)
      for item in terms:
          if item in self.invert_index:
              for tweetid in self.invert_index[item]:
                  if tweetid in Answer:
                      Answer[tweetid]+=1
                  else:
                      Answer[tweetid] = 1
      Answer = sorted(Answer.items(),key = lambda asd:asd[1],reverse=True)
      return Answer

    def token(self,doc):
      
      terms=TextBlob(doc).words.singularize()
      # print(terms)
      result=[]
      for word in terms:
          expected_str = Word(word)
          expected_str = expected_str.lemmatize("v")     
          result.append(expected_str)
      return result 


    def do_search(self,sentence):
      terms = self.token(sentence)
      # print(terms)
      if terms == []:
        sys.exit()  
      #搜索的结果答案   
    
      if len(terms)==3:
          #A and B
          if terms[1]=="and":
              answer = self.merge2_and(terms[0],terms[2])   
              print(answer)
              return answer
          #A or B       
          elif terms[1]=="or":
              answer = self.merge2_or(terms[0],terms[2])  
              print(answer)
              return answer
          #A not B    
          elif terms[1]=="not":
              answer = self.merge2_not(terms[0],terms[2])
              print(answer)
              return answer
          #输入的三个词格式不对    
          else:
              print("input wrong!")

      elif len(terms)==5:
          #A and B and C
          if (terms[1]=="and") and (terms[3]=="and"):
              answer = self.merge3_and(terms[0],terms[2],terms[4])
              print(answer)
              return answer
          #A or B or C
          elif (terms[1]=="or") and (terms[3]=="or"):
              answer = self.merge3_or(terms[0],terms[2],terms[4])
              print(answer)
              return answer
          #(A and B) or C
          elif (terms[1]=="and") and (terms[3]=="or"):
              answer = self.merge3_and_or(terms[0],terms[2],terms[4])
              print(answer)
              return answer
          #(A or B) and C
          elif (terms[1]=="or") and (terms[3]=="and"):
              answer = self.merge3_or_and(terms[0],terms[2],terms[4])
              print(answer)
              return answer
          else:
              print("More format is not supported now!")
      #进行自然语言的排序查询，返回按相似度排序的最靠前的若干个结果
      else:
          leng = len(terms)
          answer = self.do_rankSearch(terms,self.invert_index)
          print ("[Rank_Score: Tweetid]")
          for (tweetid,score) in answer:
              print (str(score/leng)+": "+tweetid)
          




if __name__ == "__main__":
  id = Search()
  file_url = id.getURL()
  file_subject = id.getSubject()
  # print(file_subject)
  # print(file_url)

  invert_index = id.createIndex(file_url,file_subject)
  # result = 
  result = id.do_search("Presentation and Alaska")
  print(result)
  