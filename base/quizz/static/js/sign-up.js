(function () {

    const signupButton = document.querySelector('form button');
    signupButton.onclick = function () {
        const username = document.querySelector('form input[name="username"]').value;
        const password = document.querySelector('form input[name="password"]').value;
        const passwordConfirm = document.querySelector('form input[name="repassword"]').value;

        let errors = [];

        if (!/^[a-z0-9]{6,200}$/i.test(username)) {
            errors.push('Username must be min length 6 and only contains a-z, A-Z, 0-9');
        }
        if (!/^[a-z0-9]{6,200}$/i.test(password)) {
            errors.push('Password must be min length 6 and only contains a-z, A-Z, 0-9');
        }
        if (password !== passwordConfirm) {
            errors.push('Password and confirm password must be same');
        }
        if (errors.length > 0) {
            alert(errors.join('\n'));
            return false;
        }

        createUser(username, password)
            .then(function (res) {
                console.log(res);
            })
            .catch(function (err) {
                alert(err.message);
            });

        return false;
    }


})();


function createUser(username, password) {
    const url = '/api/users/create/';
    const data = {
        username: username,
        password: password
    };
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
        body: JSON.stringify(data)
    };
    return fetch(url, options)
        .then(response => response.json());
}