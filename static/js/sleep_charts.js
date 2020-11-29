//"use strict";

// const barChart = new Chart(
//   $('#bar-chart'),
//   {
//     type: 'bar',
//     data: {
//       labels: ['Watermelon', 'Canteloupe', 'Honeydew'],
//       datasets: [
//         {
//           label: 'Today',
//           data: [10, 36, 27]
//         },
//         {
//           label: 'Yesterday',
//           data: [5, 0, 7]
//         }
//       ]
//     }
//   }
// );

const colorfulBarChart = new Chart(
  $('#bar-colors'),
  {
    type: 'bar',
    data: {
      labels: ['Watermelon', 'Canteloupe', 'Honeydew'],
      datasets: [
        {
          label: 'Today',
          data: [15, 36, 27]
        },
        {
          label: 'Yesterday',
          data: [5, 0, 7]
        }
      ]
    },
    options: {
      datasets: {
        bar: {
          // We use a function to automatically set the background color of
          // each bar in the bar chart.
          //
          // There are many other properties that accept functions. For more
          // information see: https://www.chartjs.org/docs/latest/general/options.html#scriptable-options
          backgroundColor: () => {
            // `randomColor` is a JS module we found off GitHub: https://github.com/davidmerfield/randomColor
            // We imported it in templates/chartjs.html
            return randomColor();
          }
        }
      },
      scales: {
        // This is where you can configure x- and y-axes if you don't like the
        // automatic range that Chart.js sets for you.
        //
        // For more info see: https://www.chartjs.org/docs/latest/axes/cartesian/
        yAxes: [
          {
            ticks: {
              min: 0,
              max: 40
            }
          },
        ]
      }
    }
  }
);

// $.get('/total-sleep.json', (res) => {
//   // We need to restructure the generic data we got from the server. In this
//   // case, we need an array of objects like this:
//   // [{x: xValue, y: yValue}, ...,]
//   const data = [];
//   for (const dailyTotal of res.data) {
//     data.push({x: dailyTotal.date, y: dailyTotal.sleep_hours});
//   }

//   // Since Chart.js doesn't understand that we want to plot this data by *time*,
//   // the resulting line graph is really ugly.
//   //
//   // See the next demo for how to use times on the x- or y-axis.
//   new Chart(
//     $('#line-chart'),
//     {
//       type: 'line',
//       data: {
//         datasets: [
//           {
//             label: 'All Melons',
//             data: data
//           }
//         ]
//       }
//     }
//   );
// });

$.get('/total-sleep.json', (res) => {
  // In order to make this work, you need to use ISO-formatted date/time
  // strings. Check out the view function for `/sales_this_week.json` in
  // server.py to see an example.
  const data = res.data.map((dailyTotal) => {
    return {x: dailyTotal.date, y: dailyTotal.sleep_hours};
  });

  // Also, to enable scaling by time, you need to import Moment *before*
  // Chart.js. See `templates/chartjs.html`.
  new Chart(
    $('#line-time'),
    {
      type: 'line',
      data: {
        datasets: [
          {
            backgroundColor : "rgba(252,233,79,0.5)",
            borderColor : "rgba(82,75,25,1)",
            pointBackgroundColor : "rgba(166,152,51,1)",
            pointBorderColor : "#fff",
            label: 'Total Sleep Hours per Week',
            data: data
          }
        ]
      },
      options: {
        scales: {
          xAxes: [
            {
              type: 'time',
              distribution: 'series'
            }
          ]
        },
        tooltips: {
          callbacks: {
            title: (tooltipItem) => {
              // The default tooltip shows ISO-formatted date/time strings
              // that are hard to read.
              //
              // Moment is a JS library that is similar to Python's datetime
              // module. Instead of using % syntax to format date/time, Moment
              // uses its own formatting syntax.
              //
              // In this example, we want to display a date that looks
              // like 'Jan 20'.
              return moment(tooltipItem.label).format('MMM D');
            }
          }
        }
      }
    }
  );
});


/////////////////////////////////////////////////////
//HYPNOGRAM graph

// $.get('/hypnogram-sleep.json', (res) => {

//   //////////THIS WORKS
//   var data = {
//       labels : ["January","February","March",
//                   "April","May","June",
//                   "July","Agost","September",
//                   "October","November","December"],
//       datasets : [
//         {
//           backgroundColor : "rgba(252,233,79,0.5)",
//           borderColor : "rgba(82,75,25,1)",
//           pointBackgroundColor : "rgba(166,152,51,1)",
//           pointBorderColor : "#fff",
//           data : [65,68,75,
//                         81,95,105,
//                         130,120,105,
//                         90,75,70],
//           steppedLine: true
//         }
//       ]
//     }
  
  
  
