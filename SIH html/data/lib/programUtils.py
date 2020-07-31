import pandas as pd
import datetime
import json
import requests
import shutil




# API functions

class FetchAPIData:
    __base_api = 'https://asia-east2-eudaemon-20a5e.cloudfunctions.net/api'

    def __init__(self, cci_id):
        self.get_children_data(cci_id)
        self.get_pix()
        self.set_attendance_template()

    def get_children_data(self, cci_id):
        __api_endpoint = '/attendance/children?cci=' + cci_id
        response = requests.get(self.__base_api + __api_endpoint)
        response_json = response.json()
        df = pd.DataFrame(response_json['result'])
        df.to_csv('./data/assets/cache/student_data.csv')

    def get_pix(self):
        df = pd.read_csv('./data/assets/cache/student_data.csv')
        for url in df['photo']:
            filename = df.loc[df['photo'] == url, 'name'].to_string().split()[1]
        
        with open('./data/assets/'+ filename + '.jpg', 'wb') as pic:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, pic)
            else:
                raise ValueError('Couldn\'t Establish secure connection')
            
    def set_attendance_template(self):
        df = pd.read_csv('./data/assets/cache/student_data.csv')
        attendance_df = df[['name', 'age', 'id']]
        attendance_df = attendance_df.assign(image='../assets/' + df['name'] + '.jpg')
        attendance_df.to_csv('./data/bin/attendance_template.csv')


# attendance and process functions

class Attendance:

    __base_api = 'https://asia-east2-eudaemon-20a5e.cloudfunctions.net/api'


    def __init__(self):
        pass

    @staticmethod    
    def load_records():
        records = pd.read_csv('./data/bin/attendance_template.csv')
        return records.to_dict()

    @staticmethod
    def displayPresent(uids):
        assert uids != None
        records = pd.read_csv('./data/bin/attendance_template.csv')
        return records.loc[records['id'].isin(uids)].to_dict()

    @staticmethod
    def assignAttendance(uids):
        records = pd.read_csv('./data/bin/attendance_template.csv')
        
        records = records.drop(labels=['age', 'image'], axis=1)
        records = records.assign(attendance=["n"] * len(records["id"])) 
        records.loc[records['id'].isin(uids), 'attendance'] = ["y"] * len(records.loc[records['id'].isin(uids)]['attendance'])
        records.loc[records['id'].isin(uids), 'timestamp'] = [datetime.datetime.now().replace(microsecond=0).isoformat()] * len(records.loc[records['id'].isin(uids)]['attendance'])
        attendance_json = {}
        attendance_json["attendance"] = json.loads(records.to_json(orient='records'))
        attendance_json["cci"] = "someStringHere"           #reassign with cci code
        result_json = json.dumps(attendance_json, indent=4,  sort_keys=True)
        with open(r'./data/attendance.json', 'w') as f:
            f.write(result_json)
        
        Attendance.postAttendance()

    
    @staticmethod
    def visitJson(args):
        # student_data = {'bio': 'SomeDictHere', 'visitData' : args}
        visit_json = json.dumps(args, indent=4, sort_keys=True)
        with open(r'./data/visit.json', 'w') as f:
            f.write(visit_json)
        Attendance.postVisitScheduled()

    @staticmethod
    def postAttendance():
        now = datetime.datetime.now()
        if now.hour > 6:
            with open(r'./data/attendance.json') as f:
                myObj = json.loads(f.read())
                response = requests.post(Attendance.__base_api + '/attendance/children', json=myObj)
            print(response.json() , response.status_code)
    
    @staticmethod
    def postVisitScheduled():
        with open(r'./data/visit.json') as f:
            myObj = json.loads(f.read())
            response = requests.post(Attendance.__base_api + '/guardian/schedule-visit', json=myObj)

        print(response.json(), response.status_code)
        
