flatpickr("#ride-date", {});
flatpickr("#ride-time", {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
});

let newRideForm = document.getElementById("ride-form");

if (newRideForm) {
    newRideForm.addEventListener("submit", createRide);
}

function createRide(event) {
    event.preventDefault();

    fetch("http:127.0.0.1:5000/api/v2/rides", {
        method: "POST",
        mode: "cors",
        credentials: "same-origin",
        body: new FormData(document.getElementById('ride-form')),
        headers: {
            'Authorization': 'Bearer ' + access_token
        }
    })
        .then((res) => {
            if (res.status == 201) {
                res.json().then((data) => {
                    window.location = "ride-offers.html";
                });
            }
            else {
                res.json().then((data) => {
                    alert.style.display = "block";
                    if (typeof (data.message) == 'object') {
                        for (var key in data.message) {
                            message.innerHTML = data.message[key];
                        }
                    } else {
                        message.innerHTML = data.message;
                    }
                });
            }
        })
        .catch((err) => {
            console.log(err);
        });
}