//     // Also, to enable scaling by time, you need to import Moment *before*
//     // Chart.js. See `templates/chartjs.html`.
//     new Chart(
//       $('#line-hypnogram'),
//       {
//         type: 'line',
//         data: data,
  
  
//           // scales: {
//           //   // xAxes: [
//           //   //   {
//           //   //     type: 'linear',
//           //   //     distribution: 'bottom'
//           //   //   }
//           //   // ]
//           //   // yAxes: [{ticks: {beginAtZero: true, callback: function(value,index,values) {return data;}}}]
//           // },
  
//         }
  
//     );
//   });
  


  // $.get('/hypnogram-sleep.json', (res) => {

  //   //////////THIS WORKS
  //   var data = {
  //       labels : ['Awake', 'NREM1', 'NREM2', 'NREM3', 'REM', 'NREM2', 'NREM3', 'REM', 'NREM2', 'NREM3', 'REM', 'NREM2', 'NREM3', 'REM', 'NREM2', 'NREM3', 'REM', 'NREM2', 'NREM3', 'REM', 'NREM2', 'NREM3', 'REM', 'Awake'],
  //       datasets : [
  //         {
  //           backgroundColor : "rgba(252,233,79,0.5)",
  //           borderColor : "rgba(82,75,25,1)",
  //           pointBackgroundColor : "rgba(166,152,51,1)",
  //           pointBorderColor : "#fff",
  //           data : [15, 20, 42, 80, 90, 100, 128, 180, 193, 226, 270, 280, 301, 360, 371, 396, 450, 471, 510, 540, 553, 580, 618, 630],
  //           steppedLine: true
  //         }
  //       ]
  //     }
    
    
    
  //     // Also, to enable scaling by time, you need to import Moment *before*
  //     // Chart.js. See `templates/chartjs.html`.
  //     new Chart(
  //       $('#line-demo-months'),
  //       {
  //         type: 'line',
  //         data: data,
    
    
  //           // scales: {
  //           //   // xAxes: [
  //           //   //   {
  //           //   //     type: 'linear',
  //           //   //     distribution: 'bottom'
  //           //   //   }
  //           //   // ]
  //           //   // yAxes: [{ticks: {beginAtZero: true, callback: function(value,index,values) {return data;}}}]
  //           // },
    
  //         }
    
  //     );
  //   });
    
  // $.get('/hypnogram-sleep.json', (res) => {

    //////////THIS WORKS
// var data = {
//     labels : ["January","February","March",
//                 "April","May","June",
//                 "July","Agost","September",
//                 "October","November","December"],
//     datasets : [
//       {
//         backgroundColor : "rgba(252,233,79,0.5)",
//         borderColor : "rgba(82,75,25,1)",
//         pointBackgroundColor : "rgba(166,152,51,1)",
//         pointBorderColor : "#fff",
//         data : [65,68,75,
//                       81,95,105,
//                       130,120,105,
//                       90,75,70],
//         steppedLine: true
//       }
//     ]
//   }
    
    
    
//       // Also, to enable scaling by time, you need to import Moment *before*
//       // Chart.js. See `templates/chartjs.html`.
//   new Chart(
//     $('#line-demo-months'),
//     {
//       type: 'line',
//       data: data,


//         // scales: {
//         //   // xAxes: [
//         //   //   {
//         //   //     type: 'linear',
//         //   //     distribution: 'bottom'
//         //   //   }
//         //   // ]
//         //   // yAxes: [{ticks: {beginAtZero: true, callback: function(value,index,values) {return data;}}}]
//         // },

//       }

//   );
    // });
      


      $.get('/hypnogram-sleep.json', (res) => {
        console.log(res)
        // console.log(res.data[0].sleep_labels) //Sleep log 
        // console.log(res.data[0].time_data)

        //////////THIS WORKS
        var yLabels = {
          1: 'NREM3', 2: 'NREM2', 3: 'NREM1', 4: 'REM', 5: 'Awake'
        }

        var data = {
            labels :  res.data.time_data,
            datasets : [
              {
                backgroundColor : "rgba(252,233,79,0.5)",
                borderColor : "rgba(82,75,25,1)",
                pointBackgroundColor : "rgba(166,152,51,1)",
                pointBorderColor : "#fff",
                data : res.data.sleep_labels,
                steppedLine: true
              }
            ]
          }
        
        
        
          // Also, to enable scaling by time, you need to import Moment *before*
          // Chart.js. See `templates/chartjs.html`.
          new Chart(
            $('#line-hypnogram'),
            {
              type: 'line',
              data: data,
        
              options : {
                scales : { 
                  xAxes:[{
                    ticks: {
                      beginAtZero: true
                    }
                  }],
                  yAxes: [{
                    ticks : {
                      beginAtZero: true,

                      callback: function(value, index, values) {
                        return yLabels[value];
                      }
                    }
                  }]
                }
              }
        
                // scales: {
                //   // xAxes: [
                //   //   {
                //   //     type: 'linear',
                //   //     distribution: 'bottom'
                //   //   }
                //   // ]
                //   // yAxes: [{ticks: {beginAtZero: true, callback: function(value,index,values) {return data;}}}]
                // },
        
              }
        
          );
        });
