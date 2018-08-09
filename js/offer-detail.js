var urlParams = new URLSearchParams(location.search);

let form = document.getElementById('ride-form')
if (urlParams.has('id')) {
    fetch(`http:127.0.0.1:5000/api/v2/rides/${urlParams.get('id')}`, {
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
                    form.elements['price'].value = data.data.price
                    form.elements['seats_available'].value = data.data.seats_available
                    form.elements['date'].value = friendlyDate(data.data.date)
                    form.elements['time'].value = friendlyTime(data.data.time)
                    form.elements['driver'].value = data.data.driver
                    document.getElementById('ride-name').innerHTML = data.data.pickup + ' to ' + data.data.dropoff
                    document.getElementById('ride-status').innerText = ' ' + data.data.status
                    document.getElementById('ride-status-color').classList.add(statusColor(data.data.status))
                    form.elements['car'].value = data.data.car
                    console.log(data.data)
                });
            }
            else {
                res.json().then((data) => {
                    console.log(data)
                });
            }
        })
        .catch((err) => {
            console.log(err);
        });
}

function statusColor(status) {
    switch (status) {
        case 'In Offer':
            return 'green'
            break;
        case 'Started':
            return 'orange'
            break;
        case 'Done':
            return 'primary'
            break;
        default:
            return 'grey'
    }
}

// Requesting a ride offer
document.getElementById('request-ride').addEventListener('click', function(){
    if (urlParams.has('id')) {
        fetch(`http:127.0.0.1:5000/api/v2/rides/${urlParams.get('id')}/requests`, {
            method: "POST",
            mode: "cors",
            credentials: "same-origin",
            headers: {
                'Authorization': 'Bearer ' + access_token
            }
        })
        .then((res) => {
            if (res.status == 201) {
                res.json().then((data) => {
                    alert.classList.add('green')
                    alert.style.display = "block";
                    if (typeof (data.message) == 'object') {
                        for (var key in data.message) {
                            message.innerHTML = data.message[key];
                        }
                    } else {
                        message.innerHTML = data.message;
                    }
                   loadUpdatedRide()
                });
            }
            else {
                res.json().then((data) => {
                    alert.classList.add('red')
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
})

function loadUpdatedRide() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.response)
            form.elements['seats_available'].value = data.data.seats_available
        }
    };
    xhttp.open("GET", `http:127.0.0.1:5000/api/v2/rides/${urlParams.get('id')}`, true);
    xhttp.setRequestHeader('Authorization', `Bearer `+ access_token)
    xhttp.send();
}