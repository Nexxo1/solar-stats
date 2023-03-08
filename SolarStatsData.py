
import time
import json
import os
from datetime import datetime


class SolarStatsData:
    """
    calculates the energy stats from the power measurements
    """
    def __init__(self, file="solarStats.data"):
        self.file = file
        self.stats = {
            "load_power": 0,  # current load power consumption in Watts
            "load_cons_energy": 0,  # load energy consumption today in W/h
            "pv_power": 0,  # current pv power in Watts
            "pv_prod_energy": 0,  # pv energy production today in W/h
            "grid_power": 0,  # current grid power in Watts, positive is production, negative is consumption
            "grid_prod_energy": 0,  # grid energy production today in W/h
            "grid_cons_energy": 0,  # grid energy consumption today in W/h
            "batt_power": 0,  # current battery power in Watts, positive is production, negative is consumption
            "batt_prod_energy": 0,  # battery energy production today in W/h
            "batt_cons_energy": 0,  # battery energy consumption today in W/h
            "time": time.time(),  # time of the last stat update
            "day": datetime.today().weekday()  # current day (used to reset the stats at the start of the day
        }

        # Open the file for reading to load into stats
        if os.path.exists(file):
            with open(file, "r") as fp:
                # Load the dictionary from the file
                self.stats = json.load(fp)

        # always resets the timer
        self.stats["time"] = time.time()

    def update_stats(self, inverter_response):
        day = datetime.today().weekday()
        # resets on a new day
        if day != self.stats["day"]:
            self.stats["day"] = day
            self.stats["load_cons_energy"] = 0
            self.stats["pv_prod_energy"] = 0
            self.stats["grid_prod_energy"] = 0
            self.stats["grid_cons_energy"] = 0
            self.stats["batt_prod_energy"] = 0
            self.stats["batt_cons_energy"] = 0
            self.stats["time"] = time.time()

        time_now = time.time()
        time_delta = time_now - self.stats["time"]
        self.stats["time"] = time_now

        site = inverter_response["Body"]["Data"]["Site"]
        load_power = site["P_Load"]
        self.stats["load_power"] = load_power
        self.stats["load_cons_energy"] += abs(load_power) * time_delta / 3600

        pv_power = site["P_PV"]
        self.stats["pv_power"] = pv_power
        self.stats["pv_prod_energy"] += abs(pv_power) * time_delta / 3600

        grid_power = site["P_Grid"]
        self.stats["grid_power"] = grid_power
        if grid_power > 0:
            self.stats["grid_prod_energy"] += abs(grid_power) * time_delta / 3600
        else:
            self.stats["grid_cons_energy"] += abs(grid_power) * time_delta / 3600

        battery_power = site["P_Akku"]
        self.stats["batt_power"] = battery_power
        if battery_power > 0:
            self.stats["batt_prod_energy"] += abs(battery_power) * time_delta / 3600
        else:
            self.stats["batt_cons_energy"] += abs(battery_power) * time_delta / 3600

        with open(self.file, "w") as fp:
            json.dump(self.stats, fp)  # encode dict into JSON
