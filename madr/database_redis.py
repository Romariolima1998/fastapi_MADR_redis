import redis

from madr.schemas import LivroSchema, RomancistaSchema
from madr.settings import Settings

redis_cliente = redis.Redis(host=Settings().REDIS_HOST, port=6379, db=0)

def add_livro_to_queue(dados:LivroSchema):
    livro_id = redis_cliente.incr('livro_id')
    redis_cliente.hset(f'livro: {livro_id}', mapping={
        'id': livro_id,
        'ano': dados.ano,
        'titulo': dados.titulo,
        'id_romancista': dados.id_romancista
    })
    redis_cliente.rpush('livro_queue', livro_id)


def add_romancista_to_queue(dados: RomancistaSchema):
    romancista_id = redis_cliente.incr('romancista_id')
    redis_cliente.hset(f'romancista: {romancista_id}', mapping={
        'id': romancista_id,
        'nome': dados.nome
    })
    redis_cliente.rpush('romancista_queue', romancista_id)