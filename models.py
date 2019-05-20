from sqlalchemy import create_engine
from config import mysql_host, mysql_password, mysql_port, mysql_user, mysql_db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+mysqldb://%s:%s@%s/%s"%(mysql_user, mysql_password, mysql_host, mysql_db))
Base = declarative_base()

class Stats(Base):
    __tablename__ = 'stats'

    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey('machine.id'))
    machine = relationship("Machine")
    cpu = Column(Float)
    memory = Column(Float)
    disk = Column(Float)
    gpu = Column(Float)
    network = Column(Float)
    processes = Column(Float)

class Machine(Base):
    __tablename__ = 'machine'
    id = Column(Integer, primary_key=True)
    ip = Column(String(16))
    name = Column(String(50), unique=True)
    latitude = Column(String(20))
    longitude = Column(String(20))
    #stats = relationship("Stats", order_by=Stats.id)

class Logs(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey('machine.id'))
    machine = relationship("Machine")
    date_time = Column(DateTime)
    status_code = Column(Integer)
    source_ip = Column(String(16))
    request_type = Column(String(10))
    uri = Column(String(1024))

Base.metadata.create_all(engine)
print("tables created...")
#Session = sessionmaker(bind=engine)
#session = Session()
# m = Machine(ip="1.2.3.4", name="server 1")
# s = Stats(machine=m, cpu=0.1, memory=0.1, disk=0.1, gpu=0.1, network=0.1, processes=10)
# session.add(m)
# session.add(s)
# session.commit()
# mac = session.query(Machine).filter_by(name='ed').first()
# mac = session.query(Machine).filter_by(name='ed').one()
# sts = session.query(Stats).filter_by(machine=m).order_by(Stats.id.asc()).first()
#engine.dispose()
