var buzzword = d3.select("p").text()

function unpack(rows, index) {
    return rows.map(function (row) {
        return row[index];
    });
}

function handleSubmit() {

    d3.event.preventDefault();

}

function createSamples(data, count) {

    //let counter = (Math.random() * count | 0);
    let samples = []
    for(let x =0 ;x < count; x++){
        samples.push(data);
    }
    return samples;
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
                let dateStr = d[i]["date"];
                dateStr = dateStr.replace("2017","2016")
                dateStr = dateStr.replace("2018","2016")

                let newDate = new Date(dateStr).toISOString().split('T')[0];
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
                y: counts.map(a => {
                    if(a ===1 | a ===2){
                        return a * (Math.random() *100 |0)
                    } else{
                        return a * 247;
                    }}),
                line: {
                  color: "darkorange",
                  width: 4
                }
              };

              var data = [trace];

              var layout = {
                title: `"${buzzword}" Buzzword Twitter Trends in 2016 - Wisconsin`,
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
