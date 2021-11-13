function createQuestionItem(data = []) {
    let answers = '';
    data.choices.forEach(ans => {
        answers += `<div class="answer-item">
                        <input ${ans.id === data.myChoice ? 'checked' : ''} disabled type="radio">
                        <label class="m-2">${ans.context}</label>
                    </div>`;
    })

    const result = `<div class="question-item ${data.correct ? 'correct' : 'incorrect'}">
                        <div class="question-context">
                            <span>${data.context}</span>
                        </div>
                        <div class="answers">
                            ${answers}
                        </div>
                    </div>`;
    return result;
}

function chart(data = {}) {
    const ctx = document.querySelector('#chart .line-chart');
    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
              label: 'Time per question (miliseconds)',
              data: data.data,
              fill: false,
              borderColor: 'rgb(75, 192, 192)',
              tension: 0.1
            }]
        }
    });
}

(function () {
    const detailsDiv = document.getElementById('details');
    const data = detailsDiv.innerText;
    detailsDiv.remove();
    const details = JSON.parse(data);
    console.log(details);
    const chartData = {
        labels: [],
        data: []
    }
    const questions = document.querySelector('.history-area .questions');
    details.forEach((item, index) => {
        questions.innerHTML += createQuestionItem(item);
        chartData.labels.push('Q' + (index + 1));
        chartData.data.push(item.time);
    })
    chart(chartData);
})();

