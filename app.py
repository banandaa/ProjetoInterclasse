from datetime import date

from flask import Flask, render_template, request, redirect, url_for, flash, g
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import *

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    times_sql = select(Time)
    # 2 - executar o select
    # variavel da lista de times
    times = db_session.execute(times_sql).scalars().all()



    return render_template(
        "dashboard.html",
        total_jogadores=0,
        total_times=len(times),
        total_partidas=0,

    )


@app.route("/jogadores")
def listar_jogadores():
    return render_template("jogadores.html", jogadores=[], times=[])


@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():

    if request.method == "POST":
        # 1- Pegar os valores do Form
        nome = request.form.get("nome", "").strip()
        numero_camisa = request.form.get("numero_camisa") or None
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None


        # 2- Verificar se foi digitado

        if not nome:
            flash('Preencha o nome do jogador', 'error')
            return  render_template("jogadores.html")

        if not numero_camisa:
            flash('Preencha o número de camisa', 'error')
            return render_template("jogadores.html")
        if not posicao:
            flash('Preencha a posicao do jogador', 'error')
            return render_template("jogadores.html")
        if not time_id:
            flash('Preencha o time do jogador', 'error')
            return render_template("jogadores.html")

        # 3- Salvar no banco

        try:
            novo_jogador = Jogador(nome = nome, numero_camisa= int( numero_camisa), posicao= posicao, time_id= int(time_id))

            db_session.add(novo_jogador)
            db_session.commit()
            flash('Jogado adicionado com Sucesso', 'success')

        except SQLAlchemyError as e:
            db_session.rollback()
            flash('Erro ao adicionar jogador', 'error')

        except Exception as e:
            db_session.rollback()
            flash('Erro inesperado', 'error')
            print(f'Erro: {e}')

        # buscar todos os times no banco
        # 1 -  montar o select
        # sql é o comando, e não a lista
        times_sql = select(Time)
        # 2 - executar o select
        # variavel da lista de times
        times = db_session.execute(times_sql).scalars().all()
        return render_template("jogadores.html", jogadores=[], times=times)


@app.route("/times")
def listar_times():
    # buscar todos os times no banco
    # 1 -  montar o select
    # sql é o comando, e não a lista
    times_sql = select(Time)
    # 2 - executar o select
    # variavel da lista de times
    times = db_session.execute(times_sql).scalars().all()
    return render_template("times.html", times=times)

@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():

    if request.method == "POST":

        #1- Pegar os valores do Form
        nome = request.form.get("nome", "").strip()
        turma = request.form.get("turma", "").strip()
        responsavel = request.form.get("responsavel", "").strip()

        #2- Verificar se foi digitado

        if not nome:
            flash('Preencha o Nome do time', 'error')
            return render_template("times.html")
        if not turma:
            flash('Preencha a Turma do time', 'error')
            return render_template("times.html")
        if not responsavel:
            flash('Preencha o Responsável do time', 'error')
            print(f'Erro: {e}')
            return render_template("times.html")

        #3- Salvar no banco

        try:
            novo_time = Time(nome= nome, turma= turma, responsavel= responsavel )

            db_session.add(novo_time)
            db_session.commit()
            flash('Time adicionado com Sucesso', 'success')

        except SQLAlchemyError as e:
            db_session.rollback()
            flash('Erro ao adicionar novo time', 'error')

        except Exception as e:
            db_session.rollback()
            flash('Erro inesperado', 'error')
            print(f'Erro: {e}')

    #buscar todos os times no banco
    #1 -  montar o select
    #sql é o comando, e não a lista
    times_sql = select(Time)
    #2 - executar o select
    #variavel da lista de times
    times = db_session.execute(times_sql).scalars().all()
    print(times)

    return render_template("times.html", times=times)


@app.route("/partidas")
def listar_partidas():

    return render_template("partidas.html", partidas=[], times=[])


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():

    if request.method == "POST":
        # 1- Pegar os valores do Form
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("placar_casa") or 0
        gols_visitante = request.form.get("placar_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()

        # 2- Verificar se foi digitado

        if not time_casa_id:
            flash('Preencha o Time de campo da Partida', 'error')
            return render_template("partidas.html")
        if not time_visitante_id:
            flash('Preencha o Time Visitante da Partida', 'error')
            return render_template("partidas.html")
        if not gols_casa:
            flash('Preencha os Gols do time de campo da Partida', 'error')
            return render_template("partidas.html")
        if not gols_visitante:
            flash('Preencha os Gols do time Visitante da Partida', 'error')
            return render_template("partidas.html")
        if not data_partida:
            flash('Preencha a Data da Partida', 'error')
            return render_template("partidas.html")

        # 3- Salvar no banco

        try:
            nova_partida = Partida(time_casa_id=int(time_casa_id),time_visitante_id= int(time_visitante_id), gols_casa= int(gols_casa), gols_visitante= int(gols_visitant), data_partida= date(data_partida))

            db_session.add(nova_partida)
            db_session.commit()
            flash('Partida adicionada com Sucesso', 'success')

        except SQLAlchemyError as e:
            db_session.rollback()
            flash('Erro ao adicionar jogador', 'error')

        except Exception as e:
            db_session.rollback()
            flash('Erro inesperado', 'error')
            print(f'Erro: {e}')

    return render_template("partidas.html", partidas=[], times=[])


if __name__ == "__main__":
    app.run(debug=True)
