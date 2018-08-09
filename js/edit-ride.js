flatpickr("#ride-date", {});
flatpickr("#ride-time", {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
});

var urlParams = new URLSearchParams(location.search);

let form = document.getElementById('ride-form')
if (urlParams.has('id')) {
    fetch("http:127.0.0.1:5000/api/v2/rides/" + urlParams.get('id'), {
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
                    var options = ''
                    for (var key in data.data.status_options) {
                        options += '<option value=\'' + data.data.status_options[key] + '\'> ' + data.data.status_options[key] + ' </option>'
                    }
                    document.getElementById('status_options').innerHTML = options

                    form.elements['price'].value = data.data.price
                    form.elements['date'].value = data.data.date
                    form.elements['time'].value = data.data.time
                    form.elements['pickup'].value = data.data.pickup
                    form.elements['dropoff'].value = data.data.dropoff
                    document.getElementById('status_options').value = data.data.status
                    document.getElementById('ride-name').innerHTML = data.data.pickup + ' to ' + data.data.dropoff
                    document.getElementById('ride-status').innerText = ' ' + data.data.status
                    document.getElementById('ride-status-color').classList.add(statusColor(data.data.status))
                    console.log(data.data.requests.data)
                    var tableBody = '';
                    for (key in data.data.requests.data){
                        console.log(data.data.requests.data[key])
                        tableBody += `
                        <tr>
                            <td> ${data.data.requests.data[key]['requestor']} </td>
                            <td> ${data.data.requests.data[key]['request_status']} </td>
                            <td>
                                <a href="#" id="accept-request" onclick = "acceptRequest('${data.data.requests.data[key]['id']}')" class="green button">Accept</a>
                                <a href="#" id="decline-request" onclick = "declineRequest('${data.data.requests.data[key]['id']}')" class="red button">Decline</a>
                            </td>
                        </tr >`
                    }
                    document.getElementById('request-table-body').innerHTML = tableBody

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

let saveButton = document.getElementById("save");
if (saveButton) {
    saveButton.addEventListener("click", editRide);
}
function editRide(event) {
    event.preventDefault();
    fetch("http:127.0.0.1:5000/api/v2/rides/" + urlParams.get('id'), {
        method: "PUT",
        mode: "cors", 
        credentials: "same-origin", 
        body: new FormData(document.getElementById('ride-form')),
        headers: {
            'Authorization': 'Bearer ' + access_token
        }
    })
        .then((res) => {
            if (res.status == 200) {
                res.json().then((data) => {
                    console.log(data)
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

function deleteRide() {
    event.preventDefault();

    fetch("http:127.0.0.1:5000/api/v2/rides/" + urlParams.get('id'), {
        method: "DELETE",
        mode: "cors", 
        credentials: "same-origin", 
        headers: {
            'Authorization': 'Bearer ' + access_token
        }
    })
        .then((res) => {
            if (res.status == 200) {
                res.json().then((data) => {
                    window.location = "ride-offers.html";
                });
            }
            else {
                res.json().then((data) => {
                    alert.style.display = "block";
                    message.innerHTML = data.message;
                });
            }
        })
        .catch((err) => {
        });
}

function acceptRequest(request_id) {
    event.preventDefault();
    var request_status = { request_status:'Accepted' }
    fetch(`http:127.0.0.1:5000/api/v2/rides/${urlParams.get('id')}/requests/${request_id}`, {
        method: "PUT",
        mode: "cors", 
        credentials: "same-origin", 
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token
        },
        body: JSON.stringify(request_status)
    })
        .then((res) => {
            if (res.status == 200) {
                res.json().then((data) => {
                    console.log(data)
                    // window.location = "ride-offers.html";
                });
            }
            else {
                res.json().then((data) => {
                    console.log(data)
                    // alert.style.display = "block";
                    // message.innerHTML = data.message;
                });
            }
        })
        .catch((err) => {
        });
}

function declineRequest(request_id) {
    event.preventDefault();
    var request_status = { 'request_status': 'Declined'}
    fetch(`http:127.0.0.1:5000/api/v2/rides/${urlParams.get('id')}/requests/${request_id}`, {
        method: "PUT",
        mode: "cors", 
        credentials: "same-origin", 
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token
        },
        body: JSON.stringify(request_status)
    })
        .then((res) => {
            if (res.status == 200) {
                res.json().then((data) => {
                    console.log(data)
                    // window.location = "ride-offers.html";
                });
            }
            else {
                res.json().then((data) => {
                    console.log(data)
                    // alert.style.display = "block";
                    // message.innerHTML = data.message;
                });
            }
        })
        .catch((err) => {
        });
}