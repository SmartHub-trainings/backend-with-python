from flask import Flask,request,jsonify
import sqlite3 as sql
from datetime import datetime
def connect_db():
    connection = sql.connect("blogDb.db")
    cursor = connection.cursor()
    sql_query ="""CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY,
        title text NOT NULL,
        content text NOT NULL,
        created_at INTEGER,
        updated_at INTEGER
        )"""
    
    cursor.execute(sql_query)
    return cursor,connection

def parse_article(article_tuple:tuple):
    article ={"id":article_tuple[0],
                              "title":article_tuple[1],
                              "content":article_tuple[2],
                              "created_at":article_tuple[3],
                              "updated_at":article_tuple[4]
                              }
    return article
    

app = Flask(__name__)

@app.route("/articles",methods=["GET","POST"])
def all_articles():
    cursor ,connection=connect_db()
    method = request.method
    try:
        
        match method:
            case "GET":
                articles =[]
                sql_query ="SELECT * FROM articles"
                cursor.execute(sql_query)
                result = cursor.fetchall()
                
                for item in result:
                    article =parse_article(item)
                    articles.append(article)
                return {"message":"Get all articles","data":articles}
            case "POST":
                body = request.json
                
                sql_query ="INSERT INTO articles (title,content,created_at,updated_at) VALUES(?,?,?,?)"
                present_time =int(datetime.utcnow().timestamp())
               
                cursor.execute(sql_query,(body.get("title"),body.get("content"),present_time,present_time))
                connection.commit()
                # result = cursor.fetchall()
                return {"message":"Create an article"}
    except Exception as error:
        print(error)
    finally:
        connection.close()
        
        
@app.route("/articles/<int:article_id>",methods=["GET", "PUT","DELETE"])
def single_article_routes(article_id:int):
    method = request.method
    cursor ,connection=connect_db()
    try:
        match method:
            case 'GET':
                sql_query ="SELECT * FROM articles WHERE id=?"
                cursor.execute(sql_query,(article_id,))
                result =cursor.fetchone()
                print(result)
                article = parse_article(result)
                return jsonify({"message":"","data":article})
    except Exception as error:
        print(error)
    finally:
        connection.close()
        
        
        
    
        
    
        
    
    







if __name__ == "__main__":
    # connect_db()
    app.run(debug=True,port=6000)


"""
blog

routes 
  articles 
/articles fetch all articles =>get
/articles create an article =>post
/articles/article_id  gives details of a particular article =>get
/articles/article_id  update an articl=>put
/articles/article_id  update an articl=>delete
"""
