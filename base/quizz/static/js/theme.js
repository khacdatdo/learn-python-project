function userMenuToggle() {
    const userMenu = document.querySelector('.userMenu .user-menu');
    userMenu.classList.toggle('active');
}

function homepage() {
    window.location.href = '/';
}

class Button {
    constructor(button) {
        this.button = button;
        this.html = button.innerHTML;
        this.isLoading = false;
    }

    setLoading(isLoading) {
        this.isLoading = isLoading;
        if (isLoading) {
            this.button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            this.setDisabled(true);
        } else {
            this.setDisabled(false);
            this.button.innerHTML = this.html;
        }
    }

    setDisabled(isDisabled) {
        this.button.disabled = isDisabled;
    }
}