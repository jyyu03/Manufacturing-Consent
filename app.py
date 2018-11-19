from flask import Flask, jsonify, render_template
import pymongo


app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client['buzzword']
db_details = db['twitter']

@app.route("/")
def home():
    return render_template("landingpage.html")

@app.route("/mapwi")
def mapwi():
    return render_template("map_wi.html")

@app.route("/buzzwordmap")
def buzzwordmap():
    return render_template("map_buzzwordmap.html")


@app.route("/getdata")
def getdata():
    fetchData = db_details.find()
    dataList = []
    for x in fetchData:
        obj = {}
        obj['buzzword'] = x['buzzword']
        obj['date'] = x['date']
        obj['lat'] = x['lat']
        obj['lon'] = x['lon']
        obj['source'] = x['source']
        dataList.append(obj)
    print(f'Rendering  data {dataList}')
    return jsonify(dataList)


if __name__ == "__main__":
    app.run(debug=True)