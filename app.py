from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import pymysql

app = Flask(__name__)

# Pasta para salvar imagens
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Configuração do Banco de Dados (MySQL)
db = pymysql.connect(
    host="localhost",
    user="seu_usuario",
    password="sua_senha",
    database="checklist_db"
)

@app.route("/upload", methods=["POST"])
def upload():
    tecnico = request.form.get("tecnico")
    descricao = request.form.get("descricao")
    imagens = request.files.getlist("imagens")

    if not tecnico or not descricao or not imagens:
        return jsonify({"mensagem": "Todos os campos são obrigatórios!"}), 400

    cursor = db.cursor()

    # Salvar imagens no servidor e banco de dados
    imagens_salvas = []
    for imagem in imagens:
        filename = secure_filename(imagem.filename)
        caminho_imagem = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        imagem.save(caminho_imagem)
        imagens_salvas.append(filename)

    # Salvar no banco de dados
    sql = "INSERT INTO checklists (tecnico, descricao, imagens) VALUES (%s, %s, %s)"
    cursor.execute(sql, (tecnico, descricao, ",".join(imagens_salvas)))
    db.commit()

    return jsonify({"mensagem": "Formulário enviado com sucesso!"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
