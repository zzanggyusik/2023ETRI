#!/bin/bash
python3 ./Simulation_Monitor/multi_simulation.py &
python3 ./Simulation_Controller/simulation_controller.py &
wait