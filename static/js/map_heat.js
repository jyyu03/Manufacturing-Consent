
// Creating map object
var myMap = L.map("map", {
  center: [44.7844, -88.7879],
  zoom: 7,
  label: "test"
});

// Adding tile layer
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
}).addTo(myMap);



// Grabbing our GeoJSON data..
d3.json("/getdata", function (data) {
  console.log("getdata " + data[0].buzzword)
});