//////////THIS WORKS
//DOUGHNUT Chart.js

$.get('/hypnogram-sleep.json', (res) => {
  console.log(res)
  // console.log(res.data[0].sleep_labels) //Sleep log 
  // console.log(res.data[0].time_data)

  //////////THIS WORKS
  var data = {
      labels : res.data.doughnut_name,
      datasets : [
        {
          backgroundColor : ["#0074D9", "#FF4136", "#2ECC40", "#FF851B"],
          borderColor : "rgba(82,75,25,1)",
          pointBackgroundColor : "rgba(166,152,51,1)",
          pointBorderColor : "#fff",
          data : res.data.doughnut_percent
          
        }
      ]
    }
  
  
  
    // Also, to enable scaling by time, you need to import Moment *before*
    // Chart.js. See `templates/chartjs.html`.
    new Chart(
      $('#doughnut-sleep-stages'),
      {
        type: 'doughnut',
        data: data,
  
  
          // scales: {
          //   // xAxes: [
          //   //   {
          //   //     type: 'linear',
          //   //     distribution: 'bottom'
          //   //   }
          //   // ]
          //   // yAxes: [{ticks: {beginAtZero: true, callback: function(value,index,values) {return data;}}}]
          // },
  
        }
  
    );
  });





// $.get('/hypnogram-sleep.json', (res) => {})
// var scatterChart = new Chart(ctx, {
//   type: 'scatter',
//   data: {
//       datasets: [{
//           label: 'Scatter Dataset',
//           data: [{
//               x: -10,
//               y: 0
//           }, {
//               x: 0,
//               y: 10
//           }, {
//               x: 10,
//               y: 5
//           }]
//       }]
//   },
//   options: {
//       scales: {
//           xAxes: [{
//               type: 'linear',
//               position: 'bottom'
//           }]
//       }
//   }
// });

// var myChart = new Chart(ctx, {
//   type: 'bar',
//   data: {
//       labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
//       datasets: [{
//           label: '# of Votes',
//           data: [12, 19, 3, 5, 2, 3],
//           backgroundColor: [
//               'rgba(255, 99, 132, 0.2)',
//               'rgba(54, 162, 235, 0.2)',
//               'rgba(255, 206, 86, 0.2)',
//               'rgba(75, 192, 192, 0.2)',
//               'rgba(153, 102, 255, 0.2)',
//               'rgba(255, 159, 64, 0.2)'
//           ],
//           borderColor: [
//               'rgba(255, 99, 132, 1)',
//               'rgba(54, 162, 235, 1)',
//               'rgba(255, 206, 86, 1)',
//               'rgba(75, 192, 192, 1)',
//               'rgba(153, 102, 255, 1)',
//               'rgba(255, 159, 64, 1)'
//           ],
//           borderWidth: 1
//       }]
//   },
//   options: {
//       scales: {
//           yAxes: [{
//               ticks: {
//                   beginAtZero: true
//               }
//           }]
//       }
//   }
// });



//Weekly Sleep Log by Time Scale

$.get('/weekly-sleep-data.json', (res) => {
  console.log(res)
  // In order to make this work, you need to use ISO-formatted date/time
  // strings. Check out the view function for `/sales_this_week.json` in
  // server.py to see an example.
  
  // const data = res.data.map((dailyTotal) => {
  //   return {x: dailyTotal.date, y: dailyTotal.sleep_hours};
  // });

  // Also, to enable scaling by time, you need to import Moment *before*
  // Chart.js. See `templates/chartjs.html`.

  const barChart = new Chart(
    $('#weekly-bar-scale'),
    {
      type: 'bar',
      data: {
        labels: res.data.dates_over_time,
        datasets: [
          {
            //label: res.data.dates_over_time,
            data: res.data.total_hours
          },
        ]
      },
      options: {
        datasets: {
          bar: {
            // We use a function to automatically set the background color of
            // each bar in the bar chart.
            //
            // There are many other properties that accept functions. For more
            // information see: https://www.chartjs.org/docs/latest/general/options.html#scriptable-options
            backgroundColor: () => {
              // `randomColor` is a JS module we found off GitHub: https://github.com/davidmerfield/randomColor
              // We imported it in templates/chartjs.html
              return randomColor();
            }
          }
        },
        scales: {
          yAxes : [{
            ticks: {
              beginAtZero: true,
              

            }
          }]
        }
      }
    }
  );
  // new Chart(
  //   $('#weekly-time-scale'),
  //   {
  //     type: 'line',
  //     data: {
  //       datasets: [
  //         {
  //           backgroundColor : "rgba(252,233,79,0.5)",
  //           borderColor : "rgba(82,75,25,1)",
  //           pointBackgroundColor : "rgba(166,152,51,1)",
  //           pointBorderColor : "#fff",
  //           label: 'Total Sleep Hours per Week',
  //           data: [1,2,3,4,5]
  //         }
  //       ]
  //     },
  //     options: {
  //       scales: {
  //         xAxes: [
  //           {
  //             type: 'time',
  //             distribution: 'series'
  //           }
  //         ]
  //       },
  //       tooltips: {
  //         callbacks: {
  //           title: (tooltipItem) => {
  //             // The default tooltip shows ISO-formatted date/time strings
  //             // that are hard to read.
  //             //
  //             // Moment is a JS library that is similar to Python's datetime
  //             // module. Instead of using % syntax to format date/time, Moment
  //             // uses its own formatting syntax.
  //             //
  //             // In this example, we want to display a date that looks
  //             // like 'Jan 20'.
  //             return moment(tooltipItem.label).format('MMM D');
  //           }
  //         }
  //       }
  //     }
  //   }
  // );
});

