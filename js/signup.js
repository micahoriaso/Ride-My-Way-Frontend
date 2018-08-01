let signupform = document.getElementById("signup");
if (signupform) {
    signupform.addEventListener("submit", signup);
}

function signup(event) {
    event.preventDefault();

    fetch("http:127.0.0.1:5000/api/v2/auth/signup", {
        method: "POST",
        mode: "cors",
        credentials: "same-origin",
        body: new FormData(document.getElementById('signup'))
    })
    .then((res) => {
        if (res.status == 201) {
            res.json().then((data) => {
                localStorage.removeItem('access-token');
                localStorage.setItem('access-token', data.access_token);
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