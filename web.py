import flask 
import csv
import flask_cors
from timeit import default_timer as timer

words=[]
history=[]
with open(r"unigram_freq.csv")as file:
        print("save")
        word=csv.reader(file)
        i=0
        for lines in word:
           words.append(lines[0])

with open(r"AnimeQuotes.csv", encoding="utf-8")as file:
        print("save")
        word=csv.reader(file)
        i=0
        for lines in word:
           history.append(lines[0])

web=flask.Flask(__name__)
flask_cors.CORS(web,methods=["POST"])

@web.route("/autocomplete",methods=['POST'])
def connect():
   data=flask.request.get_json()
   new=data.get('text', '')
   completed_text=autocomplete(new)

   return flask.jsonify({"complete_DP":completed_text[0],"time_DP":completed_text[1],"complete_BF":completed_text[2],"time_BF":completed_text[3]})

def connect():
   data=flask.request.get_json()
   new=data['text']

   
   table=autocomplete(new)
   tes=new.split()
   cek=False
   s="..."
   for i in tes:
       if search_pattern(s,i)==1:
           cek=True
           break
       
   if cek==False:
       history.append(new)

   return flask.jsonify({"nice":table})
@web.route("/autocorrect", methods=['POST'])
def connect_autocorrect():
    print("aurcojsaoifjae")
    data = flask.request.get_json()
    new = data.get('text', '')
    corrected_text = autocorect(new)
    send=flask.jsonify({"correct_DP": corrected_text[0],"time_DP":corrected_text[1],"correct_BF":corrected_text[2],"time_BF":corrected_text[3]})
    return send

def autocorect(sentences):
   
    text=sentences.split()
    textTable=list(map(failure,text))
    start_time=timer()
   # FalseWord=[]
    newSentence=''
    for index,i in enumerate(text):
        cek=False
        for index2,j in enumerate(words):
            
            if  KMP(i.lower(),j.lower(),textTable[index]):
                cek=True
                newSentence=newSentence+" "+i
                break
        if not cek:
          
           # FalseWord.append(i)
           min=words[0]
           n=levenshteinFullMatrix(min,i)
           for j in range(1,len(words)):
               m=levenshteinFullMatrix(words[j],i)
               if n>m:
                   n=m
                   min=words[j]
    
           newSentence=newSentence+' <div class="correct">'+min+'</div>'               
    end_time=timer()
    print(newSentence)
    waktu_DP=end_time-start_time
    print("waktu_DP ",waktu_DP)
    newSentence2=''
    
    start_time=timer() 

    for index,i in enumerate(text):
        cek=False
        for j in words:
            
            if  brute_force(j,i.lower()):
                cek=True
                newSentence2=newSentence2+" "+i
                break
        if not cek:
          
           # FalseWord.append(i)
           min=words[0]
           n=levenshteinFullMatrix(min,i)
           for j in range(1,len(words)):
               m=levenshteinFullMatrix(words[j],i)
               if n>m:
                   n=m
                   min=words[j]
    
           newSentence2=newSentence2+' <div class="correct">'+min+'</div>' 
              
    
    end_time=timer()
    waktu_BF=(end_time-start_time)
    print("waktu BF ",waktu_BF)

    return [newSentence,waktu_DP,newSentence2,waktu_BF]
def KMP(word,pattern,table):
    word=word.lower()
    pattern=pattern.lower()
    lenWord=len(word)
    lenPattern=len(pattern)
    if lenWord!=lenPattern:
        return False
    else:
        i=int(0)
        j=int(0)
        while i<lenWord:
              
            if word[i]==pattern[j]:
                i+=1
                j+=1
            elif j==0:
                j=0
                i+=1
            else:
                j=table[j-1]
            if j==lenPattern:
                return True
    return False
            
            
def failure(word):
    wordBorder=[0 for _ in range(0,len(word))]
    i=1
    j=0
    while i<len(word):
        
        if word[i]==word[j]:
            wordBorder[i]=j+1
            i+=1
            j+=1
        else:
            if (j>0):
                j=wordBorder[j-1]
            else:
                j=0
                i+=1
    return wordBorder

def levenshteinFullMatrix(str1, str2):
    
    m = len(str1)
    n = len(str2)
 
    # Initialize a matrix to store the edit distances
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
 
    # Initialize the first row and column with values from 0 to m and 0 to n respectively
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
 
    # Fill the matrix using dynamic programming to compute edit distances
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                # Characters match, no operation needed
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Characters don't match, choose minimum cost among insertion, deletion, or substitution
                dp[i][j] = 1 + min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1])
 
    # Return the edit distance between the strings
    return dp[m][n]

def brute_force(text, pattern):
    text=text.lower()
    pattern=pattern.lower()
    for i in range(len(text) - len(pattern) + 1):
        j = 0
        while j < len(pattern) and text[i + j] == pattern[j]:
            j += 1
        if j == len(pattern):
            return True
    return False


def search_pattern(pattern, text):
    # Get the lengths of the pattern and the text
    m = len(pattern)
    n = len(text)

    # A loop to slide pattern over text one by one
    for i in range(n - m + 1):
        # For current index i, check for pattern match
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        
        # If the entire pattern matches the text starting at index i
        if j == m:
            return 1
    
    return 0
    
def autocomplete(sentences):
    text=sentences.split()
    newSentence=''
    lps=[]
    for i in text:
        if i[len(i)-3:]=="...":
            lps.append(failure(i[:-3]))
    start_time=timer()   
    
    for i in text:
        cekBreak=False
        cekTitik=False
        for j in (history):
            
            teksCek=j.split()
            ind=0
            for k in teksCek:
                
                if i[len(i)-3:]=="...":
                    cekTitik=True
                    
                    if KMP(k[:len(i)-3],i[:-3],lps[ind]):
                        cekBreak=True
                        ind+=1
                        for l in range(teksCek.index(k),len(teksCek)):
                            newSentence=newSentence+' '+teksCek[l]
                if cekBreak:
                    break          

        if cekTitik==False:
            newSentence=newSentence+' '+i   

    end_time=timer() 
    waktu_KMP=end_time-start_time
    print("KMP",(end_time-start_time) * 10**3, "ms")
    newSentence1=''
    
    
    start_time=timer()
    
    for i in text:
        cekBreak=False
        cekTitik=False
        for j in (history):
            
            teksCek2=j.split()

            for k in teksCek2:

                if i[len(i)-3:]=="...":
                    cekTitik=True
                       
                    if brute_force(k[:len(i)-3],i[:-3]):
                        cekBreak=True
                        for l in range(teksCek2.index(k),len(teksCek2)):
                            newSentence1=newSentence1+' '+teksCek2[l]
                


                if cekBreak:
                    break          

        if cekTitik==False:
            newSentence1=newSentence1+' '+i 
   
    end_time=timer()
    waktu_BF=end_time-start_time
    print("Brute force ",(end_time-start_time) * 10**3, "ms")
    
    
    return [newSentence,waktu_KMP,newSentence1,waktu_BF]   
if __name__=="__main__":
    web.run()