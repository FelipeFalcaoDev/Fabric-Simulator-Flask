import mysql.connector
import mysql.connector.errors

def criarConexao():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',
            password='',
            database='fabrica'
        )
        return conexao
    except mysql.connector.errors.IntegrityError as error:
        print("Erro de integridade: ", error)
        return None

def login(usuario, senha):
    conexao = criarConexao()

    if conexao is None:
        return {"erro": True}
    else:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE idUsuarios = %s AND senha = %s;", [usuario, senha])
        resultado = cursor.fetchall()

        usuario = {}

        if len(resultado) > 0:
            usuario['id'] = resultado[0][0]
            usuario['nome'] = resultado[0][1]
            usuario['funcao'] = resultado[0][2]
        else:
            usuario["erro"] = True
            
        cursor.close()
        conexao.close()

        return usuario
    
def BuscarPorArea(area):
    conexao = criarConexao()

    if conexao is None:
        return False
    else:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM produtos WHERE area = %s;", (area,))
        resultado = cursor.fetchall()
        produtos = {}
        for i in range(len(resultado)):
            produtos[resultado[i][0]] = {
                "idProduto": resultado[i][0],
                "nomeProduto": resultado[i][1],
                "quantidade": resultado[i][2],
                "lote": resultado[i][3],
                "dataValidade": resultado[i][4],
                "area": resultado[i][5]
            }
        return produtos

def BuscarTodosProdutos():
    conexao = criarConexao()

    if conexao is None:
        return []

    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos")
    resultado = cursor.fetchall()

    produtos = []
    for linha in resultado:
        produtos.append({
            "idProduto": linha[0],
            "nomeProduto": linha[1],
            "quantidade": linha[2]
        })
    return produtos

def BuscarHistoricoVendas():
    conexao = criarConexao()

    if conexao is None:
        return []

    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM vendas")  # Busca todas as vendas realizadas
    resultado = cursor.fetchall()

    vendas = []
    for linha in resultado:
        vendas.append({
            "idVenda": linha[0],
            "idProduto": linha[1],
            "quantidade": linha[2],
            "destino": linha[3],
            "data": linha[4]
        })
    return vendas     

print(criarConexao())