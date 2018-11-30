from flask import Flask, jsonify, render_template
import pymongo
import re



app = Flask(__name__)

#conn = 'mongodb://localhost:27017'
conn = 'mongodb://edwardwisejr:Flender77!@ds255403.mlab.com:55403/manufacture_consent'
client = pymongo.MongoClient(conn)

#db = client['buzzword']
db = client.get_database()
#db_details = db['twitter']
db_details = db['mc_tweets_to_plot']


@app.route("/")
def home():
    return render_template("landingpage.html")

@app.route("/mapwi")
def mapwi():
    return render_template("map_wi.html")

@app.route("/buzzwordmap/<buzzword>")
def buzzwordmap(buzzword):
    print(f'map buzz word {buzzword}')
    return render_template("map_buzzwordmap.html", buzzword=buzzword)


@app.route("/getdata/<buzzword>")
def getdata(buzzword):
    print(f'buzz word getdata {buzzword}')
    rgx = re.compile(f'.*{buzzword}.*', re.IGNORECASE)

    fetchData = db_details.find({'buzz_word': rgx})
    #fetchData = db_details.find()

    dataList = []
    for x in fetchData:
        obj = {}
        obj['buzzword'] = x['buzz_word']
        obj['date'] = x['date']
        obj['lat'] = x['lat']
        obj['lon'] = x['long']
        obj['source'] = x['source']
        dataList.append(obj)
    print(f'Rendering  data {dataList}')
    return jsonify(dataList)


@app.route("/trends/<buzzword>")
def trends(buzzword):
    print(f'trends buzz word {buzzword}')
    return render_template("plot.html", buzzword=buzzword)

@app.route("/getplotdata/<buzzword>")
def plotData(buzzword):
    
    return getdata(buzzword)



if __name__ == "__main__":
    app.run(debug=True)