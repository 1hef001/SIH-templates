from flask import Flask, render_template, request, redirect, url_for, flash
from helper import load_records, assignAttendance, displayPresent, visitJson
import os
from facerecognition import init_video_record, close_recording

app = Flask(__name__)

# <--- Main --->
att_list = []
BOOL = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-attendance')
def init_start_attendance():
    global BOOL
    if BOOL == True:
        message = 'Face Recognition is already running'
    else:
        BOOL = True
        init_video_record()
        message = 'Face Recognition has started'
    
    flash(message)
    return redirect(url_for('index'))

@app.route('/stop-attendance')
def init_stop_attendance():
    global BOOL
    if BOOL == False:
        message = 'Face Recognition is not running'
    else:
        BOOL = False
        close_recording()
        message = 'Face Recognition was stopped'
    
    flash(message)
    return redirect(url_for('index'))


@app.route('/edit-attendance/', methods=['GET', 'POST'])
def init_edit_attendance():
    # print(name)
    student_record = load_records('students.csv')
    # print(student_record)
    return render_template('editAttendance.html', student_record=student_record, len=len(student_record['Name']))

@app.route('/edit-attendance/submit', methods=['GET', 'POST'])
def submit_attendance():
    global att_list
    att_list = request.args.getlist('attendance')
    records = displayPresent('students.csv', uids=att_list)
    assignAttendance('students.csv', uids=att_list)
    # returnJson('students.csv', att_list)
    return render_template('attendance.html', student_record=records, len=len(records['Name']))

@app.route('/schedule-visit/', methods=['GET', 'POST'])
def init_schedule_visit():
    return render_template('visitForm.html')

@app.route('/schedule-visit/confirm', methods=['GET', 'POST'])
def schedule_visit():
    args = request.args.to_dict()
    visitJson(args)
    flash('Visit Scheduled')
    return redirect(url_for('index'))

def main():
    app.secret_key = os.urandom(24)
    app.run(port=5000, debug=True)

if __name__ == "__main__":
    main()