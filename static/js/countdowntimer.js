// //"use strict";  NOTE: DO NOT INCLUDE! THE JS FILE WILL NOT RUN WHEN IMPORTING THE SCRIPT TAG IN THE HTML!!!

// var duration = moment.duration({
// 	// 'days': 1,
// 	//'hours': 1,
//   'minutes': 1,
//   'seconds': 00

// });

// var timestamp = new Date(0, 0, 0, 2, 10, 30); //2hr, 10min, 30 sec??
// var interval = 1; //Dictates the speed of the countdown. So at 2, it'll countdown faster
// var timer = setInterval(function() {
//   timestamp = new Date(timestamp.getTime() + interval * 1000);

//   duration = moment.duration(duration.asSeconds() - interval, 'seconds');
//   var hour = duration.hours();
//   var min = duration.minutes();
//   var sec = duration.seconds();

//   sec -= 1;
//   if (min < 0) return clearInterval(timer);
//   if (min < 10 && min.length != 2) min = '0' + min;
//   if (sec < 0 && min != 0) {
//     min -= 1;
//     sec = 59;
//   } else if (sec < 10 && length.sec != 2) sec = '0' + sec;

//   $('.countdown').text(min + ':' + sec);
//   if (min == 0 && sec == 0)
//     clearInterval(timer);


// }, 1000);



// var duration = moment.duration({
// 	//'days': 1,
// 	'hours': 2,
//   'minutes': 1,
//   'seconds': 00

// });

// var timestamp = new Date(0, 0, 0, 0, 0, 0); //hr, min, sec for last three numbers.
// var interval = 1; //dictates speed of the countdown. At 2, it'll countdown faster
// var timer = setInterval(function() {
//   timestamp = new Date(timestamp.getTime() + interval * 1000); //multiply by 1000 to correct for epoch time

//   duration = moment.duration(duration.asSeconds() - interval, 'seconds'); //so at 59 seconds and interval at 1, it'll count down to 58, 57, etc.
//   var hour = duration.hours(); //defining the variable at hours
//   var min = duration.minutes();
//   var sec = duration.seconds();

// 	//This is where the countdown is executed
//   sec -= 1; 
//   if (min < 0) return clearInterval(timer);
//   if (min < 10 && min.length != 2) min = '0' + min;
//   if (sec < 0 && min != 0 && hour == 0) {
//   	//hour -= 1;
//     min -= 1;
//     sec = 59;
//   } else if (sec < 10 && length.sec != 2) sec = '0' + sec;

//   $('.countdown').text(hour + ':' + min + ':' + sec);
//   if (hour == 0 && min == 0 && sec == 0)
//     clearInterval(timer);


// }, 1000);

// ////////////
// //"use strict";  NOTE: DO NOT INCLUDE! THE JS FILE WILL NOT RUN WHEN IMPORTING THE SCRIPT TAG IN THE HTML!!!

// var duration = moment.duration({
// 	// 'days': 1,
// 	'hours': 1,
//   'minutes': 0,
//   'seconds': 11

// });

// var timestamp = new Date(0, 0, 0, 2, 10, 30); //2hr, 10min, 30 sec??
// var interval = 1; //Dictates the speed of the countdown. So at 2, it'll countdown faster
// var timer = setInterval(function() {
//   timestamp = new Date(timestamp.getTime() + interval * 1000);

//   duration = moment.duration(duration.asSeconds() - interval, 'seconds');
//   var hour = duration.hours();
//   var min = duration.minutes();
//   var sec = duration.seconds();

//   sec -= 1;
//   if (hour < 0 && min < 0) return clearInterval(timer);
//   if (min < 10 && min.length != 2) min = '0' + min;
//   if (sec < 0 && min != 0 && hour < 0) {
//   	//hour -= 1,
//     min -= 1;
//     sec = 59;
//   } 
// /*   if (sec < 0 && min != 0) {
//     min -= 1,
//     sec = 59; */
//  else if (sec < 10 && length.sec != 2) sec = '0' + sec; //This displays after 10 seconds to 9 seconds as 09, 08, 07, etc. Just formatting
   

