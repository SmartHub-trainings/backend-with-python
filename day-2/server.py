from flask import Flask,request

app = Flask(__name__)
database= {
    "Articles":[]
}

@app.route("/")
def index():
    # print(request.args)
    # print(request.args["id"])
    # # print(request.args.get("searchTermtyr"))
    # print(request.args.get("searchTermtyr","can not get"))
    
    
    
    return {"message":"Welcome to the home route"}

# @app.route("/articles")
# def get_all_articles():
#     return {"data":database.get("Articles"),"message":"Obtained all articles"}



@app.route("/articles",methods=["GET","POST"])
def get_all_or_create_an_article():
    method = request.method
    print(method)

    if method =="GET":
        return {"data":database.get("Articles"),"message":"Obtained all articles"}
    
    
    body = request.json
    print(body)
    body["id"]=len(database.get("Articles"))+1
    database["Articles"].append(body)
    return {"data":body,"message":"Created article successfully"}

@app.route("/articles/<int:id>")
def get_an_article_buy_id(id):
    articles = database.get("Articles")
    for article in articles:
        if article["id"]==id:
            return {"data":article,"message":"Created article successfully"}
    return {"data":None,"message":"No such article"}



@app.route("/articles/<int:id>", methods =["DELETE","PUT"])
def del_put_article(id):
    method = request.method

    print(method)
    articles= database.get("Articles")
    article = next((a for a in articles if a["id"] == id), None)

    # if not article:
    #     return {"data": None, "message":"Article not found"}


    if method == "DELETE":
        articles.remove(article)
        return {"data": None, "message": "Article remove successfully"}
        
    body = request.json
    body["id"] = id
    articles.append(body)
    return {"data": body, "message":"Article updated successfully"}







# def sortList(numbers:list):
#     numbers.sort()
#     return numbers


        









if __name__ == "__main__":
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
