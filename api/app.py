from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from offres_emploi import Api
from offres_emploi.utils import dt_to_str_iso
from copy import copy
import time
from collections.abc import MutableMapping
import pandas as pd
import numpy as np
import re
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Sequence, DateTime, Float, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import database_exists, create_database
import logging


app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)

client_id = ""
client_secret = ""

client = Api(client_id=client_id, 
             client_secret=client_secret)

def collect_data(start, end, delta, all_results):
        local_start = copy(start)
        while local_start < end:
            time.sleep(10)
            local_end = local_start + delta
            print(f"Start getting data from  {local_start} to {local_end}")
            results = []
            params = {
                "codeROME": "M1805",
                'minCreationDate': dt_to_str_iso(local_start),
                'maxCreationDate': dt_to_str_iso(local_end)
            }
            try:
                response = client.search(params=params)
                num_results = int(response["Content-Range"]["max_results"])
                results = response["resultats"]
            except AttributeError:
                print("No results. Continue...")
                num_results = 0
            except Exception as e:
                print("Error !!!!!!!!!!!!!!!!")
                print(e)
                print(type(e))
                num_results = 0
            if num_results > 149:
                print(f"Too much results : {num_results}")
                collect_data(local_start, local_end, delta / 2, all_results)
            else:
                print(f"{num_results} results collected.")
            all_results += results
            local_start += delta


@app.route("/", methods=["GET"])
def hello_world():
    return "Hello, World!"

@app.route("/collect", methods=["POST"])
def get_datetime():
    data = request.get_json()
    print(data)
    
    if "begin_datetime" not in data:
        return jsonify({'error': 'No datetime provided'}), 400
    
    try:
        dt = datetime.fromisoformat(data['begin_datetime'])
        dt += timedelta(seconds=1)
    except ValueError:
        return jsonify({'error': 'Invalid datetime format'}), 400        

    all_results = []
    delta = timedelta(days=10)
    start = datetime(2024, 9, 1, 0, 0)
    end = datetime(2024, 11, 23, 12, 0)
    
    collect_data(start, end, delta, all_results)

    return jsonify({'data': all_results}), 200
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)