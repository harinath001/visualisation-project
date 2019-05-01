import requests
import psutil
import time
import json


def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f' % (value, )
    return "%s" % n


url = "http://localhost/stats/add"
sleep_time = 3 #in seconds
prev_bytes_sent = psutil.net_io_counters().bytes_sent
prev_time = time.time()

time.sleep(sleep_time)
while True:
    cpu = psutil.cpu_percent(interval=1)
    processes = len(psutil.pids())
    gpu = None
    memory = psutil.virtual_memory()[2]
    disk = (psutil.disk_usage('/').total)/(1024*1024)
    network = (psutil.net_io_counters().bytes_sent - prev_bytes_sent)/(time.time() - prev_time)
    prev_time = time.time()
    try:
        r = requests.post(url, json={"server_name": "server 1", "cpu": cpu, "memory":memory, "network": network, "gpu": gpu, "processes": processes, "disk": disk})
        print(json.dumps(r.json(), indent=4))
    except Exception as ex:
        print(ex)
    time.sleep(sleep_time)
