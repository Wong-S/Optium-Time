"use strict";

const barChart = new Chart(
  $('#bar-chart'),
  {
    type: 'bar',
    data: {
      labels: ['Watermelon', 'Canteloupe', 'Honeydew'],
      datasets: [
        {
          label: 'Today',
          data: [10, 36, 27]
        },
        {
          label: 'Yesterday',
          data: [5, 0, 7]
        }
      ]
    }
  }
);

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

$.get('/total-sleep.json', (res) => {
  // We need to restructure the generic data we got from the server. In this
  // case, we need an array of objects like this:
  // [{x: xValue, y: yValue}, ...,]
  const data = [];
  for (const dailyTotal of res.data) {
    data.push({x: dailyTotal.date, y: dailyTotal.sleep_hours});
  }

  // Since Chart.js doesn't understand that we want to plot this data by *time*,
  // the resulting line graph is really ugly.
  //
  // See the next demo for how to use times on the x- or y-axis.
  new Chart(
    $('#line-chart'),
    {
      type: 'line',
      data: {
        datasets: [
          {
            label: 'All Melons',
            data: data
          }
        ]
      }
    }
  );
});

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
