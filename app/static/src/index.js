import $ from '../node_modules/jquery';

var alerts = $(".alert");

for (let i = 0; i < alerts.length; i++) {
    setTimeout(function () {
        $("#" + alerts[i].id).fadeOut('slow');
    }, 5000);
}
