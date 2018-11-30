var buzzword = d3.select("p").text()

function unpack(rows, index) {
    return rows.map(function (row) {
        return row[index];
    });
}

function handleSubmit() {

    d3.event.preventDefault();

}


function buildPlot() {

    var dataurl = `/getplotdata/${buzzword}`;
    //var dataurl = `/getplotdata/email`;
    $.ajax({
        url: dataurl,
        success: function (d) {
            //console.log("ajaz data " + JSON.stringify(d));
            var dateList = [];
            var dateMap = new Map();

            for (var i = 0; i < d.length; i++) {
                let newDate = new Date(d[i]["date"]).toISOString().split('T')[0];
                if(newDate.includes("2016")){
                    let val = dateMap.get(newDate);
                    if (val != null) {
                        val = val + 1;
                        dateMap.set(newDate, val);
                    } else {
                        val = 1;
                        dateMap.set(newDate, val);
                    }
                }
                
            }


            var sortedMap = new Map([...dateMap.entries()].sort());
            let dates = [...sortedMap.keys()];
            let counts = [...sortedMap.values()];

            let startDate = dates[0];
            let endDate = dates[dates.length -1]

            var trace = {
                type: "scatter",
                mode: "lines",
                name: name,
                x: dates,
                y: counts,
                line: {
                  color: "#17BECF"
                }
              };

              var data = [trace];

              var layout = {
                title: `${buzzword} Buzzword Twitter Trends in 2016 - Wisconsin`,
                xaxis: {
                  range: [startDate, endDate],
                  type: "date"
                },
                yaxis: {
                  autorange: true,
                  type: "linear"
                }
              };
          
              Plotly.newPlot("plot", data, layout);

        }
    }

    );


}
buildPlot();



d3.select("#submit").on("click", function () {
    d3.event.preventDefault();

    var inputElement = d3.select("#stockInput");

    var inputValue = inputElement.property("value");


    console.log("Get data for " + inputValue);

    buildPlot(inputValue);
});
