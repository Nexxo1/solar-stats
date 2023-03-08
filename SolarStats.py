"""Application Solar Stats, pushes inverter data and stats to prometheus """

import os
import time
from prometheus_client import start_http_server, Gauge, Enum
import requests
from SolarStatsData import SolarStatsData


class SolarStats:
    """
    Creates a prometheus exporter that will provide solar stats metrics from the fronius inverter

    """

    def __init__(self, inverter_ip="192.168.10.50", polling_interval_seconds=5, test_mode=False):
        self.inverter_ip = inverter_ip
        self.polling_interval_seconds = polling_interval_seconds
        if test_mode:
            self.test_mode = "test_"
        else:
            self.test_mode = ""

        # Creates the Prometheus metrics to collect
        self.load_power_gauge = Gauge(self.test_mode+"load_power", "current load power consumption in Watts")
        self.load_cons_energy_gauge = Gauge(self.test_mode+"load_cons_energy", "Load energy consumption today in W/h")
        self.pv_power_gauge = Gauge(self.test_mode+"pv_power", "Current PV power production in Watts")
        self.pv_prod_energy_gauge = Gauge(self.test_mode+"pv_prod_energy", "PV energy production today in W/h")
        self.grid_power_gauge = Gauge(self.test_mode+"grid_power", "Current grid power in Watts, positive is production, negative is consumption")
        self.grid_prod_energy_gauge = Gauge(self.test_mode+"grid_prod_energy", "Grid energy production today in W/h")
        self.grid_cons_energy_gauge = Gauge(self.test_mode+"grid_cons_energy", "Grid energy consumption today in W/h")
        self.batt_power_gauge = Gauge(self.test_mode+"batt_power", "Current battery power in Watts, positive is production, negative is consumption")
        self.batt_prod_energy_gauge = Gauge(self.test_mode+"batt_prod_energy", "Battery energy production today in W/h")
        self.batt_cons_energy_gauge = Gauge(self.test_mode+"batt_cons_energy", "Battery energy consumption today in W/h")

        self.stats = SolarStatsData()

    def run_metrics_loop(self):
        """Metrics fetching loop"""

        while True:
            self.fetch()
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        """
        Get metrics from application and refresh Prometheus metrics with
        new values.
        """

        # Fetch data from the inverter
        url = "http://" + self.inverter_ip + "/solar_api/v1/GetPowerFlowRealtimeData.fcgi"
        # A GET request to the API
        response = requests.get(url)
        response_json = response.json()

        # calculates stats
        self.stats.update_stats(response_json)

        # Update Prometheus metrics with application metrics
        self.load_power_gauge.set(self.stats.stats["load_power"])
        self.load_cons_energy_gauge.set(self.stats.stats["load_cons_energy"])
        self.pv_power_gauge.set(self.stats.stats["pv_power"])
        self.pv_prod_energy_gauge.set(self.stats.stats["pv_prod_energy"])
        self.grid_power_gauge.set(self.stats.stats["grid_power"])
        self.grid_prod_energy_gauge.set(self.stats.stats["grid_prod_energy"])
        self.grid_cons_energy_gauge.set(self.stats.stats["grid_cons_energy"])
        self.batt_power_gauge.set(self.stats.stats["batt_power"])
        self.batt_prod_energy_gauge.set(self.stats.stats["batt_prod_energy"])
        self.batt_cons_energy_gauge.set(self.stats.stats["batt_cons_energy"])


def main():
    """Main entry point"""

    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "5"))
    inverter_ip = os.getenv("INVERTER_IP", "192.168.10.50")
    exporter_port = int(os.getenv("EXPORTER_PORT", "9877"))
    test_mode_int = int(os.getenv("TEST_MODE", "0"))
    if test_mode_int == 0:
        test_mode = False
    else:
        test_mode = True

    print("Starting solar stats with the following config:")
    print(" - polling_interval_seconds: ", polling_interval_seconds)
    print(" - inverter_ip: ", inverter_ip)
    print(" - exporter_port: ", exporter_port)
    print(" - test_mode: ", test_mode)

    app_metrics = SolarStats(
        inverter_ip=inverter_ip,
        polling_interval_seconds=polling_interval_seconds,
        test_mode=test_mode
    )
    start_http_server(exporter_port)
    app_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()