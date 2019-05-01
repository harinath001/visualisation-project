from flask import Flask
from flask import request

from sqlalchemy import create_engine, and_, or_
from config import *
from models import Stats,Machine, Logs
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import json
from datetime import datetime
import datetime as dt

app = Flask(__name__)

enable_print = True

@app.route('/server_list', methods=["GET"])
def get_server_list():
    session = Session()
    retval = {}
    try:
        all_servers = session.query(Machine).all()
        names = []
        for each in all_servers:
            names.append(each.name)
        retval = json.dumps(names)
    except Exception as ex:
        retval = {"exception": str(ex)}
    return retval

@app.route('/stats/add', methods=["POST"])
def stats_add():
    values = request.get_json()
    if not values:
        return json.dumps({"error": "please provide data with json headers"})
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
            if enable_print: print(json.dumps(values, indent=4))
            cpu = float(values.get("cpu")) if "cpu" in values and values.get("cpu") else None
            disk = float(values.get("disk")) if "disk" in values and values.get("disk") else None
            memory = float(values.get("memory")) if "memory" in values and values.get("memory") else None
            gpu = float(values.get("gpu")) if "gpu" in values and values.get("gpu") else None
            network = float(values.get("network")) if "network" in values and values.get("network") else None
            processes = float(values.get("processes")) if "processes" in values and values.get("processes") else None
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
    if not values:
        return json.dumps({"error": "please provide data with json headers"})
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

@app.route('/logs/add', methods=["POST"])
def add_logs():
    values = request.get_json()
    if not values:
        return json.dumps({"error": "please provide data with json headers"})
    name = values.get('server_name', None)
    logs = {}
    if not name:
        return json.dumps({"error": "invalid name"})
    session = Session()
    machine = None
    try:
        if enable_print: print("the name of the server is ", name)
        machine = session.query(Machine).filter_by(name=name).one()
    except Exception as ex:
        logs = {"excpetion": "None or More than one servers exist with the name %s"%(name, )}

    if machine:

        try:
            if enable_print: print(json.dumps(values, indent=4))

            date_time = datetime.strptime(values.get("date_time"), "%Y-%m-%d %H:%M:%S") if "date_time" in values and values.get("date_time") else None
            status_code = int(values.get("status_code")) if "status_code" in values and values.get("status_code") else None
            source_ip = values.get("source_ip") if "source_ip" in values and values.get("source_ip") else None
            request_type = values.get("request_type") if "request_type" in values and values.get("request_type") else None
            uri = values.get("uri") if "uri" in values and values.get("uri") else None
            new_log = Logs(machine=machine, date_time=date_time, status_code=status_code,
                             source_ip=source_ip, request_type=request_type, uri=uri
                         )
            session.add(new_log)
            session.commit()
            logs = {"status": "Success"}
        except Exception as ex:
            logs = {"exception": str(ex)}


    session.close()
    return json.dumps(logs)



@app.route('/logs/get', methods=["POST"])
def get_logs():
    values = request.get_json()
    if not values:
        return json.dumps({"error": "please provide data with json headers"})
    name = values.get('server_name')
    from_date_time = values.get("from_date_time", None)
    to_date_time = values.get("to_date_time", None)
    uri_filter = values.get("uri_filter", None)
    selection_element = values.get("selection_element", None)

    logs = {}
    if not name:
        return json.dumps({"error": "invalid name"})
    if not selection_element or selection_element not in Logs.__dict__:
        return json.dumps({"error": "no selection element  given or selection element not found in table"})
    session = Session()
    machine = None
    try:
        machine = session.query(Machine).filter_by(name=name).one()
    except Exception as ex:
        logs = {"excpetion": "None or More than one servers exist with the name %s"%(name, )}

    if machine:
        # add the filter for the datetime
        from_date = datetime.strptime(from_date_time, "%Y-%m-%d %H:%M:%S") if from_date_time else datetime.now()-dt.timedelta(days=36500)
        to_date = datetime.strptime(to_date_time, "%Y-%m-%d %H:%M:%S") if to_date_time else datetime.now()+dt.timedelta(days=365)
        query = session.query(Logs.__dict__[selection_element], func.count(Logs.__dict__[selection_element])).filter( and_( (Logs.machine == machine) ,  Logs.date_time >= from_date , Logs.date_time <= to_date) )
        query = query.group_by(Logs.__dict__[selection_element])
        if uri_filter: query = query.filter(Logs.uri.like("%"+uri_filter+"%"))
        all_logs = query.all()
        # logs["results"] = []
        # for each in all_logs:
        #     logs["results"].append(
        #         {
        #             "status_code": each.status_code,
        #             "uri": each.uri,
        #             "date_time": each.date_time.strftime("%Y-%m-%d %H:%M:%S"),
        #             "source_ip": each.source_ip,
        #             "request_type": each.request_type,
        #          }
        #     )
        logs = all_logs
    session.close()
    return json.dumps(logs)



@app.route('/')
def root():
    return 'use /stats/get?server_name or /web_logs/get'

if __name__ == "__main__":
    engine = create_engine("mysql+mysqldb://%s:%s@%s/%s"%(mysql_user, mysql_password, mysql_host, mysql_db))
    Session = sessionmaker(bind=engine)
    app.run(host="0.0.0.0", port=80)

