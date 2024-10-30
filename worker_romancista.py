import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from madr.models import Romancista
from madr.settings import Settings

redis_cliente = redis.Redis(host=Settings().REDIS_HOST, port=6379, db=0)

engine = create_engine(Settings().DATABASE_URL)
Session = sessionmaker(bind=engine)

session = Session()

def process_task(task_id):
    task_data = redis_cliente.hgetall(f'romancista: {task_id.decode("utf-8")}')
    if task_data:
        romancista = Romancista(id=int(task_data[b'id'].decode('utf-8')),
                                nome=task_data[b'nome'].decode('utf-8'))
        
        session.add(romancista)
        session.commit()
        redis_cliente.delete(f'romancista: {task_id.decode("utf-8")}')

    else:
        print('task_data not found in redis')

if __name__ == '__main__':
    print('woker started')

    while True:
        task = redis_cliente.blpop('romancista_queue')
        if task:
            _, task_id = task
            process_task(task_id)