
// Creating map object
var heatMap = L.map("heatmap", {
  center: [44.7844, -88.7879],
  zoom: 7,
});

// Adding tile layer
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
}).addTo(heatMap);

function createRandom(value, count) {

  let randomList = [];
  for (let i = 0; i < count; i++) {

    randomList.push([+value[0] + Math.random()/100, +value[1] + Math.random()/100])
  }

  return randomList;
}
var buzzword = d3.select("p").text()
console.log("fetched buzzword from html " + buzzword);
//TODO temp hack
// if (buzzword === 'clinton') {
//   buzzword = "hillary's email";
// }
let url = `/getdata/${buzzword}`
console.log("url " + url)
// Grabbing our GeoJSON data..
d3.json(url, function (data) {

  let heatArray = [];

  for (let i = 0; i < data.length; i++) {
    //heatArray.push([data[i].lat, data[i].lon])
    let cnt = 1000;
    if(buzzword === "wall"){
      cnt = 100;
    }
    let lst = [];
    if((data[i].lat > 43 && data[i].lat < 45)){
      lst = createRandom([data[i].lat, data[i].lon], cnt);

    }


    for (let j = 0; j < lst.length; j++) {
      console.log("lst " + lst[i]);

      if(lst[i] != null){
        console.log("lst " + [lst[i][0], lst[i][1]]);

        heatArray.push([lst[i][0], lst[i][1]])
      }


    }

  }

  L.heatLayer(heatArray, {
    radius: 40,
    blur: 55,
    gradient: { 0.4: 'blue', 0.65: 'lime', 1: 'red' }
  }).addTo(heatMap);



  d3.json("../static/data/WI.geojson", function (data) {
    L.geoJson(data, {
      style: function (feature) {

        return {
          color: "black",
          weight: 0.5
        }
      },
      onEachFeature: function (feature, layer) {

        layer.on({
          mouseover: function (event) {
            layer = event.target;
          }
        })
        layer.bindPopup("<h5>" + feature.properties.COUNTY_NAME + "</h5>"
        );

      }
    }
    
    ).addTo(heatMap);
  });



});

var legend = L.control({ position: 'topright' });

legend.onAdd = function (map) {

  var div = L.DomUtil.create('div', 'info legend');
  div.innerHTML += '<h6><i>US Presidential Election 2016 - Wisconsin</i></h6> '
  div.innerHTML += '<br><i>Twitter Heatmap for buzzword :  '

  if("clinton" === buzzword){
    div.innerHTML += 'Hillary Clinton Emails</i> '

  } else {
    div.innerHTML += buzzword + '</i> '

  }
  return div;
};

legend.addTo(heatMap);







