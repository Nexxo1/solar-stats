#!/bin/bash

polling_interval_seconds=5
inverter_ip=192.168.10.50
exporter_port=9877
test_mode=1

export POLLING_INTERVAL_SECONDS=$polling_interval_seconds
export INVERTER_IP=$inverter_ip
export EXPORTER_PORT=$exporter_port
export TEST_MODE=$test_mode

python3 SolarStats.py