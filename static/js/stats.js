//--import {app_state} from 'app_state';
//--import {inject, singleton} from 'aurelia-dependency-injection';
//--import {AppRouter} from 'aurelia-router';
//--import {Router} from 'aurelia-router';
//--import moment from '//cdn.jsdelivr.net/momentjs/latest/moment.min.js';
//--import daterangepicker from '//cdn.jsdelivr.net/bootstrap.daterangepicker/2/daterangepicker.js';
//--import {json} from 'aurelia-fetch-client';
import 'fetch';



  activate() {
  }

  //data_request(games) {

    //this.loaderSpin = true;

   // this.http.fetch('stats_req', {
     //    method: "POST",
       //  body: JSON.stringify({"games":games, "start_date":this.start_Date, "end_date":this.end_Date})
         //}).then(response => response.json())
    //.then(req_data => this.req_data = req_data)
    //.then(response => this.loaderSpin = false);

    //console.log("games: " + games);
    //console.log("startDate " + this.start_Date);
    //console.log("endDate " + this.end_Date);

  //}


  attached() {
    console.log('----- date range picker');

    $(function() {
      var button = $("#prevData"),
      submitButt = $("#dwnldData");
      button.on("click",function(e) {
         submitButt.prop("disabled",false); // NOT a toggle
      });
    });

    var start = moment().subtract(31, 'days');
    var end = moment();
    var dataSet = this.req_data;

    function cb(start, end) {
        $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    }

    $('#reportrange').daterangepicker({
        startDate: start,
        endDate: end,
        minDate: start,
        ranges: {
           'Today': [moment(), moment()],
           'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
           'Last 7 Days': [moment().subtract(6, 'days'), moment()],
           'Last 30 Days': [moment().subtract(29, 'days'), moment()],
           'This Month': [moment().startOf('month'), moment().endOf('month')],
           'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    }, cb);

    cb(start, end);

    $('#reportrange').on('apply.daterangepicker', (ev, picker) => {
      this.start_Date=String(picker.startDate.format('YYYY-MM-DD'));
      this.end_Date=String(picker.endDate.format('YYYY-MM-DD'));
      });

  }

}