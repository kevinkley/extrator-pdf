import fitz  # PyMuPDF
from flask import Flask, request, jsonify

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Define a rota da API. A Vercel usa /api/ [nome do arquivo]
@app.route('/api/extract_pdf', methods=['POST'])
def extract_pdf():
    try:
        # 1. Verifica se um arquivo foi enviado na requisição
        if 'file' not in request.files:
            return jsonify({"error": "Nenhum arquivo encontrado"}), 400

        file = request.files['file']

        # 2. Lê o arquivo PDF em memória
        pdf_bytes = file.read()
        
        # 3. Abre o PDF com PyMuPDF (fitz)
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        full_text = ""
        
        # 4. Itera por todas as páginas e extrai o texto
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            full_text += page.get_text()
            
        doc.close()

        # 5. Retorna o texto extraído em um JSON
        return jsonify({
            "extracted_text": full_text
        })

    except Exception as e:
        # Retorna um erro genérico se algo falhar
        return jsonify({"error": f"Erro ao processar o PDF: {str(e)}"}), 500

# Esta rota é usada pela Vercel para testes
@app.route('/', methods=['GET'])
def home():
    return "API de Extração de PDF está no ar. Use o endpoint POST /api/extract_pdf"