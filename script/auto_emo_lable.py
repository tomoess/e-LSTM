# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 11:21:36 2017

@author: 星
"""


########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64, sys
import json
import pandas as pd
import os,time
headers = {
    # Request headers. Replace the placeholder key below with your subscription key.
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '497b6ab054e44c5ca43b057371860c09',
}
params = urllib.parse.urlencode({
})

def auto_label(csv_file,saved_dir):
    img_data = pd.read_csv(csv_file)
    if('emotion' in img_data.keys()):
        emotion_list = img_data['emotion']
        emotion_list = emotion_list.fillna('')       
    else:
        emotion_list = ['']*len(img_data)
    for i,cocoid in enumerate(img_data['cocoid']):
        img_url = 'http://images.cocodataset.org/train2014/COCO_train2014_'+str(cocoid).zfill(12)+'.jpg'
        while(len(emotion_list[i]) == 0 or emotion_list[i].find('error')>0):
            print(cocoid,i,len(img_data))
            request = get_emotion_form_img(img_url)
            emotion_list[i]=request
            if(request.find('error')>0):
                img_data['emotion'] = emotion_list
                img_data.to_csv(csv_file,index=False)
                time.sleep(3)
            if(len(request)==0):
                img_data['emotion'] = emotion_list
                img_data.to_csv(csv_file,index=False)
                time.sleep(5)
    img_data['emotion'] = emotion_list
    img_data.to_csv(csv_file,index=False)
def get_emotion_form_img(img_url):
    body_dict = {}
    body_dict['url'] = img_url
    body = json.dumps(body_dict)
    try:
        # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
        #   For example, if you obtained your subscription keys from westcentralus, replace "westus" in the 
        #   URL below with "westcentralus".
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data.decode('utf-8'))
        print ("Response:")
        request_json = json.dumps(parsed, sort_keys=True)
        print (request_json)
        conn.close()
        return request_json
    except Exception as e:
        print(e.args)
        return ''
        
auto_label('../labels/60000to82783.csv','../labels/emotion')
