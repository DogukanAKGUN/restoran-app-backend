import pymongo
import json
import base64
import datetime
import http.client
from flask import Flask,jsonify,render_template,request,redirect,session
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

myclient = pymongo.MongoClient("mongodb+srv://dogukanakgun22:dogukan123Q@restorant-app-db.2rc5mky.mongodb.net/?retryWrites=true&w=majority&appName=restorant-app-db")
mydb = myclient["RestoranDB"]
menuTable = mydb["MenuItems"]
HotDrinksTable = mydb["HotDrinks"]
ColdDrinksTable = mydb["ColdDrinks"]
CanDinksTable = mydb["CanDrinks"]
ItemsTable = mydb["Items"]
vehiclesTable = mydb["vehicles"]
usersTable = mydb["Users"]
otomobilBrandsTable = mydb["otomobilBrands"]
motorcycleBrandsTable = mydb["motorcycleBrands"]
suvBrandsTable = mydb["suvBrands"]
carDetailTable = mydb["carDetails"]
vehicleListTable = mydb["vehicleList"]


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print("data",data)
    userName = data["username"]
    password = data["password"]
    userCheck = usersTable.find_one({'username': userName})


    if userCheck is not None:
        if (userCheck['password'] == password):
            return {"result":"ok"}
        else:
            return '404'
    else:
        print("Yok knk girme")

"""
def get_sequence(seq_name):
    return mydb.counters.find_and_modify(query={"_id": seq_name}, update={"$inc": {"seq": 1}}, upsert=True)["seq"]
"""

@app.route('/script')
def script():
    menuitems = list(menuTable.find({}))

    return menuitems

@app.route('/get-items')
def getItems():
    items = list(ItemsTable.find({}))

    return items

@app.route('/hot-drinks')
def hotDrinks():
    hotdrinks = list(ItemsTable.find({"type": "Sıcak İçecekler"}))
    return hotdrinks

@app.route('/cold-drinks')
def coldDrinks():
    colddrinks = list(ItemsTable.find({"type": "Soğuk İçecekler"}))
    return colddrinks

@app.route('/can-drinks')
def canDrinks():
    candrinks = list(ItemsTable.find({"type": "Kutu İçecekler"}))
    return candrinks

@app.route('/toasts')
def toasts():
    toasts = list(ItemsTable.find({"type": "Tostlar"}))
    return toasts

@app.route('/snacks')
def snacks():
    toasts = list(ItemsTable.find({"type": "Aperatifler"}))
    return toasts

@app.route('/icecream')
def icecream():
    toasts = list(ItemsTable.find({"type": "Dondurmalar"}))
    return toasts

@app.route('/update-menu-item', methods=['POST'])
def updateMenuItem():
    data = request.get_json()

    id = data['_id']
    menuTable.find_one_and_replace({"_id": id},data)
    item = menuTable.find_one({"_id": id})

    return item

@app.route('/update-item', methods=['POST'])
def updateItem():
    data = request.get_json()
    if data["_id"] is None:
        return "olmadı"
    id = data['_id']
    ItemsTable.find_one_and_replace({"_id": id},data)
    item = ItemsTable.find_one({"_id": id})

    return item

@app.route('/save-item', methods=['POST'])
def saveItem():
    data = request.get_json()

    id = ItemsTable.count_documents({}) +1
    data["_id"] = id
    print(data)
    ItemsTable.insert_one(data)
    return "ok"

@app.route('/delete-item', methods=['POST'])
def delItem():
    data = request.get_json()
    id = data["_id"]
    ItemsTable.delete_one({"_id":id})
    return "ok"

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    count = list(usersTable.find())
    user = {
        "_id": len(count) + 1,
        "role": "user",
        "userName": data["userName"],
        "password": data["password"]
    }
    #usersTable.insert_one(user)
    return {"resultCode":"Ok"}



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)