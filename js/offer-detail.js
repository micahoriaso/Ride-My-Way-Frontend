var urlParams = new URLSearchParams(location.search);

let access_token = localStorage.getItem('access-token')
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