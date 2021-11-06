(function () {
    const buttonLogin = document.getElementById('btnLogin');
    buttonLogin.onclick = function () {
        const username = document.querySelector('[name=username]').value;
        const password = document.querySelector('[name=password]').value;

        if (!username || !password) {
            alert('Username and password is required')
            return false;
        }

        const data = {
            username: username,
            password: password
        };

        sendRequest('/api/auth/login/', data, 'POST')
            .then(function (res) {
                if (res.data) {
                    window.location.href = '/';
                } else {
                    alert(res.message);
                }
            })
            .catch(function (err) {
                console.log(err);
            });

        return false;
    }
})();