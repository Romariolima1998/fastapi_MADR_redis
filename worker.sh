#!/bin/bash
# Inicia o primeiro processo em segundo plano
python3 worker_livro.py &
# Inicia o segundo processo em segundo plano
python3 worker_romancista.py &
# Aguarda os dois processos terminarem
wait