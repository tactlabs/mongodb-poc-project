from flask import Flask,render_template,request,redirect
from dotenv import load_dotenv

import os
from pymongo import MongoClient

app = Flask(__name__)
PORT = 3000


load_dotenv
mongo_uri = os.getenv('MONGO_URI')
cluster = MongoClient(mongo_uri)

db = cluster["task-update"]
collection = db["details"]

@app.route('/',methods=['GET','POST'])
def home():
    return render_template("index.html")

@app.route('/submit',methods=['GET','POST'])
def submt():
    collection = db["details"]
    if request.method == 'POST':

        name = request.form.get("nm")
        date = request.form.get("date")
        task = request.form.get("task")
        time = request.form.get("time")

        # print(name)
        # print(date)
        # print(task)
        # print(time)
        query = {"Name" : name ,"Date" : date , "Task" : task , "Working Time" : time}
        collection.insert_one(query)
        
        for x in collection.find():
            name = x['Name']
            date = x['Date']
            task = x['Task']
            time = x['Working Time']

            result = {
                'Name' : name,
                'Date' : date,
                'Task' : task,
                'Working_Time' : time
            }

    return render_template("intern.html",result = result)


    # return "Daily update added successfully! "

@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/all_details',methods=["GET","POST"])
def all_details():
    collection = db["details"]
    details =[]
    for x in collection.find():
        name = x['Name']
        date = x['Date']
        task = x['Task']
        time = x['Working Time']

        result = {
            'Name' : name,
            'Date' : date,
            'Task' : task,
            'Working_Time' : time
        }
        details.append(result)
    # print(details)
    return render_template("all_details.html",result = details)

@app.route('/drop',methods=['GET','POST'])
def drop():
    collection = db["details"]
    collection.delete_many({})

    return redirect(request.referrer) 



# @app.route('/sort',methods=["GET","POST"])
# def sort():
#     collection = db["details"]
#     details =[]
#     for x in collection.find().sort({"Name":1}):
#         name = x['Name']
#         date = x['Date']
#         task = x['Task']
#         time = x['Working Time']

#         result = {
#             'Name' : name,
#             'Date' : date,
#             'Task' : task,
#             'Working_Time' : time
#         }
#         details.append(result)
#     # print(details)
#     return render_template("sort.html",result = details)

@app.route('/task_count',methods=["GET","POST"])
def task_count():
    collection = db["details"]
    # details =[]
    agg_result = collection.aggregate(
        [{
            "$group" :
             {"_id" : "$Name",
             "Task_count" : {"$sum" : 1}
             }}
        ])
    
    return render_template("task_count.html",agg_result = agg_result)
    


if __name__ == '__main__':
    app.run(debug=True,port=PORT)