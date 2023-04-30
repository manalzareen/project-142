from flask import Flask, jsonify, request
import pandas as pd
from demographic_filtering import output
from content_filtering import get_recommendations

articles_data = pd.read_csv('articles.csv')
all_articles = articles_data[['url' , 'title' , 'text' , 'lang' , 'total_events']]
liked_articles = []
not_liked_articles = []

app = Flask(__name__)

def assign_val():
    m_data = {
        "url": all_articles.iloc[0,0],
        "title": all_articles.iloc[0,1],
        "text": all_articles.iloc[0,2] or "N/A",
        "lang": all_articles.iloc[0,3],
        "total_events": all_articles.iloc[0,4]/2
    }
    return m_data

@app.route("/get-article")
def get_article():

    article_info = assign_val()
    return jsonify({
        "data": article_info,
        "status": "success"
    })

@app.route("/liked-article")
def liked_article():
    global all_articles
    article_info = assign_val()
    liked_articles.append(article_info)
    all_articles.drop([0], inplace=True)
    all_articles = all_articles.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

@app.route("/unliked-article")
def unliked_article():
    global all_articles
    article_info = assign_val()
    not_liked_articles.append(article_info)
    all_articles.drop([0], inplace=True)
    all_articles = all_articles.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

# API to return most popular articles.
@app.route("/popular-articles")
def popular_articles():
    popular_articles=[]
    for index,value in output.iterrows():
        p_a={
            "url":rows["url"],
            "title":rows["title"],
            "text":rows["text"],
             "language":rows["lang"],
             "total_events":rows["total_events"]/2
        }
        popular_articles.append(p_a)

    return jsonify({
        "status":"success",
        "data":popular_articles
    })

# API to return top 10 similar articles using content based filtering method.
@app.route("/recommended-articles")
def recommended_articles():
    global liked_article
    col_names=["url","title","text","lang","total_events"]
    all_articles=pd.DataFrame(columns=col_names)
    for i in liked_article:
        rem =get_recommendations(i["title"])
        all_recommended=all_recommended.append(rem)
    all_recommended.drop_duplicates(subset=["title"],inplace=True)
    ra=[]
    for index,rows in all_recommendated.iterrows():
        r={
            "url":rows["url"],
            "title":rows["title"],
            "text":rows["text"],
             "language":rows["lang"],
             "total_events":rows["total_events"]/2
        }
        ra.append(r)

    return jsonify({
        "status":"success",
        "data":popular_articles
    })
    
    

if __name__ == "__main__":
    app.run()