from flask import Flask, render_template, request, redirect
from bd import login, BuscarPorArea, BuscarTodosProdutos, criarConexao, BuscarHistoricoVendas

app = Flask(__name__)
user = {}

@app.route('/')
def index():
    return render_template('login.html', e=False)

@app.route('/logar', methods=['POST'])
def logar():
    global user
    usuario = request.form['id']
    senha = request.form['password']

    user = login(usuario, senha)

    if "erro" in user:
        return render_template('login.html', e=True)
    else:
        return redirect('/fabrica')
    
@app.route('/logout')
def logout():
    return redirect('/')

@app.route('/fabrica')
def fabrica():
    if user:
        nome = user['nome']
        funcao = user['funcao']
        return render_template('fabrica.html', user=user, nome=nome, funcao=funcao)
    else:
        return redirect('/')
    
@app.route('/area/<int:area>')
def areas(area):
    produtosArea = BuscarPorArea(area)
    return render_template('area.html', produtosArea=produtosArea, area=area)

@app.route('/vendas/<int:idProduto>')
def vendas(idProduto):
    produtos = BuscarTodosProdutos()
    produto = next((p for p in produtos if p['idProduto'] == idProduto), None)  # Buscar o produto específico
    return render_template('vendas.html', produtos=produtos, idProduto=idProduto, produto=produto)

@app.route('/submit', methods=['POST'])
def realizar_venda():
    quantidade = int(request.form['Quantidade'])
    destino = request.form['Destino']
    produto_id = request.form['produto_id']

    conexao = criarConexao()
    cursor = conexao.cursor()

    # Verificando a quantidade disponível do produto
    cursor.execute("SELECT quantidade FROM produtos WHERE idProdutos = %s;", (produto_id,))
    resultado = cursor.fetchone()

    if resultado is None:
        return "Produto não encontrado", 404

    quantidade_disponivel = resultado[0]

    if quantidade > quantidade_disponivel:
        return "Quantidade solicitada maior do que a disponível", 400

    # Atualizando a quantidade no banco de dados
    cursor.execute("UPDATE produtos SET quantidade = quantidade - %s WHERE idProdutos = %s;", (quantidade, produto_id))

    # Registrando a venda no histórico
    cursor.execute("INSERT INTO vendas (idProdutos, quantidadeVendida, destino, dataHora) VALUES (%s, %s, %s, NOW());", (produto_id, quantidade, destino))
    
    conexao.commit()
    cursor.close()
    conexao.close()

    return redirect('/fabrica')  # Redirecionar após a venda

@app.route('/historico')
def historico():
    vendas = BuscarHistoricoVendas()
    return render_template('historico.html', vendas=vendas)
    
if __name__ == '__main__':
    app.run(debug=True)