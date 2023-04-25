from flask import Flask, request
from flask_cors import CORS, cross_origin
from typing import *
import json
import datetime as dt_
from datetime import datetime, date, time, timezone
import boto3

app = Flask(__name__)


@app.route('/getStatus', methods=['GET'])
@cross_origin(origin='*')
def getStatus():
    start__: Optional[str] = request.args.get("DateTime", None, type=str)
    diff_: Optional[str] = request.args.get("Diff", None, type=int) 

    if start__ is None or diff_ is None:
        return {
            'statusCode': 404,
            'body': {"info":'Missing Parameters'}
        }

    client = boto3.resource('dynamodb')
    table = client.Table('apiData_AIQ')
    
    res = []
    start_ = datetime.strptime(start__, "%Y-%m-%dT%H:%M")
    count_ = 1
    while len(res) < diff_:
        time_key_ = (start_ - dt_.timedelta(minutes = count_)).strftime("%Y-%m-%dT%H:%M")
        resp_ = table.get_item(Key={"id": time_key_})
            
        
        if "Item" in resp_:
            res.append(resp_['Item'])
        count_ += 1
        
    
    if len(res)>0:
        
        cast = {
            "TVOC": [],
            "TEMP": [],
            "HCHO": [],
            "C02": [],
            "PM25": [],
            "PM10": [],
            "HUMI": [],
            "id": [],
            "DateTime": []}
            
        for i in res:
            cast["TVOC"].append(i["TVOC"])
            cast["TEMP"].append(i["TEMP"])
            cast["HCHO"].append(i["HCHO"])
            cast["C02"].append(i["C02"])
            cast["PM25"].append(i["PM25"])
            cast["PM10"].append(i["PM10"])
            cast["HUMI"].append(i["HUMI"])
            cast["id"].append(i["id"])
            cast["DateTime"].append(i["DateTime"])
        
        
        return {
            'statusCode': 200,
            'body': cast,
        }
    else:
        return {
            'statusCode': 404,
            'body': {"info":'Not found'}
        }


app.run(host='0.0.0.0', port=5000)