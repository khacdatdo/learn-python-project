(function () {
    initOptions();

    const btnPlay = document.getElementById('btnPlay');
    btnPlay.onclick = async () => {
        const btn = new Button(btnPlay);
        btn.setLoading(true);
        const language = document.querySelector('select[name="language"]').value;
        const category = document.querySelector('select[name="category"]').value;
        const level = document.querySelector('select[name="level"]').value;
        const filter = {
            language,
            category,
            level
        }
        const questions = await getQuestions(filter);
        console.log(questions);

        btn.setLoading(false);
        play();
        return false;
    }
})();

function initOptions() {
    const params = new URLSearchParams(window.location.search);
    language = params.get('language');
    category = params.get('category');
    level = params.get('level');
    if (language) {
        document.querySelector('select[name="language"]').value = language;
    }
    if (category) {
        document.querySelector('select[name="category"]').value = category;
    }
    if (level) {
        document.querySelector('select[name="level"]').value = level;
    }
}

function getQuestions(filter) {
    const url = `/api/questions/?${Object.keys(filter).map(key => `${key}=${filter[key]}`).join('&')}`;
    return fetch(url).then(response => response.json());
}

function play() {
    document.querySelector('.before-play').classList.add('animate__slideOutLeft')
    document.querySelector('.playing').classList.add('animate__slideInRight', 'active');
    const countDownTime = 5;
    let countDown = countDownTime;
    const interval = setInterval(() => {
        countDown--;
        document.querySelector('.countdown').innerHTML = countDown;
        if (countDown <= 0) {
            clearInterval(interval);
            const temp = document.querySelector('.getting-started');
            temp.classList.add('animate__fadeOut')
            setTimeout(() => {
                temp.remove();
            }, 500);
        }
    }, 1000);
}

function hideQuestion(ques_container) {

}

function setProgress(percent) {
    document.querySelector('.progress').style.width = `${percent}%`;
}