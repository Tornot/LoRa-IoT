let receivedData = []
window.onload = (event) => {
    let x = []
    let y = []

    receivedData.forEach((item,index)=>{
        console.log("hello");
    })

    let _data = [{
        x: ['giraffes', 'orangutans', 'monkeys'],
        y: [20, 14, 23],
        type: 'bar'
    }];

    Plotly.newPlot('myDiv', _data);

}

let xhr = new XMLHttpRequest();
request = "/get_temperature_data"
xhr.onreadystatechange = function () {
    receivedData = xhr.responseText
};
xhr.open("GET", request, true)
xhr.send();

