import sys, os
from datetime import datetime
import zmq
import zmq.asyncio
import threading
import json
import asyncio

async def monitoring_server_open(config):
    host_config = config["host_config"]
    
    HOST_IP = host_config["host_ip"]
    HOST_PORT = host_config["host_monitor_port"]
    
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.ROUTER)
    socket.bind(f"tcp://{HOST_IP}:{HOST_PORT}")
    
    print(f'\n@@ Monitoring Router Bined tcp://{HOST_IP}:{HOST_PORT} Success!! @@')
    print(f'Waiting Messagess From Client(Monitoring)')
    
    while True :
        message = await socket.recv_multipart()
       
        identity, content = message
        content = json.loads(content.decode())
        container_name = content["client_name"]
        monitor_state = content["message"]
        
        print(f'\nFrom Monitor Dealer {container_name} Received Message : {content}')
        
        if monitor_state == config["host_config"]["task_done_message"]:
            #print("Task Done")
            #TODO close Container
            print(f'{container_name} monitor state : {monitor_state}')
            stop_container(container_name)
            
async def controller_server_open(config):  
    host_config = config["host_config"]
    client_config = config["client_config"]
    
    client_list = list(config["client_config"].keys())
    
    HOST_IP = host_config["host_ip"]
    HOST_PORT = host_config["host_controller_port"]
    
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.ROUTER)
    socket.bind(f"tcp://{HOST_IP}:{HOST_PORT}")
    
    print(f'\n@@ Controller Router Bined tcp://{HOST_IP}:{HOST_PORT} Success!! @@')
    
    while True :
        message = await socket.recv_multipart()
        print(f'From Controller Dealer n Received Message : {message}')
        print(f'Waiting Messagess From Client(Controller)')
        
        identity, content = message
        
        #TODO from message 
        if content.decode() in client_list:
            response = {
                'scenario' : client_config[content.decode()]["scenario"],
                'seed' : client_config[content.decode()]["seed"]
                }
            await socket.send_multipart([identity, json.dumps(response).encode()])
            print(f'Sent to {content.decode()} : Senario {client_config[content.decode()]["scenario"]} Seed {client_config[content.decode()]["seed"]}')
            print("Waiting From other Controller...")
            
async def run_containers(config):
    start_timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    container_config = config["container_config"]
    
    # Make Directory
    dir_path = f'{container_config["mount_dir_path"]}/r_{start_timestamp}'
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    
    #TODO Run Container
    await asyncio.sleep(1)
    
    client_config = config["client_config"]
    client_image = config["container_config"]['client_image']
    client_list = list(config["client_config"].keys())
    
    print("\n@@ Start Runing Containers ...")
    
    for i in range(len(client_list)):
        print(f'[{i}] : Container {client_list[i]} Starting...')
        
        try :
            os.system(f"docker run -v {dir_path}:/Result -d  -e CONTAINER_NAME={client_list[i]} --name {client_list[i]} {client_image}")
            print(f'[{i}] : Container {client_list[i]} is Now Running!!')

        except:
            os.system(f"docker start {client_list[i]}")
            print(f'[{i}] : Container {client_list[i]} is Now Starting!!')
            
    print("\n@@ All container is Running !!!\n")
    
def user_input_listener(start_event, stop_event):
    while True:
        user_input = input("\nProcess Options \n'S' : Start, 'R' : Restart, 'E' : Exit, 'D' : Delete, 'P' : Prune\n").lower()
        if user_input == 'r':
            print('\n')
            os.execv(sys.executable, ['python'] + sys.argv)
            
        elif user_input == 'e':
            print("\nGood Bye!! \nExiting program...")
            os._exit(0)
            
        elif user_input == 's':
            start_event.set()
        
        elif user_input == 'd':
            print(f"\nDeleting All programs Containers ... ")
            os.system(f'docker stop $(docker ps -q)')
            print(f"Deleting Done!!")
            
        elif user_input == 'p':
            print(f'\nRemoving All programs Containers ...')
            os.system(f'docker rm $(docker ps -aq)')
            print(f"Removing Done!!")
            
        else:
            print("Invalid input. Please enter 'r' or 'e' or 's'.") 
    
def stop_container(container_name):
    print(f'\nStopping {container_name} ...')
    
    os.system(f"docker stop {container_name}") # Docker Stop
    
    print(f'Deleting {container_name}...')
    
    os.system(f'docker rm {container_name}') # Docker rm
    
    print(f'{container_name} Deleted!!\n')
            
async def main(config, start_event, stop_event):
    print('\n@@ Main Server is Opened!! @@\n')
    while not start_event.is_set():
        try:
            await asyncio.wait_for(start_event.wait(), timeout=0.0001)
        except asyncio.TimeoutError:
            continue    
    tasks = asyncio.gather(*[monitoring_server_open(config), controller_server_open(config), run_containers(config)])
    
    try:
        await tasks
        
    except asyncio.CancelledError:
        print("Main tasks cancelled.")
            
if __name__ == '__main__':
    with open("./server_config.json") as config_file:
        config = json.load(config_file)
        
    loop = asyncio.get_event_loop()    
        
    start_event = asyncio.Event()
    stop_event = asyncio.Event()

    input_thread = threading.Thread(target=user_input_listener, args=(start_event, stop_event,))
    input_thread.start()
    
    try:
        loop.run_until_complete(main(config, start_event, stop_event))
        
    except KeyboardInterrupt:
        print("Caught keyboard interrupt. Canceling tasks...")
        for task in asyncio.all_tasks():
            task.cancel()
    finally:
        loop.close()