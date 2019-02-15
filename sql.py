from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from time import strftime


engine = create_engine('sqlite:///db.sqlite')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    value = Column(String)
    status = Column(Integer)
    timestamp = Column(Integer)

    def __init__(self, value, status, timestamp):
        self.value = value
        self.status = status
        self.timestamp = timestamp

    def __repr__(self):
        return '%i/%s/%i/%i' % (self.id, self.value, self.status, self.timestamp)


def update_db(input_stream):
    changed_items = []
    #update base from main_array
    for i in input_stream:
        #если отправка прошла успешно - обновляем
        if i[2] == 1:
            print('sended and updated id {} in db'.format(i[0]))
            key = session.query(Data).filter_by(id=i[0]).first()
            setattr(key, 'status', 1)
            changed_items.append(i)
    #применяем изменения
    session.commit()
    return changed_items


def write_db(input_stream):
    data_write = Data(value=input_stream[0], status=input_stream[1], timestamp=input_stream[2])
    session.add(data_write)
    session.commit()
    print('writing id {} in db at {}'.format(data_write.id, strftime('%M:%S')))
    return data_write.id


def init_db():
    print('init_db')
    result_arr = []
    for i in session.query(Data).filter_by(status=0):
        result_arr.append([i.id, i.value, i.status, i.timestamp])
    session.commit()
    return result_arr



