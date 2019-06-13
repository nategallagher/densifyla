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

var spinners = $(".spinner-border");

for (let i = 0; i < spinners.length; i++){
    youThere(spinners[i].dataset.address, spinners[i].dataset.userid, spinners[i].id, null);
    let intervalHandle = setInterval(function () {
        youThere(spinners[i].dataset.address, spinners[i].dataset.userid, spinners[i].id, intervalHandle)
    }, 5000);
}

function youThere(addressString, userId, spinnerId, handle) {
    // sends request to server to see if report exists for corresponding address string
    $.get('/reports/' + userId + '/' + addressString, function (data) {
        if (data['report_file_exists']){
            $("#" + spinnerId).remove();
            $("#" + spinnerId + "_links").css('display', 'block');
            if (handle != null) {
                clearInterval(handle);
            }
        }
    });
}
