import $ from 'jquery';
import 'popper.js';
import 'bootstrap';

var alerts = $(".alert");

for (let i = 0; i < alerts.length; i++) {
    setTimeout(function () {
        $("#" + alerts[i].id).fadeOut('slow');
    }, 5000);
    alerts[i].addEventListener("click", () => {
        $("#" + alerts[i].id).remove();
    });
}

