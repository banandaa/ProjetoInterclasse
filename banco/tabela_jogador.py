from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError

from database import Jogador, db_session, Time


def select_todos_jogadores():

    # join(tabela que eu quero juntar, condição = chave estrangeira igual chave primária )

    jogadores_sql = select(Jogador, Time).join(Time, Jogador.time_id == Time.id)
    #usar scalars quando tiver somente uma tabela
    jogadores = db_session.execute(jogadores_sql).all()
    return jogadores

def select_quantidade_total():
    jogadores_sql = select(func.count(Jogador.id))
    qtd_total = db_session.execute(jogadores_sql).scalar()
    return qtd_total

print(select_quantidade_total())

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

def select_um(id_jogador):
    jogador_sql = select(Jogador).where(Jogador.id == id_jogador)
    jogador = db_session.execute(jogador_sql).scalar_one_or_none()
    return jogador

def select_por_time(id_time):
    jogadores_sql = select(Jogador).where(Jogador.time_id == id_time)
    jogadores = db_session.execute(jogadores_sql).scalars().all()
    return jogadores

print(select_por_time(2))
