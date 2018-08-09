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
                form.elements['firstname'].value = data.firstname
                form.elements['lastname'].value = data.lastname
                form.elements['email'].value = data.email
                form.elements['phone_number'].value = data.phone_number
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

let saveButton = document.getElementById("save");
if (saveButton) {
    saveButton.addEventListener("click", editProfile);
}

function editProfile(event) {
    event.preventDefault();
    fetch("http:127.0.0.1:5000/api/v2/users", {
        method: "PUT",
        mode: "cors",
        credentials: "same-origin",
        body: new FormData(document.getElementById('profile')),
        headers: {
            'Authorization': 'Bearer ' + access_token
        }
    })
        .then((res) => {
            if (res.status == 200) {
                res.json().then((data) => {
                    console.log(data)
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
            console.log(err);
        });
}