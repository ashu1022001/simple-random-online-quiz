from flask import Flask, json
from flask import send_from_directory, request
import requests
import random

answers = {
    'q1': 'Yes'
}

questions = [
    {
        'questionId': 'q1',
        'question': 'IS python a case sensitive language?',
        'options': [
            'Yes',
            'No',
            'Machine dependent',
            'None'
        ]
    }
]

questionsUrl = 'https://opentdb.com/api.php?amount=10&category=18&difficulty=medium&type=multiple'


def init_db_questions():
    # sending get request and saving the response as response object 
    r = requests.get(url = questionsUrl) 
  
    # extracting data in json format 
    questionsResponse = r.json()
    prepare_quiz(questionsResponse['results'])
    
def prepare_quiz(quizQuestions = []):
    global questions
    global answers
    questions = []
    answers = {}
    questionCount = 1
    for quizQuestion in quizQuestions:
        options = quizQuestion['incorrect_answers']
        options.append(quizQuestion['correct_answer'])
        random.shuffle(options)
        questions.append({
            'questionId': 'q' + str(questionCount),
            'question': quizQuestion['question'],
            'options': options
        })
        answers['q' + str(questionCount)] = quizQuestion['correct_answer']
        questionCount = questionCount + 1
    print(questions)


api = Flask(__name__)
api.config['RESULT_STATIC_PATH'] = "templates/"



@api.route('/')
def root():
    init_db_questions()
    return send_from_directory(api.config['RESULT_STATIC_PATH'], 'index.html')

@api.route('/assets/js/<path:filename>')  
def send_js_file(filename):  
      return send_from_directory('assets/js/', filename)

@api.route('/assets/css/<path:filename>')  
def send_css_file(filename):  
      return send_from_directory('assets/css/', filename)

@api.route('/questions', methods=['GET'])
def get_questions():
  response = api.response_class(
        response=json.dumps(questions),
        status=200,
        mimetype='application/json',
    )
  response.headers['Access-Control-Allow-Origin'] = '*'
  response.headers['Access-Control-Allow-Methods'] = '*'
  response.headers['Access-Control-Allow-Headers'] = '*'
  return response


@api.route('/result', methods=['POST'])
def get_result():
    score = 0
    results = []
    userSelections = request.json['data']
    for question in userSelections: 
        if answers[question['questionId']] == question['answer']:
            score = score + 1
            results.append(True)
        else:
            results.append(False)
    return {
        'score': score,
        'results': results
    }



if __name__ == '__main__':
    api.run()