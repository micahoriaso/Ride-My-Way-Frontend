let access_token = localStorage.getItem('access-token')
let form = document.getElementById('profile')
fetch("http:127.0.0.1:5000/api/v2/users", {
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
                form.elements['first_name'].value = data.firstname
                form.elements['last_name'].value = data.lastname
                form.elements['email'].value = data.email
                form.elements['phone_number'].value = data.phone_number

                document.getElementById('user-name').innerText = data.fullname
                document.getElementById('user-profile-name').innerText = data.fullname
            });
        }
        else {
            res.json().then((data) => {
            });
        }
    })
    .catch((err) => {
    });

fetch("http:127.0.0.1:5000/api/v2/cars", {
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
                var table = '';
                for (var key in data.data) {
                    table += `
                        <tr>
                            <td class="bold"><a href="edit-car.html?registration=${data.data[key]['registration']}"> ${data.data[key]['model']} </a></td>
                            <td> ${data.data[key]['registration']} </td>
                            <td> ${data.data[key]['capacity']} </td>
                            <td><a href="#" id="delete-car" onclick = "deleteCar('${data.data[key]['registration']}')" class="grey button">Delete</a></td>
                        </tr >`
                }
                document.getElementById('car-table').innerHTML = table
            });
        }
        else {
            res.json().then((data) => {
            });
        }
    })
    .catch((err) => {
    });


function deleteCar(registration) {
    event.preventDefault();

    fetch("http:127.0.0.1:5000/api/v2/cars/" + registration, {
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
                    window.location = "profile.html";
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
    });