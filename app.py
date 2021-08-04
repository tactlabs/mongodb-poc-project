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
        email = request.form.get("email")
        clname = request.form.get("clname")
        year_month = request.form.get("ym")

        query = {"Name" : name ,"Email" : email , "College_Name" : clname , "Passout_Year" : year_month}
        collection.insert_one(query)
        
        for x in collection.find():
            name   = x['Name']
            email  = x['Email']
            clname = x['College_Name']
            year_month = x['Passout_Year']

            result = {
                'Name' : name,
                'Email' : email,
                'College_Name' : clname,
                'Passout_Year' : year_month
            }

    return render_template("intern.html",result = result)

@app.route('/find_one',methods=['GET','POST'])
def first_one():
   
    result = collection.find_one()
        
    print(result)
    return render_template("find_one.html",result = result)


@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/all_details',methods=["GET","POST"])
def all_details():
    collection = db["details"]
    details =[]
    for x in collection.find():
        name   = x['Name']
        email  = x['Email']
        clname = x['College_Name']
        year_month = x['Passout_Year']

        result = {
            'Name' : name,
            'Email' : email,
            'College_Name' : clname,
            'Passout_Year' : year_month
        }
        details.append(result)
    # print(details)
    return render_template("all_details.html",result = details)

@app.route('/drop',methods=['GET','POST'])
def drop():
    collection = db["details"]
    collection.delete_many({})

    return redirect(request.referrer) 
  

@app.route('/college-count',methods=["GET","POST"])
def task_count():
    collection = db["details"]
    # details =[]
    agg_result = collection.aggregate(
        [{
            "$group" :
             {"_id" : "$College_Name",
             "Number_of_interns" : {"$sum" : 1}
             }}
        ])
    
    return render_template("number_of_interns.html",agg_result = agg_result)
    


@app.route('/sort',methods=['GET','POST'])
def sort():

    result = collection.find().sort("Name") 
    # print(result)
    return render_template("sort.html",result = result)


@app.route('/search',methods=['GET','POST'])
def search():
    nm = request.form.get("nm")
    # print(nm)
    result = collection.find_one({"Name":nm})
    # print(result)

    return render_template("search.html",result = result)


@app.route('/delete_one',methods=['GET','POST'])
def delete_name():
    name = request.form.get("del")
    print(name)
    del_name = {"Name" : name}
    collection.delete_one(del_name)

    return redirect(request.referrer)

@app.route('/name_edit',methods=['GET','POST'])
def name_edit():
    name = request.form.get("name")
    update_name = request.form.get("update")

    filter = { 'Name': name }
    newvalues = { "$set": { 'Name': update_name } }

    collection.update_one(filter, newvalues) 
    return redirect(request.referrer)

@app.route('/limit',methods=['GET','POST'])
def limit():
    lmt =int(request.form.get("nm"))
    print(lmt)
    doc1 = collection.find().limit(lmt)
    # print(doc1)

    return render_template("limited_intern_details.html",doc1 = doc1)

if __name__ == '__main__':
    app.run(debug=True,port=PORT)