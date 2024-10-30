import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from madr.models import Livro
from madr.settings import Settings

redis_cliente = redis.Redis(host=Settings().REDIS_HOST, port=6379, db=0)

engine = create_engine(Settings().DATABASE_URL)
Session = sessionmaker(bind=engine)

session = Session()

def process_task(task_id):
    task_data = redis_cliente.hgetall(f'livro: {task_id.decode("utf-8")}')
    if task_data:
        livro = Livro(
            id=int(task_data[b'id'].decode('utf-8')), ano=int(task_data[b'ano'].decode('utf-8')),
            titulo=task_data[b'titulo'].decode('utf-8'),
            id_romancista=task_data[b'id_romancista'].decode('utf-8'), )
        
        session.add(livro)
        session.commit()
        redis_cliente.delete(f'livro: {task_id.decode("utf-8")}')

    else:
        print('task_data not found in redis')

if __name__ == '__main__':
    print('woker started')

    while True:
        task = redis_cliente.blpop('livro_queue')
        if task:
            _, task_id = task
            process_task(task_id)