//   $('.countdown').text(hour + ':' + min + ':' + sec);
//   if (min == 0 && sec == 0)
//     clearInterval(timer);


// }, 1000);


// $.get('/countdown.json', (res) => {
//   console.log(res)


// let duration = moment.duration({
// 	//'days': 1,
// 	'hours': res.hours, //0, //res.hours,
//   'minutes': res.minutes, //0, //res.minutes,
//   'seconds': 00

// });

// let timestamp = new Date(0, 0, 0, 0, 0, 0); //hr, min, sec for last three numbers.
// let interval = 1; //dictates speed of the countdown. At 2, it'll countdown faster
// let timer = setInterval(function() {
//   timestamp = new Date(timestamp.getTime() + interval * 1000); //multiply by 1000 to correct for epoch time

//   duration = moment.duration(duration.asSeconds() - interval, 'seconds'); //so at 59 seconds and interval at 1, it'll count down to 58, 57, etc.
//   let hour = duration.hours(); //defining the variable at hours
//   let min = duration.minutes();
//   let sec = duration.seconds();

// 	//This is where the countdown is executed
//   sec -= 1; 
//   if (min < 0) return clearInterval(timer);
//   if (min < 10 && min.length != 2) min = '0' + min;
//   if (sec < 0 && min != 0 && hour == 0) {
//   	//hour -= 1;
//     min -= 1;
//     sec = 59;
//   } else if (sec < 10 && length.sec != 2) sec = '0' + sec;

//   $('.countdown').text(hour + ':' + min + ':' + sec);
//   if (hour == 0 && min == 0 && sec == 0)
//     clearInterval(timer),
//     $.get("/countdown-timer-message-twilio"), (res) => {
//       console.log(res)
//     };
    
//     //$('#alarm-alarm').prepend('href="/countdown-text/{{alarm}}"');
//     //document.getElementById("text-send").submit();
//     //return "ALARM";


// }, 1000);

// }) 



//Revision 2 : Fixes Weird Countdown issue where there is a -1, now getting issue with minute formatting when != 2 and then the hour. Need additional conditional statement 

$.get('/countdown.json', (res) => {
  console.log(res)


let duration = moment.duration({
	//'days': 1,
	'hours': res.hours, //0, //res.hours,
  'minutes': res.minutes, //0, //res.minutes,
  'seconds': 00

});

let timestamp = new Date(0, 0, 0, 0, 0, 0); //hr, min, sec for last three numbers.
let interval = 1; //dictates speed of the countdown. At 2, it'll countdown faster
let timer = setInterval(function() {
  timestamp = new Date(timestamp.getTime() + interval * 1000); //multiply by 1000 to correct for epoch time

  duration = moment.duration(duration.asSeconds() - interval, 'seconds'); //so at 59 seconds and interval at 1, it'll count down to 58, 57, etc.
  let hour = duration.hours(); //defining the variable at hours
  let min = duration.minutes();
  let sec = duration.seconds();

	//This is where the countdown is executed
  
  sec -= 1; 
  if (min < 0) return clearInterval(timer);
  if (min < 10 && min.length != 2) min = '0' + min;
  //Nested if Statement below
  if (sec < 0 && min != 0 && hour == 0) {
  	//hour -= 1;
    //min -= 1;
    sec = 59;
    if (min != 0){
    min -= 1;
    } 
    if (hour != 0) {
    hour -= 1;
    }
  } else if (sec < 10 && length.sec != 2) sec = '0' + sec;

  $('.countdown').text(hour + ':' + min + ':' + sec);
  if (hour == 0 && min == 0 && sec == 0)
    clearInterval(timer),
    $.get("/countdown-timer-message-twilio"), (res) => {
      console.log(res)
    };
    
    //$('#alarm-alarm').prepend('href="/countdown-text/{{alarm}}"');
    //document.getElementById("text-send").submit();
    //return "ALARM";


}, 1000);

}) 