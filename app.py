from flask import Flask
from flask import request

from sqlalchemy import create_engine
from config import *
from models import Stats,Machine
from sqlalchemy.orm import sessionmaker
import json

app = Flask(__name__)

@app.route('/stats/add', methods=["POST"])
def stats_add():
    values = request.get_json()

    name = values.get('server_name', None)
    stats = {}
    if not name:
        return json.dumps({"error": "invalid name"})
    session = Session()
    machine = None
    try:
        machine = session.query(Machine).filter_by(name=name).one()
    except Exception as ex:
        stats = {"excpetion": "None or More than one servers exist with the name %s"%(name, )}

    if machine:
        count = session.query(Stats).filter_by(machine=machine).count()
        if count >= stats_count_limit:
            extra_stats = session.query(Stats).filter_by(machine=machine).order_by(Stats.id.asc()).limit(count-stats_count_limit+1)
            for each in extra_stats:
                session.delete(each)
        try:
            cpu = float(values.get("cpu")) if "cpu" in values else None
            disk = float(values.get("disk")) if "disk" in values else None
            memory = float(values.get("memory")) if "memory" in values else None
            gpu = float(values.get("gpu")) if "gpu" in values else None
            network = float(values.get("network")) if "network" in values else None
            processes = float(values.get("processes")) if "processes" in values else None
            new_stat = Stats(machine=machine, cpu=cpu, memory=memory,
                         disk=disk, gpu=gpu,
                         network=network, processes=processes)
            session.add(new_stat)
            session.commit()
            stats = {"status": "Success"}
        except Exception as ex:
            stats = {"exception": str(ex)}


    session.close()
    return json.dumps(stats)

@app.route('/stats/get', methods=["GET"])
def stats_get():
    name = request.values.get('server_name')
    stats = {}
    if not name:
        return json.dumps({"error": "invalid name"})
    session = Session()
    machine = None
    try:
        machine = session.query(Machine).filter_by(name=name).one()
    except Exception as ex:
        stats = {"excpetion": "None or More than one servers exist with the name %s"%(name, )}

    if machine:
        all_stats = session.query(Stats).filter_by(machine=machine).all()
        stats["results"] = []
        for each in all_stats:
            stats["results"].append(
                {
                    "cpu": each.cpu,
                    "memory": each.memory,
                    "disk": each.disk,
                    "gpu": each.gpu,
                    "network": each.network,
                    "processes": each.processes
                 }
            )

    session.close()
    return json.dumps(stats)

@app.route("/new-machine", methods=["POST"])
def new_machine():
    values = request.get_json()
    result = {}
    session = None
    password = values.get("password", None)
    if not password:
        result = {"exception": "password missing"}
    else:
        if not password==entry_password :
            result = {"exception": "Wrong password"}
        else:
            try:
                ip = values.get("ip", None)
                name = values.get("name", None)
                if(not name or not ip): raise Exception("IP or NAME missing !!")
                session = Session()
                m = Machine(ip=ip, name=name)
                session.add(m)
                session.commit()
                result = {"status": "success !!"}
            except Exception as ex:
                result = {"exception": str(ex)}

    if session: session.close()
    return json.dumps(result)

@app.route('/')
def root():
    return 'use /stats/get?server_name or /web_logs/get'

if __name__ == "__main__":
    engine = create_engine("mysql+mysqldb://%s:%s@%s/%s"%(mysql_user, mysql_password, mysql_host, mysql_db))
    Session = sessionmaker(bind=engine)
    app.run(host="0.0.0.0", port=80)

