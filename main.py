from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json

# Importa o módulo json para trabalhar com dados JSON.


app = Flask('carros')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# Configura o SQLAlchemy para rastrear modificações dos objetos, o que não é recomendado para produção.
# O SQLAlchemy cria e modifica todos os dados da nossa tabela de forma automatica 

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senai%40134@127.0.0.1/CarrosBD'
# Configura a URI de conexão com o banco de dados MySQL.
# Senha -> senai@134, porém aqui a senha passa a ser -> senai%40134

mybd = SQLAlchemy(app)
# Cria uma instância do SQLAlchemy, passando a aplicação Flask como parâmetro.


# A classe Carros define um modelo de dados que corresponde a uma tabela no banco de dados. Neste caso, a tabela representa carros.
class Carros(mybd.Model):
    id = mybd.Column(mybd.Integer, primary_key=True)
    marca = mybd.Column(mybd.String(50))
    modelo = mybd.Column(mybd.String(100))
    ano = mybd.Column(mybd.Integer)
    valor = mybd.Column(mybd.Numeric(10, 2))  # Ajustado para Numeric
    cor = mybd.Column(mybd.String(100))
    numero_Vendas = mybd.Column(mybd.Integer)
    
    # mybd.create_all()

# Objetivo: O método to_json é usado para converter um objeto Carros em um formato JSON. 
# Isso é útil quando você precisa enviar os dados do objeto como resposta de uma API, pois JSON é um formato amplamente 
# utilizado para troca de dados em web services.

# Uso: Quando você chama carro.to_json() em uma instância de Carros, o método retorna um dicionário contendo os dados do carro, 
# o que facilita a serialização do objeto em JSON para envio em respostas HTTP.

# Serialização é o processo de transformar um objeto em um formato que pode ser facilmente armazenado ou transmitido e depois 
# reconstruído. No contexto da web e das APIs, isso geralmente significa converter um objeto em um formato de texto, 
# como JSON (JavaScript Object Notation) ou XML (eXtensible Markup Language), que pode ser enviado através de uma rede.
    def to_json(self):
        return{"id":self.id, "marca": self.marca, "modelo": self.modelo, "ano": self.ano, "valor": float(self.valor), "cor": self.cor, "numero_Vendas": self.numero_Vendas}

# ********************************************************************************************************

# Selecionar Tudo
@app.route("/carros", methods=["GET"])
def seleciona_carro():
    carro_objetos = Carros.query.all()
# Executa uma consulta no banco de dados para obter todos os registros da tabela 'Carros'.
# O método 'query.all()' retorna uma lista de objetos 'Carros'
    carro_json = [carro.to_json() for carro in carro_objetos]
 # Cria uma lista de dicionários JSON.
 # Para cada objeto 'carro' na lista 'carro_objetos', chama o método 'to_json()' do objeto 'Carros' para convertê-lo em um dicionário.
    return gera_response(200, "carros", carro_json)
# Retorna a resposta HTTP gerada pela função 'gera_response'.
# O status da resposta é 200 (OK), o conteúdo é a lista 'carro_json' e a chave é 'carros'.

# ********************************************************************************************************

# Selecionar Individual
@app.route("/carros/<id>", methods=["GET"])
def seleciona_carro_id(id):
# O parâmetro 'id' será passado para a função a partir da URL.
    carro_objetos = Carros.query.filter_by(id=id).first()
# Executa uma consulta no banco de dados para obter o registro da tabela 'Carros' com o 'id' correspondente.
# O método 'filter_by(id=id)' Filtra os registros da tabela Carros pelo campo id igual ao valor passado como argumento.
# O método 'first()'  Retorna o primeiro registro que corresponde ao filtro ou None se nenhum registro for encontrado.
    carro_json = carro_objetos.to_json()
# Converte o objeto 'carro_objetos' em um dicionário JSON chamando o método 'to_json()' do objeto 'Carros'.

    return gera_response(200, "carros", carro_json)


# ********************************************************************************************************

# Cadastrar
@app.route("/carros", methods=["POST"])
def cria_carro():
    body = request.get_json()
