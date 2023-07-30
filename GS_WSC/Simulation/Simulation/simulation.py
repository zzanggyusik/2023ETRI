import time, sys
import random

def simulate_option(scenario, seed, config):
    start_time = time.time()
    
    random.seed(seed)
    
    for i in range(100):
        rand_num = random.random()
        
        if scenario == "1" and rand_num > 0.3:
            time.sleep(1)
        
        elif scenario == "2" and rand_num > 0.5:
            time.sleep(1)
            
        elif scenario == "3" and rand_num > 0.7:
            time.sleep(1)
            
        if (i+1 // 10) == 0: 
            print(i+1)
            
        print(i)
            
    finish_time = time.time()
    
    result_path = f'{config["result_path"]}{config["client_name"]}.txt'
    result_data = f'Task Time : {finish_time - start_time}\nScenario : {scenario}\nSeed : {seed}'
    save_result(result_path, result_data)
    print("Simulation Done!!")
        
def simulate():
    start_time = time.time()
        
    for i in range(100):
        if random.random() > 0.5:
            time.sleep(1)
    
    finish_time = time.time()
    
    result_path = f'./localhost.txt'
    result_data = f'Task Time : {finish_time - start_time}'
    save_result(result_path, result_data)
        
def save_result(path, data):
    with open(path, 'w') as f:
        f.write(data)
        
if __name__ == '__main__':
    
        
    if len(sys.argv) > 1:
        config = {
            "result_path" : sys.argv[3],
            "client_name" : sys.argv[4]
        }
        simulate_option(sys.argv[1], sys.argv[2], config)
        
    else : simulate()