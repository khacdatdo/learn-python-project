(function () {
    initOptions();
    initEvent();

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
        addQuestion(questions.data);

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
            const question = document.querySelector('.question-item:first-child');
            question.classList.add('active', 'animate__fadeIn');
            setTimeout(() => {
                temp.remove();
                setQuestionCurrentCount();
                $('body').trigger('timestart');
            }, 500);
        }
    }, 1000);
}

function addQuestion(data) {
    let questions = ""
    data.forEach(q => {
        let answers = ``;
        q.choices.forEach(c => {
            answers += `<div class="col-md-3 p-2">
                            <div answer-id="${c.id}" correct="${c.is_correct_answer}" class="block p-4 answer-item animate__animated">
                                <span class="answer-context">${c.context}</span>
                            </div>
                        </div>`;
        });
        questions += `<div question-id="${q.id}" class="question-item animate__animated">
                        <div class="question-context-container row justify-content-center p-4">
                            <span class="question-context">${q.context}</span>
                        </div>
                        <div class="answers row justify-content-center">
                            ${answers}
                        </div>
                    </div>`;
    });
    $('.playing .questions').empty().append(questions);
    addEventAnswer();
}

function initEvent() {
    window.customEvent = {};
    window.customEvent.progress = null;
    window.customEvent.score = 0;
    localStorage.setItem('game_data', JSON.stringify([]));

    $('body').on('timestart', function () {
        window.customEvent.progressStartTime = new Date();
        console.log('timestart');
        if (window.customEvent.progress) {
            clearInterval(window.customEvent.progress);
        }
        let time = 20000;
        let count = 0;
        let step = 100;
        window.customEvent.progress = setInterval(() => {
            if (count * step >= time) {
                clearInterval(window.customEvent.progress);
                const data = JSON.parse(localStorage.getItem('game_data'));
                const question = {};
                question.id = $('.question-item.active').attr('question-id');
                question.context = $('.question-item.active').find('.question-context').text();
                question.choices = [];
                $('.question-item.active .answer-item').each(function () {
                    const choice = {};
                    choice.id = $(this).attr('answer-id');
                    choice.context = $(this).find('.answer-context').text();
                    choice.is_correct_answer = $(this).attr('correct') === 'true';
                    question.choices.push(choice);
                });
                question.myChoice = null;
                question.correct = false;
                question.time = getTime();
                data.push(question);
                localStorage.setItem('game_data', JSON.stringify(data));
                $('body').trigger('showresult');
            }
            setProgress((count * step) * 100 / time);
            count++;
        }, step);
    })

    $('body').on('showresult', function () {
        console.log('showresult');
        if (window.customEvent.progress) {
            clearInterval(window.customEvent.progress);
        }
        $('.question-item.active .answer-item').each(function () {
            $(this).off('click');
            if ($(this).attr('correct') === 'true') {
                $(this).addClass('animate__flash animate__fast');
            } else {
                $(this).addClass('animate__fadeOut animate__faster');
            }
        });
        setTimeout(function () {
            nextQuestion();
        }, 3000);
    });

    $('body').on('sendresult',async function () {
        console.log('sendresult');
        const data = JSON.parse(localStorage.getItem('game_data'));
        console.log(data);
        showAllDone();
        await wait(1000);
        sendRequest('/api/history/', data, 'POST').then(async (res) => {
            console.log(res);
            await wait(1000);
            window.location.href = '/summary/' + res.data;
        });
    })
}

function nextQuestion() {
    const currentQuestion = $('.question-item.active');
    if (currentQuestion && currentQuestion.next().length > 0) {
        $('body').trigger('timestart');
        currentQuestion.removeClass('active');
        currentQuestion.next().addClass('active animate__fadeIn');
        setQuestionCurrentCount();
    } else {
        $('body').trigger('sendresult');
    }
}

function addEventAnswer() {
    $('.answer-item').one('click', function () {
        const data = JSON.parse(localStorage.getItem('game_data'));
        const question = {};
        question.id = $(this).parent().parent().parent().attr('question-id');
        question.context = $(this).parent().parent().parent().find('.question-context').text();
        question.choices = [];
        question.myChoice = $(this).attr('answer-id');
        question.correct = $(this).attr('correct') === 'true';
        $(this).parent().parent().find('.answer-item').each(function () {
            const choice = {};
            choice.id = $(this).attr('answer-id');
            choice.context = $(this).find('.answer-context').text();
            choice.is_correct_answer = $(this).attr('correct') === 'true';
            question.choices.push(choice);
            if (question.myChoice === choice.id && choice.is_correct_answer) {
                setCorrectedCount();
            }
        });
        question.time = getTime();
        data.push(question);
        localStorage.setItem('game_data', JSON.stringify(data));
        $('body').trigger('showresult');
    });
}

function getTime() {
    if (window.customEvent.progressStartTime) {
        const time = new Date() - window.customEvent.progressStartTime;
        return time;
    }
    return 0;
}

function setProgress(percent) {
    document.querySelector('.progress').style.width = `${percent}%`;
}

function setCorrectedCount() {
    document.querySelector('.game-info .score span').innerHTML = ++window.customEvent.score;
}

function setQuestionCurrentCount() {
    let temp = $('.question-item').length;
    $('.question-item').each(function (index) {
        if ($(this).hasClass('active')) {
            document.querySelector('.game-info .count span').innerText = `${index + 1}/${temp}`;
        }
    });
}

function showAllDone() {
    document.querySelector('.playing').classList.add('animate__slideOutLeft')
    document.querySelector('.after-play').classList.add('animate__slideInRight', 'active');
}

function wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
