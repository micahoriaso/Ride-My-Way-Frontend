var alert = document.getElementById('alert');
var message = document.getElementById('alert-message');

function closeAlert(){
    setTimeout(function () {
        alert.style.display = "none";
    }, 3000);
}