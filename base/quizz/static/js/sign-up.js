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

        sendRequest('/api/users/', {
            username, password
        }, 'POST')
            .then(function (res) {
                if (res.data) {
                    alert(res.message);
                    window.location.href = '/';
                } else {
                    alert(res.message);
                }
            })
            .catch(function (err) {
                alert(err.message);
            });

        return false;
    }


})();