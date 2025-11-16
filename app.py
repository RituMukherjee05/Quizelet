from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend is running!"

quizzes = {
    "dbms": [
        {
            "question": "Which of the following is used to uniquely identify a record in a table?",
            "options": ["Foreign key", "Primary key", "Candidate key", "Alternate key"],
            "answer": "Primary key"
        }
    ]
}

@app.route("/api/subjects")
def get_subjects():
    return jsonify(list(quizzes.keys()))

@app.route("/api/quiz/<subject>")
def get_quiz(subject):
    subject = subject.lower()
    quiz = quizzes.get(subject)
    if quiz:
        safe_quiz = [
            {
                "id": idx,
                "question": q["question"],
                "options": q["options"]
            }
            for idx, q in enumerate(quiz)
        ]
        return jsonify(safe_quiz)
    return jsonify({"error": "Subject not found"}), 404

@app.route("/api/check_answer/<subject>/<int:q_id>", methods=["POST"])
def check_answer(subject, q_id):
    user_answer = request.args.get("answer")
    correct_answer = quizzes[subject][q_id]["answer"]
    return jsonify({
        "is_correct": user_answer == correct_answer,
        "correct_answer": correct_answer
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
