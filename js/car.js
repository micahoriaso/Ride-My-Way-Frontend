let form = document.getElementById('car')
if (form) {
    form.addEventListener("submit", createCar);
}
function createCar(event) {
    event.preventDefault();

    fetch("http:127.0.0.1:5000/api/v2/cars", {
        method: "POST",
        mode: "cors",
        credentials: "same-origin",
        headers: {
            'Authorization': 'Bearer ' + access_token
        },
        body: new FormData(document.getElementById('car'))
    })
        .then((res) => {
            if (res.status == 201) {
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