# Obtém o corpo da requisição (esperado no formato JSON) e o armazena na variável 'body'.
# 'request.get_json()' converte o corpo da requisição em um dicionário Python.

    try:
        carro = Carros(id=body["id"], marca=body["marca"], modelo= body["modelo"], ano= body["ano"], valor= body["valor"], cor= body["cor"], numero_Vendas= body["numero_Vendas"])
# Tenta criar uma nova instância da classe Carros com os dados fornecidos no corpo da requisição. 
# Os valores de marca, modelo e ano são extraídos do dicionário body e passados como argumentos para criar o novo objeto carro.
        mybd.session.add(carro)
# Adiciona o novo objeto carro à sessão do banco de dados para ser inserido no banco de dados.
        mybd.session.commit()
# Confirma a transação no banco de dados, persistindo o novo registro.
        return gera_response(201, "carros", carro.to_json(), "Criado com sucesso")
# Retorna uma resposta HTTP gerada pela função gera_response. O status da resposta é 201 (Created), 
# o conteúdo é o dicionário JSON do novo carro (obtido através do método to_json), e a mensagem é "Criado com sucesso".
    except Exception as e:
        print('Erro', e)
# Em caso de exceção, imprime a mensagem de erro no console.
        return gera_response(400, "carros", {}, "Erro ao cadastrar")


# ********************************************************************************************************

# Atualizar
@app.route("/carros/<id>", methods=["PUT"])
def atualiza_carro(id):
    carro_objetos = Carros.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('marca' in body):
            carro_objetos.marca = body['marca']
        if('modelo' in body):
            carro_objetos.modelo = body['modelo']
        if('ano' in body):
            carro_objetos.ano = body['ano']
        if('valor' in body):
            carro_objetos.valor = body['valor']
        if('cor' in body):
            carro_objetos.cor = body['cor']
        if('numero_Vendas' in body):
            carro_objetos.numero_Vendas = body['numero_Vendas']
# Se a chave marca/modelo/ano estiver presente no corpo da requisição, atualiza o campo marca do objeto carro_objetos.
        mybd.session.add(carro_objetos)
# Adiciona o objeto carro_objetos atualizado à sessão do banco de dados.
        mybd.session.commit()
# Confirma a transação no banco de dados, persistindo as atualizações.
        return gera_response(200, "carros", carro_objetos.to_json(), "Atualizado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "carros", {}, "Erro ao atualizar")


# ********************************************************************************************************

# Deletar
@app.route("/carros/<id>", methods=["DELETE"])
def deleta_carro(id):
    carro_objetos = Carros.query.filter_by(id=id).first()

    try:
        mybd.session.delete(carro_objetos)
# Remove o objeto carro_objetos da sessão do banco de dados.
        mybd.session.commit()
# Confirma a transação no banco de dados, efetivando a exclusão do registro.
        return gera_response(200, "carros", carro_objetos.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "carros", {}, "Erro ao deletar")
    
# ********************************************************************************************************

def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
# Define uma função chamada 'gera_response' que cria uma resposta HTTP.
# A função aceita quatro parâmetros:
# - status: Código de status HTTP (por exemplo, 200, 201, 400, etc.).
# - nome_do_conteudo: Nome da chave que será usada no dicionário de resposta.
# - conteudo: O conteúdo a ser incluído na resposta.
# - mensagem: Uma mensagem opcional a ser incluída na resposta. O valor padrão é False.
    body = {}
# Inicializa um dicionário vazio chamado 'body'.
    body[nome_do_conteudo] = conteudo
# Adiciona uma entrada ao dicionário 'body' com a chave sendo 'nome_do_conteudo' e o valor sendo 'conteudo'.
    if(mensagem):
        body["mensagem"] = mensagem
# Se o parâmetro 'mensagem' foi fornecido (não é False), adiciona uma entrada ao dicionário 'body'
# com a chave "mensagem" e o valor sendo 'mensagem'.
    return Response(json.dumps(body), status=status, mimetype="application/json")
# Converte o dicionário 'body' em uma string JSON usando 'json.dumps'.
# O dumps é uma função do módulo json da biblioteca padrão do Python, usada para converter um objeto Python em uma string no formato JSON

# Cria um objeto de resposta HTTP usando 'Response'.
# Define o código de status da resposta para 'status'.
# Define o tipo MIME da resposta para "application/json".
# Retorna o objeto de resposta.

app.run(port=5000, host='localhost', debug=True)
