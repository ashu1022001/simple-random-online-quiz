function getQuestions() {
    $.ajax({url: "http://localhost:5000/questions", success: function(result){
        renderQuestions(result);
      }});
}


function renderQuestions(questions) {
    const container = $('#quiz-container');
    console.log(container);
    let questionCount = 1;
    for (const question of questions) {
        let optionsHTML = '';
        let optionsCount = 1;
        for (const option of question.options) {
            optionsHTML += `
            <label class="quiz-form__ans" for="${question.questionId}-${optionsCount}">
            <input type="radio" name="${question.questionId}" id="${question.questionId}-${optionsCount}" value="${option}" />
            <div class="design"></div>
            <span class="text">${option}</span>
            </label>`;
            optionsCount++;
        }

        container.append(`
            <div class="quiz-form__quiz">
                <p class="quiz-form__question">
                ${questionCount}. ${question.question}
                </p>
                ${optionsHTML}
            </div>
        `);
        questionCount++;
    }
}


function submitQuiz(event) {
    const checkedRadios = document.querySelectorAll('input[type="radio"]:checked');
    const userSelections = Array.from(checkedRadios || []).map((radio) => {
        return {
            questionId: radio.name,
            answer: radio.value
        };
    });
    jQuery.ajax({
        url: 'http://localhost:5000/result',
        type: "POST",
        contentType:"application/json",
        dataType: "json",
        data: JSON.stringify({ data: userSelections}),
        success: function(result){
            showResults(result);
            M.Modal.getInstance(document.querySelector('#resultModal')).open();
      }});
      event.preventDefault();
}

function showResults(results) {
    const resultContainer = $('#results-container');
    let resultHtml = '';
    let questionCount = 1;
    for (const result of results.results) {
        resultHtml += `
            <span>${questionCount})&nbsp; ${result ? 'Right' : 'Wrong'}</span>
            <br/>
        `;
        questionCount++;
    }
    resultHtml += `
        <p>Score: ${results.score}</p>
    `;
    resultContainer.append(resultHtml);
}

function restart() {
    window.location.reload();
}

$(document).ready(function(){
    $('.modal').modal();
});