var buzzword = d3.select("p").text()

function unpack(rows, index) {
    return rows.map(function (row) {
        return row[index];
    });
}

function handleSubmit() {

    d3.event.preventDefault();


}
function getData() {
    var url = `/getplotdata/${buzzword}`;
    console.log("url " + url)
    var list = []
    // d3.json(url, function (data) {
    //     console.log("getting json data " + data);
    //     list.push(data)
    // });

    d3.json(url, (data) => list = data);
    return list;
}

var plotData = getData();
console.log("plot data " + plotData.length);

function buildPlot() {

    var dataurl = `/getplotdata/${buzzword}`;
    console.log("url " + dataurl)
    $.ajax({
        url: dataurl,
        success: function(d){
            console.log("ajaz data " + d.length);
        }
    }

    );
    // d3.json(url, function (data) {
    //     console.log("getting json data " + data);

    //     var name = data.dataset.name;
    //     var stock = data.dataset.dataset_code;
    //     var startDate = data.dataset.start_date;
    //     var endDate = data.dataset.end_date;
    //     var dates = unpack(data.dataset.data, 0);
    //     var closingPrices = unpack(data.dataset.data, 1);
    //     var trace1 = {
    //         type: "scatter",
    //         mode: "lines",
    //         name: name,
    //         x: dates,
    //         y: closingPrices,
    //         line: {
    //             color: "#17BECF"
    //         }
    //     };

    //     var data = [trace1];

    //     var layout = {
    //         title: `${stock} closing prices`,
    //         xaxis: {
    //             range: [startDate, endDate],
    //             type: "date"
    //         },
    //         yaxis: {
    //             autorange: true,
    //             type: "linear"
    //         }
    //     };

    //     Plotly.newPlot("plot", data, layout);
    // });
    // d3.json("/getplotdata/clinton").then(function (data) {
    //     console.log("***fetching data " + data.length);




    // });

    // $.getJSON(url, function(data){
    //     console.log("fetched data " + data)
    // })


}
buildPlot();



d3.select("#submit").on("click", function () {
    d3.event.preventDefault();

    var inputElement = d3.select("#stockInput");

    var inputValue = inputElement.property("value");


    console.log("Get data for " + inputValue);

    buildPlot(inputValue);
});
