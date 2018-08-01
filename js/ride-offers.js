let access_token = localStorage.getItem('access-token')
var ridesGiven = fetch("http:127.0.0.1:5000/api/v2/rides", {
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
                var tableBody = '';
                for (var key in data.data) {
                    tableBody += '<tr>'
                    data.data[key]['owner'] ? 
                    tableBody += `<td class="bold"><a href="edit-ride.html?id=${data.data[key]['id']}">${data.data[key]['pickup']} to ${data.data[key]['dropoff']}</a></td>` :
                    tableBody += `<td class="bold"><a href="offer-detail.html?id=${data.data[key]['id']}">${data.data[key]['pickup']} to ${data.data[key]['dropoff']}</a></td>`
                    tableBody += `
                        <td>${friendlyTime(data.data[key]['time'])}</td>
                        <td><span class="${statusColor(data.data[key]['status'])} dot"></span> ${data.data[key]['status']} </td>
                        <td>${data.data[key]['driver']} </td>
                        <td>${data.data[key]['car']} </td>
                    `
                    tableBody += '</tr>'
                }
                document.getElementById('ride-table-body').innerHTML = tableBody
            });
        }
        else {
            res.json().then((data) => {
                alert.style.display = "block";
                alert.style.backgroundColor = "#f44336";
                message.innerHTML = data.message;
            });
        }
    })
    .catch((err) => {
        console.log(err);
    });


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
