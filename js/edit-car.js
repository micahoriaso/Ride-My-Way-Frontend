let access_token = localStorage.getItem('access-token')
let form = document.getElementById('car')
if (form) {
    form.addEventListener("submit", createCar);
}

var urlParams = new URLSearchParams(location.search);
if (urlParams.has('registration')) {
    urlParams.get('registration');
    fetch("http:127.0.0.1:5000/api/v2/cars/" + urlParams.get('registration'), {
        method: "GET",
        mode: "cors", 
        credentials: "same-origin",
        headers: {
            'Authorization': 'Bearer ' + access_token
        }
    })
    .then((res) => {
        if (res.status == 200) {
            res.json().then((data) => {
                form.elements['registration'].value = data.data.registration
                form.elements['model'].value = data.data.model
                form.elements['capacity'].value = data.data.capacity
            });
        }
        else {
            res.json().then((data) => {
            });
        }
    })
    .catch((err) => {
        console.log(err);
        });
}



function createCar(event) {
    event.preventDefault();

    fetch("http:127.0.0.1:5000/api/v2/cars/" + urlParams.get('registration'), {
        method: "PUT",
        mode: "cors", 
        credentials: "same-origin",
        headers: {
            'Authorization': 'Bearer ' + access_token
        },
        body: new FormData(document.getElementById('car'))
    })
    .then((res) => {
        if (res.status == 200) {
            res.json().then((data) => {
                window.location = "profile.html";
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