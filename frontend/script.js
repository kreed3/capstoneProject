// 

const data = {year:"oneyear", yearText:"One Year", weather:"severe"}

function chooseYear(state) {
    let selected = state.options[state.selectedIndex].innerHTML;
    let value = state.value;
    alert("Selected state: " + selected + ". Value: " + value);
    data ["year"] = value;
    data["yearText"] = selected;
    //getData(value, selected);
}

function chooseWeather(weather) {
    let selected = weather.options[weather.selectedIndex].innerHTML;
    let value = weather.value;
    alert("Selected state: " + selected + ". Value: " + value);
    data ["weather"] = value;
    //getData(value, selected);
    //getData(value, selected, weather);
}

function handleSubmit() { 
    getData(data["year"], data["yearText"], data["weather"])

}

//ADDING DATA TO THE CHART: ----------------------------------------------------------------------------------------
async function getData(value, selected, weather) {
    console.log(data)
    const response = await fetch("http://127.0.0.1:5000/data");
    const jsonData = await response.json(); // fetching data and awaiting response from server
    //console.log(jsonData); //making sure data was getting through
    //
    // extracting data from tenyear dictionary
    let temp = jsonData[value!==""?value:"oneyear"]
    let selectedText = selected!==""?selected:"One Year"

    const keys = Object.keys(temp)
    console.log(value)
    let normData = []
    keys.map((key) => {
        //console.log(jsonData["tenyear"][key]["severe"])
        const value = {name: key, score: parseFloat(temp[key][weather]*100).toFixed(2)} //changing bars to percent
        normData.push(value)
    })

    // assigning actual stuff to the chart attributes
    let chartjson = {
        "title": "Residents Movement from Louisiana After " + selectedText + " of " + weather + " weather",
        "data": normData,

        "xtitle": "states",
        "ytitle": "probability",
        "ymax": 100,
        "ykey": 'score',
        "xkey": "name",
        "prefix": "%"

        
    }
    //CREATING THE CHART ----------------------------------------------------------------------------------------
     //chart colors
        var colors = [];
        const getRandomHex = () => {
            let n = (Math.random() * 0xfffff * 1000000).toString(16)
            return '#' + n.slice(0,6)
        }
        for (var i = 0; i < chartjson.data.length; i++) {
                colors[i]= getRandomHex()
        }

        //constants
        var TROW = 'tr',
            TDATA = 'td';
        
        var chart = document.createElement('div');
        //create the chart canvas
        var barchart = document.createElement('table');
        //create the title row
        var titlerow = document.createElement(TROW);
        //create the title data
        var titledata = document.createElement(TDATA);
        //make the colspan to number of records
        titledata.setAttribute('colspan', chartjson.data.length + 1);
        titledata.setAttribute('class', 'charttitle');
        titledata.innerText = chartjson.title;
        titlerow.appendChild(titledata);
        barchart.appendChild(titlerow);
        chart.appendChild(barchart);

        //create the bar row
        var barrow = document.createElement(TROW);
        
        //lets add data to the chart
        for (var i = 0; i < chartjson.data.length; i++) {
            barrow.setAttribute('class', 'bars');
            var prefix = chartjson.prefix || '';
            //create the bar data
            var bardata = document.createElement(TDATA);
            var bar = document.createElement('div');
            //bar.setAttribute('class', colors[0] );
            bar.style.backgroundColor=colors[i]
            bar.style.height = chartjson.data[i][chartjson.ykey] + prefix;
            bar.style.width = "25px";
            bardata.innerText = chartjson.data[i][chartjson.ykey] + prefix;
            bardata.appendChild(bar);
            barrow.appendChild(bardata);
        }
        
        //create legends
        var legendrow = document.createElement(TROW);
        var legend = document.createElement(TDATA);
        legend.setAttribute('class', 'legend');
        legend.setAttribute('colspan', chartjson.data.length);
        
        //add legend data
        for (var i = 0; i < chartjson.data.length; i++) {
            var legbox = document.createElement('span');
            legbox.setAttribute('class', 'legbox');
            var barname = document.createElement('span');
            barname.setAttribute('class',' xaxisname');
            barname.style.backgroundColor= colors[i]
            var bartext = document.createElement('span');
            bartext.innerText = chartjson.data[i][chartjson.xkey];
            legbox.appendChild(barname);
            legbox.appendChild(bartext);
            legend.appendChild(legbox);
        }
        barrow.appendChild(legend);
        barchart.appendChild(barrow);
        barchart.appendChild(legendrow);
        chart.appendChild(barchart);
        document.getElementById('chart').innerHTML = chart.outerHTML;

    //console.log(normData)
    //const textdata = document.getElementById("data").innerHTML = jsonData["oneyear"]["Alabama"]["norm"]
}



//getData("", "")

