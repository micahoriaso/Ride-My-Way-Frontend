function friendlyDate(date){
    friendly_date = new Date(date)
    return friendly_date.toDateString()
}

function friendlyTime(time){
    friendly_time = new Date('1970-01-01T' + time)
    return friendly_time.toLocaleTimeString()
}

// get current user details
let access_token = localStorage.getItem('access-token')
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
                if (document.getElementById('user-profile-name')){
                    document.getElementById('user-profile-name').innerText = data.fullname
                }
            });
        }
        else {
            res.json().then((data) => {
            });
        }
    })
    .catch((err) => {
    });

// Toggle display of profile menu 
let profile_caret = document.getElementById('profile-caret')
let dropdown_content = document.getElementById("dropdown-content");
dropdown_content.style.display = "none"

profile_caret.addEventListener('click', function () {
    if (dropdown_content.style.display === "none") {
        dropdown_content.style.display = "block";
        profile_caret.style.transform = 'rotate(180deg)'
    } else {
        profile_caret.style.transform = 'rotate(360deg)'
        dropdown_content.style.display = "none";
    }
})