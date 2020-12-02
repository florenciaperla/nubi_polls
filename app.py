from flask import Flask, request, json, Response
from flask import Flask, request, json, Response
from pymongo import MongoClient
import logging as log
import datetime
from bson import ObjectId

print("connecting database...")
client = MongoClient("mongodb+srv://ddmilgram:DPYutVu33y2ZofXI@cluster0-oa6bc.mongodb.net/<test>?retryWrites=false&w=majority")
print("connection established with Mongo")

class MongoAPI:
    def __init__(self, document):
        cursor = client["polls"]
        self.collection = cursor[document]

    def read(self):
        documents = self.collection.find()
        output = [{item: str(data[item]) for item in data} for data in documents]
        return output

    def find_byid(self,id):
        document = self.collection.find_one({"_id" : ObjectId(id)})
        return document

    def find_one(self,key,value):
        document = self.collection.find_one({key : value})
        return document

    def find(self,key,value):
        documents = self.collection.find({key : value})
        output = [{item: str(data[item]) for item in data} for data in documents]
        return output

    def write(self, data):
        new_document = data
        new_document["createdDate"] = datetime.datetime.today()
        self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted'}
        return output

    def update(self):
        filt = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, data):
        filt = data['Filter']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output


app = Flask(__name__)   

@app.route('/')
def base():
    return "status:up"

@app.route('/answers/getbyuser', methods=['GET'])
def answers_getbyuser():
    data = request.json
    res = MongoAPI("answers").find("email",data["email"])
    return Response(response=json.dumps(res),status=200,mimetype='application/json')

@app.route('/answers/add', methods=['POST'])
def answers_post():
    data = request.json
    res = MongoAPI("answers").write(data)
    return Response(response=json.dumps(res),status=200,mimetype='application/json')

@app.route('/polls/add', methods=['POST'])
def polls_post():
    data = request.json
    res = MongoAPI("polls").write(data)
    return Response(response=json.dumps(res),status=200,mimetype='application/json')    

@app.route('/polls/getall', methods=['GET'])
def polls_get():
    res = MongoAPI("polls").read()
    return Response(response=json.dumps(res),status=200,mimetype='application/json')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)







