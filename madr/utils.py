

def string_handling(string: str) -> str:
    # Tratamento da string: remover espaços extras e deixar tudo minúsculo
    nome_tratado = string.strip().lower()

    # Remover espaços duplicados no meio da string
    nome_tratado = " ".join(nome_tratado.split())

    return nome_tratado
