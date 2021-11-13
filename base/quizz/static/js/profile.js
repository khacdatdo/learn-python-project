(function () {
    document.getElementById('btnChangePassword').onclick = function () {
        const old_password = document.querySelector('[name=old_password]').value;
        const new_password = document.querySelector('[name=new_password]').value;
        const confirm_password = document.querySelector('[name=confirm_password]').value;
        if (!old_password || !new_password || !confirm_password) {
            alert('Please fill all fields');
            return false;
        }
        if (new_password !== confirm_password) {
            alert('Password not match');
            return false;
        }
        changePassword({
            old_password,
            new_password
        }).then(function (res) {
            alert(res.message);
            window.location.reload();
        }).catch(function (res) {
            alert(res.message);
        });

        return false;
    }
})();


function changePassword(data) {
    return sendRequest('/api/auth/change-password/', data, 'POST').then(res => {
        if (res.errors) throw res;
        return res;
    });
}