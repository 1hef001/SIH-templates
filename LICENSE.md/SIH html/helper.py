import pandas as pd
import datetime
import pytz
import json

def load_records(filename):
    records = pd.read_csv(filename)
    return records.to_dict()

def displayPresent(filename, uids):
    assert uids != None
    records = pd.read_csv(filename)
    return records.loc[records['UID'].isin(uids)].to_dict()

def assignAttendance(filename, uids):
    records = pd.read_csv(filename)
    # print(records)
    records = records.rename(columns={'Name' : 'name', 'Age' : 'age', 'Image' : 'image', 'UID' : 'id'})
    records = records.assign(attendance=["n"] * len(records["name"])) 
    records.loc[records['id'].isin(uids), 'attendance'] = ["y"] * len(records.loc[records['id'].isin(uids)]['attendance'])
    records.loc[records['id'].isin(uids), 'timestamp'] = [datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d-%m-%YT%H:%M:%S")] * len(records.loc[records['id'].isin(uids)]['attendance'])
    attendance_json = {}
    attendance_json["attendance"] = json.loads(records.to_json(orient='records'))
    attendance_json["cci"] = "someStringHere"           #reassign with cci code
    result_json = json.dumps(attendance_json, indent=4,  sort_keys=True)
    with open(r'./data/result.json', 'w') as f:
        f.write(result_json)

# print(load_records('students.csv', ['139AF']))

def visitJson(args):
    student_data = {'bio': 'SomeStringHere', 'visitData' : args}
    visit_json = json.dumps(student_data, indent=4, sort_keys=True)
    with open(r'./data/visit.json', 'w') as f:
        f.write(visit_json)