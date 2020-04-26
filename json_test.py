# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 19:35:19 2020

@author: Warsars
"""
import json
import time
import numpy as np
import math
from random import randint
import requests
arg = 0;
n=0;
while True:
    arg = arg + math.pi / 40;
    if arg > 2 * math.pi:
        arg=arg-2*math.pi;
        n=n+1;
    sin_curr = math.sin(arg);
    #print(round(sin_curr*100,0));
    new_data = {'id': 2, 'ax': int(round(sin_curr*100,2)), 'ay': 2, 'az': 3, 'gx': 100, 'gy': 5, 'gz': 5, 'mx': 0, 'my': 0, 'mz': 0};
    requests.post("http://127.0.0.1:8000/api/v1/esp/create/", data=new_data)
    time.sleep(0.5);
    if n>4:
        break;
    response = requests.get("http://127.0.0.1:8000/api/v1/esp/last?format=json")
    current_data = json.loads(response.text);
    #http://127.0.0.1:8000/api/v1/esp/last?format=json
    #encoded_hand = json.dumps(current_data)
    print('ax= ',current_data['ax']);