// const barChart = new Chart(
//   $('#weekly-bar-scale'),
//   {
//     type: 'bar',
//     data: {
//       labels: ['Watermelon', 'Canteloupe', 'Honeydew'],
//       datasets: [
//         {
//           label: 'Today',
//           data: [10, 36, 27]
//         },
//         {
//           label: 'Yesterday',
//           data: [5, 0, 7]
//         }
//       ]
//     }
//   }
// );

//MONTHLY LINE SCALE CHART


$.get('/monthly-sleep-data.json', (res) => {
  console.log(res)

  // const data = res.data.map((dailyTotal) => {
  //   return {x: dailyTotal.monthly_dates_over_time, y: dailyTotal.total_monthly_hours};
  // });
  // In order to make this work, you need to use ISO-formatted date/time
  // strings. Check out the view function for `/sales_this_week.json` in
  // server.py to see an example.
  
  // const data = res.data.map((dailyTotal) => {
  //   return {x: dailyTotal.date, y: dailyTotal.sleep_hours};
  // });

  // Also, to enable scaling by time, you need to import Moment *before*
  // Chart.js. See `templates/chartjs.html`.

  const lineMonthlyChart = new Chart(
    $('#monthly-line-scale'),
    {
      type: 'line',
      data: {
      labels: res.data.monthly_dates_over_time,
        datasets: [
          {
            //label: res.data.dates_over_time,
            data: res.data.total_monthly_hours
          },
        ]
      },
      options: {
        scales: {
          xAxes: [{
            type: 'time',
            distribution: 'series'
          }],
          yAxes : [{
            ticks: {
              beginAtZero: true,
              

            }
          }]
        }
      },
      tooltips: {
        callbacks: {
          title: (tooltipItem) => {
            // The default tooltip shows ISO-formatted date/time strings
            // that are hard to read.
            //
            // Moment is a JS library that is similar to Python's datetime
            // module. Instead of using % syntax to format date/time, Moment
            // uses its own formatting syntax.
            //
            // In this example, we want to display a date that looks
            // like 'Jan 20'.
            return moment(tooltipItem.label).format('MMM D');
          }
        }
      }
    }
  );
  // new Chart(
  //   $('#weekly-time-scale'),
  //   {
  //     type: 'line',
  //     data: {
  //       datasets: [
  //         {
  //           backgroundColor : "rgba(252,233,79,0.5)",
  //           borderColor : "rgba(82,75,25,1)",
  //           pointBackgroundColor : "rgba(166,152,51,1)",
  //           pointBorderColor : "#fff",
  //           label: 'Total Sleep Hours per Week',
  //           data: [1,2,3,4,5]
  //         }
  //       ]
  //     },
  //     options: {
  //       scales: {
  //         xAxes: [
  //           {
  //             type: 'time',
  //             distribution: 'series'
  //           }
  //         ]
  //       },
  //       tooltips: {
  //         callbacks: {
  //           title: (tooltipItem) => {
  //             // The default tooltip shows ISO-formatted date/time strings
  //             // that are hard to read.
  //             //
  //             // Moment is a JS library that is similar to Python's datetime
  //             // module. Instead of using % syntax to format date/time, Moment
  //             // uses its own formatting syntax.
  //             //
  //             // In this example, we want to display a date that looks
  //             // like 'Jan 20'.
  //             return moment(tooltipItem.label).format('MMM D');
  //           }
  //         }
  //       }
  //     }
  //   }
  // );
});
