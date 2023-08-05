from config import *

import cv2
from pyzbar.pyzbar import decode
import json

import pymongo

def cam_open():
    cam = cv2.VideoCapture(0)
    
    qr_data = []

    i = 0
    while(cam.isOpened()): #카메라 켜놓는 부분
        ret, img = cam.read()

        cv2.rectangle((0.0),(0, 500), (500,0), (500,500))

        if not ret:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
        decoded = decode(gray)
        for d in decoded: 
            x, y, w, h = d.rect

            barcode_data = d.data.decode("utf-8")
            barcode_data = json.dumps(barcode_data)
            barcode_type = d.type

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            text = f'{barcode_data} ({barcode_type})'
            cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
            
            print(barcode_data)
            
            if barcode_data not in qr_data:
                qr_data.append(barcode_data)
                
            print(qr_data)

        cv2.imshow('img', img)
        
        key = cv2.waitKey(1)
        
        if key == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    
def db_updater(qr_data):
    db_url = f"mongodb://{DBConfig.ip}:{DBConfig.port}"
    human_info_db = pymongo.MongoClient(db_url)[DBConfig.human_db_name]
    site_info_db = pymongo.MongoClient(db_url)[DBConfig.site_db_name]
    
    for i in range(len(qr_data)):
        if qr_data[i]['id'] in HUMAN_LIST:
            human_info_db[DBConfig.human_info_collection].update_one({'id':qr_data[i]['id']}, {'exist':qr_data[i]['exist']})
            
            

def main():
    cam_open()
    
    pass

if __name__ == "__main__":
    main()
