from pyevsim.system_simulator import SystemSimulator
from pyevsim.definition import *

from ai_generator import GeneratorModel

import asyncio
import zmq

import json
import pymongo

async def on_receive(socket:zmq.Socket, _engine:SystemSimulator):
    
    with open('./instance/db_config.json') as _file:
        db_config = json.load(_file)
        
    db_url = f"mongodb://{db_config['site_human_db']['db_user']}:{db_config['site_human_db']['db_pw']}@{db_config['site_human_db']['db_addr']}"
    db = pymongo.MongoClient(db_url)[db_config['site_human_db']['db_name']]
    
    while True:
        data = socket.recv_multipart()
        recv_data = data[1].decode('utf-8')
        human_info = recv_data.split(",")

        print(human_info)

        if human_info[0] == "reset":
            for co in ['sim_human_info', 'sim_sensing_info', "sim_health_info"]:
                db.drop_collection(co)
            data = [{'human_id': '412f6032-aad4-433c-b89c-a9f1755a08ec',
            'gender': 0,
            'age': 27,
            'daily_condition': 0,
            'medical_history': 1,
            'health_score': 100},
            {'human_id': '412f6032-aad4-433c-b89c-a9f1755a08ee',
            'gender': 1,
            'age': 40,
            'daily_condition': 0,
            'medical_history': 0,
            'health_score': 100},
            {'human_id': '412f6032-aad4-433c-b89c-a9f1755a08cc',
            'gender': 0,
            'age': 35,
            'daily_condition': 1,
            'medical_history': 1,
            'health_score': 100},
            ]

            db['sim_human_info'].insert_many(data)
        else:
            _engine.insert_external_event("human_info", human_info)

async def process_async(config:dict):
    context = zmq.Context()
    socket = context.socket(zmq.ROUTER)
    socket.bind(f"tcp://*:{config['server_port']}")
    
    ss = SystemSimulator()
    first = ss.register_engine("seni", "REAL_TIME", 0.01)
    
    first.insert_input_port("human_info")

    gen = GeneratorModel(0, Infinite, "Generator", "seni", first, config)
    first.register_entity(gen)
    first.coupling_relation(None, "human_info", gen, "human_info")

    ss.exec_non_block_simulate(["seni"])
    
    await asyncio.wait([
        asyncio.create_task(on_receive(socket, first)),
    ])

def main():
    # load configuration file
    with open('./config.json') as _file:
        config_data = json.load(_file)
        print(config_data)
    asyncio.run(process_async(config_data))
    
if __name__ == "__main__":
    main()