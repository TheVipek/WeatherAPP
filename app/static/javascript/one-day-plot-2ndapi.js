var data_set ;
$.ajaxSetup({
    async:false
});
$.getJSON("../one_day.json",function(data) {
        data_set = data;

});



const ctx = document.getElementById('myChart').getContext('2d');

const myChart = new Chart(ctx, {
    type: 'line', // type of chart
    
    options:{ // options for chart
        responsive:true,
        interaction:{
            intersect:false,
            axis:'x'
        },
        animation:{
            y:{ // quick animation for Y 
                duration:2500,
                easing:'easeInSine'
            }
        },
        scales:{
            y:{
                ticks:{
                    
                    display:false  // make points at left not visible (y)
                    
                },
                grid:{
                    display:true // display grid in background (y)
                },
                /*title:{
                    color:'rgba(0,0,0,1)'
                }*/


            },
            x:{
                ticks:{
                    
                },
                grid:{
                    display:true // display grid in background (x)
                }

            }
        },
        plugins:{//settings like title ,subtitle above and much more
            title:{
                
                display:false,
                text:'WeatherAPP'
            },
            subtitle:{
                display:false,
                text:'1 Day Weather'
            }
        }
    },
     // dataset
     data: {//values under x (00:00 , 05:00 etc.)

        labels: [data_set["days"][0]["time"][0],data_set["days"][0]["time"][2],data_set["days"][0]["time"][4],data_set["days"][0]["time"][6],
        data_set["days"][0]["time"][8],data_set["days"][0]["time"][10],data_set["days"][0]["time"][12],data_set["days"][0]["time"][14],
        data_set["days"][0]["time"][16],data_set["days"][0]["time"][18],data_set["days"][0]["time"][20],data_set["days"][0]["time"][22]
        ],             
        datasets: [{ 
            pointRadius:4,   // point size by default and after hover v 
            hoverRadius:7,
            label: 'Temperature',
            data: [data_set["days"][0]["temp_c"][0],data_set["days"][0]["temp_c"][2],data_set["days"][0]["temp_c"][4],data_set["days"][0]["temp_c"][6],
            data_set["days"][0]["temp_c"][8],data_set["days"][0]["temp_c"][10],data_set["days"][0]["temp_c"][12],data_set["days"][0]["temp_c"][14],
            data_set["days"][0]["temp_c"][16],data_set["days"][0]["temp_c"][18],data_set["days"][0]["temp_c"][20],data_set["days"][0]["temp_c"][22]
            ],
            backgroundColor: ['#2c685b'], // used color inside label selector and points that are at graph
            
            borderColor: ['#9e4356'], // color of line and label border
            fill:true,
            tension:0.5, // making it less 'tensionous'
            borderWidth: 5
        }]

    },
});