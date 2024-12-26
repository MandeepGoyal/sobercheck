"""
Author: Mandeep Goyal
Date: 2024-12-23
Description: This project determines how sober are you and recomends quality food at the time.
"""

from flask import Flask, jsonify, request, render_template
import configparser
from openai import OpenAI
import json

# Initialize the Flask app
app = Flask(__name__)

# Load secrets
config = configparser.ConfigParser()
config.read("secrets.txt")

OPENAI_API_KEY = config["DEFAULT"]["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)
chat_log = [{"role": "system", "content": "You have to help for deveoping and project to add in the resume."}]


# Define a route for the home page
@app.route('/')
def home():
    return render_template("index.html")

def evaluate(questions, responses):
    chat_log.append({"role": "system", "content": "You will be given questions and some response, after that you need to evaluate for much the person is drunk on the scale of 1 to 10 and also yoou need to suggest a dish that the person should eat to decrease the hangover."})
    chat_log.append({"role": "system", "content": str(questions)})
    chat_log.append({"role": "system", "content": str(responses)})
    chat_log.append({"role": "system", "content": "Your response should only 2 things, first is a line as 'Your level of drunkness seems to be 8 out of 10. I suggest you to eat Rice', Now carefully understand that all the string format should be same, just change the number and the dish after calculating."})


    response = client.chat.completions.create(
        messages=chat_log,
        model="gpt-4o",
    )
    res = response.choices[0].message.content
    print("Response:",res)
    return res
    


questions = [
    {
        "question": "How many drinks have you had in the last hour?",
        "options": ["None", "1-2 drinks", "3 or more drinks"]
    },
    {
        "question": "Do you feel you have difficulty maintaining your balance?",
        "options": ["No difficulty", "Some difficulty", "Cannot maintain balance"]
    },
    {
        "question": "How easily can you focus on a task or conversation?",
        "options": ["Very easily", "With some effort", "Cannot focus at all"]
    },
    {
        "question": "Can you clearly differentiate between stationary and moving objects?",
        "options": ["Very clear", "Somewhat clear", "Not clear at all"]
    },
    {
        "question": "Do you feel the need to lie down because of dizziness?",
        "options": ["Not at all", "Sometimes", "Frequently"]
    }
]

@app.route('/submit_responses', methods=['POST'])
def submit_responses():
    user_responses = request.json.get('responses')
    print("User Responses:", user_responses)  # Log responses for debugging or processing
    
    # Process responses (e.g., call the LLM function)
    # Example: Call an LLM function with the responses
    result = evaluate(questions,user_responses)  # Replace with your actual LLM call
    
    # Return a response to the client
    return jsonify({"message": "Responses received!", "result": result})


@app.route('/play')
def play():
    # Pass the questions to the play.html template
    return render_template('play.html', questions=questions)


if __name__ == '__main__':
    app.run(debug=True)




"""
Make sure to be in proper working directory
python3 -m venv myenv
source myenv/bin/activate
deactivate
pip freeze > requirements.txt
pip install -r requirements.txt
"""