import asyncio
import zmq

import json
import socket

import cv2
from pyzbar.pyzbar import decode

with open('./config.json') as _file:
    config = json.load(_file)

async def on_receive(socket:zmq.Socket):
    while True:
        data = socket.recv_multipart()
        print(data)

async def handle_camera(socket):
    cap = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture(config['video_path'])
    
    qr_data = []

    i = 0
    while(cap.isOpened()): #카메라 켜놓는 부분
        ret, img = cap.read()

        cv2.rectangle((0.0),(0, 500), (500,0), (500,500))

        if not ret:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
        decoded = decode(gray)
        for d in decoded: 
            x, y, w, h = d.rect

            barcode_data = d.data.decode("utf-8")
            barcode_type = d.type

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            text = '%s (%s)' % (barcode_data, barcode_type)
            cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
            
            if barcode_data == "reset":
                qr_data = []
            if barcode_data not in qr_data:
                qr_data.append(barcode_data)
                socket.send_string(barcode_data)
                #print(type(barcode_data))
                #print('data {} appended'.format(barcode_data))
                
            #result = sim_mongo.data_search(qr_data) #데이터 찾아오는거 
            #print(result)

        cv2.imshow('img', img)
        
        key = cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()
        
async def process_async(config:dict):
    context = zmq.Context()
    sock = context.socket(zmq.DEALER)
    sock.connect(f"tcp://{config['server_addr']}:{config['server_port']}")
    
    #sock.send_string("J")
    await asyncio.wait([
        asyncio.create_task(handle_camera(sock)),
        asyncio.create_task(on_receive(sock)),
    ])

def main():
    # load configuration file
    with open('./config.json') as _file:
        config_data = json.load(_file)
        print(config_data)
    asyncio.run(process_async(config_data))
    
    pass

if __name__ == "__main__":
    main()
