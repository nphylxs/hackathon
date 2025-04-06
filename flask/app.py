from flask import Flask, render_template, url_for, request, jsonify
import csv
import os
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

DATA_FILE = 'schedule.json'

# Helper to load schedule data
def load_schedule():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

# Helper to save schedule data
def save_schedule(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/schedule')
def schedule():
    schedule = load_schedule()
    return render_template('schedule.html', schedule=schedule)

@app.route('/add', methods=['POST'])
def add_schedule():
    try:
        data = request.get_json()  # Get the incoming JSON data
        
        # If the schedule file exists, append to it, else create a new file
        try:
            with open(DATA_FILE, 'r') as file:
                schedule = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            schedule = []

        # Append the new schedule item to the list
        schedule.append(data)

        # Save the updated schedule back to the file
        with open(DATA_FILE, 'w') as file:
            json.dump(schedule, file, indent=4)
        
        return jsonify({"message": "Schedule saved successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/load', methods=['GET'])
def load_items():
    schedule = load_schedule()
    return jsonify(schedule)

if __name__ == '__main__':
    app.run(debug=True)

    


