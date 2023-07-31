import cv2
import json
import asyncio
from pyzbar.pyzbar import decode
from pymongo import MongoClient

async def cam(config):
    id = config["id"]
    pwd = config["pwd"]
    
    client = MongoClient(config['ip'], config['port'])
    db = client.pyrexiasim.human_info
      
    cam = cv2.VideoCapture(0)
    qr_data = []

    i = 0
    while(cam.isOpened()):
    
        ret, img = cam.read()
        str = "Press Q to escape"
        cv2.putText(img, str, (1100, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
        cv2.rectangle((0.0),(0, 1000), (1000,0), (1000,1000))

        if not ret:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
        decoded = decode(gray)
        for d in decoded: 
            x, y, w, h = d.rect

            barcode_data = d.data.decode("utf-8")
            barcode_type = d.type

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            text = f'{barcode_data}, {barcode_type}'
            cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
            
            if barcode_data == "reset":
                qr_data = []
                # Delete ALL
            
            if barcode_data not in qr_data:
                qr_data.append(barcode_data)
                barcode_data = eval(barcode_data)
                print((barcode_data))
                
                if barcode_data['exist'] == 1:
                    db.insert_one(barcode_data)
                    #Data insert
                    print('Data inserted {}'.format(barcode_data["human_id"]))
                
                elif barcode_data['exist'] == 0:
                    db.update_one({"id": barcode_data["id"]}, {"$set": barcode_data})
                    print('Data updated {}'.format(barcode_data["id"]))

        cv2.imshow('img', img)
        
        key = cv2.waitKey(1)
        
        if key == ord('q'):
            break
        
    cam.release()
    cv2.destroyAllWindows()

def main():
    with open("./master_config.json") as _file:
        config = json.load(_file)
    asyncio.run(cam(config["DB_config"]))    
            
if __name__ == "__main__":
    # To escape Press Q
    main()