from flask import flash
from sqlalchemy import select

from database import Jogador, db_session

def select_todos_jogadores():

    jogadores_sql = select(Jogador)
    jogadores = db_session.execute(jogadores_sql).scalars().all()
    return jogadores

def salvar(nome, numero_camisa, posicao, time_id):
    try:
        novo_jogador = Jogador(nome=nome, numero_camisa=int(numero_camisa), posicao=posicao, time_id=int(time_id))

        db_session.add(novo_jogador)
        db_session.commit()
        flash('Jogador adicionado com Sucesso', 'success')

    except SQLAlchemyError as e:
        db_session.rollback()
        flash('Erro ao adicionar jogador', 'error')

    except Exception as e:
        db_session.rollback()
        flash('Erro inesperado', 'error')
        print(f'Erro: {e}')
