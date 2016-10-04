import {app_state} from 'app_state';
import {inject, singleton} from 'aurelia-dependency-injection';
import {AppRouter} from 'aurelia-router';
import {Router} from 'aurelia-router';
import moment from 'CATR/moment';
import daterangepicker from 'CATR/daterangepicker';
import {json} from 'aurelia-fetch-client';


@inject(app_state, AppRouter)
@singleton()
export class catr {

  static inject() { return [Router]; }

  constructor(app_state, router) {
    this.app_state = app_state;
    this.router = router;
    this.start_Date = moment().subtract(31, 'days').format('YYYY-MM-DD');
    this.end_Date = moment().format('YYYY-MM-DD');
    this.loaderSpin = false;
  }

  activate() {
  }

  data_request(acct_id) {

    this.loaderSpin = true;

    this.app_state.http.fetch('catr_req', {
         method: "POST",
         body: JSON.stringify({"acct_id":acct_id, "start_date":this.start_Date, "end_date":this.end_Date})
         }).then(response => response.json())
    .then(req_data => this.req_data = req_data)
    .then(response => this.loaderSpin = false);

    console.log("acct_id: " + acct_id);
    console.log("startDate " + this.start_Date);
    console.log("endDate " + this.end_Date);

  }

  downloadFile(acct_id) {

    console.log("acct_id: " + acct_id);
    console.log("startDate " + this.start_Date);
    console.log("endDate " + this.end_Date);

    var csvContent = "No.,Account Number,DB/CR,Amount,Date,Transaction Code,Transaction Description,\n";

    var submitButt = $("#dwnldData");
    submitButt.prop("disabled",true); // NOT a toggle

    this.req_data.forEach(row => {
    csvContent = csvContent + row.Counter + ',' + row.ACCT_NUM + ',' + row.DEBIT_CR_TYPE_CD + ',' + row.TRXN_AMT_ADJUSTED  + ',' + row.TRXN_DT  + ',' + row.FIN_TRXN_TYPE_CD  + ',' + row.FIN_TRXN_TYPE_DESC + '\n';
    });

    this.export(csvContent);

  }
  export(text) {
    var pom = document.createElement('a');
    pom.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    pom.setAttribute('download', 'export.csv');
    pom.style.display = 'none';
    document.body.appendChild(pom);
    pom.click();
    document.body.removeChild(pom);
  }
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