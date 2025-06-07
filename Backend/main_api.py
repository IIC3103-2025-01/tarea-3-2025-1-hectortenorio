from flask import Flask, request, jsonify
from flask_cors import CORS
from scraping import ejecutar_scraping
from embedding_class import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_postgres import PGVector
import requests
import os

modelo_llm_url = "https://asteroide.ing.uc.cl"


db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_database = os.environ.get("DB_NAME")
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT", "5432")

app = Flask(__name__)
CORS(app)


embedding = Embeddings()

vectorstore = PGVector(
    embeddings=embedding,
    collection_name="wikipedia_chunks",
    connection=f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}",
    use_jsonb=True,
)


@app.route('/')
def home():
    return "Flask está funcionando"


@app.route("/scrape", methods=["POST"])
def scraping_endpoint():
    data = request.get_json()
    url = data.get("url")
    
    if not url:
        return jsonify({"error": "No se proporciono una url valida'"}), 400

    resultado = ejecutar_scraping(url)

    if "error" in resultado:
        return jsonify(resultado), 400
    
    contenido = resultado.get("contenido", "")

    if isinstance(contenido, list):
        raw_text = "\n".join(contenido)
    else:
        raw_text = contenido


    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    chunks = splitter.split_text(raw_text)

    documents = []
    ids = []
    for numero_de_chunk in range(len(chunks)):
        doc = Document(page_content=chunks[numero_de_chunk], metadata={"url": url, "index": numero_de_chunk})
        documents.append(doc)
        ids.append(f"{url}_{numero_de_chunk}")

    global vectorstore
    vectorstore.delete(ids=None)
    print("se ejecuta esta linea")
    vectorstore.delete_collection()
    vectorstore = PGVector(
        embeddings=embedding,
        collection_name="wikipedia_chunks",
        connection=f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}",
        use_jsonb=True,
    )

    vectorstore.add_documents(documents, ids=ids)

    return jsonify({"mensaje": f"Scraping y embeddings completados. Total chunks: {len(chunks)}"})


@app.route("/talk", methods=["POST"])
def send_to_model():
    data = request.get_json()
    user_prompt = data.get("pregunta")

    print("no se ejecuta la funcion basica")
    if not user_prompt:
        print("error en el prompt")
        print(user_prompt)
        return jsonify({"error": "No se proporcionó un prompt"}), 400

    print(" print error post prompt")
    try:
        documentos_relevantes = vectorstore.similarity_search(user_prompt, k=3)
        contexto = "\n".join([doc.page_content for doc in documentos_relevantes])
    except Exception as e:
        return jsonify({"error": f"Error al buscar en PGVector: {str(e)}"}), 500

    # 2. Concatenar el contexto con el prompt del usuario
    print("se ejecuto el endpoint")
    prompt_con_contexto = f"""
    Usa el siguiente contexto para responder la pregunta:

    {contexto}

    Pregunta: {user_prompt}
    """

    # 3. Enviar el prompt completo al modelo LLM
    try:
        response = requests.post(
            "https://asteroide.ing.uc.cl/api/generate",
            json={
                "model": "integracion",
                "prompt": prompt_con_contexto,
                "stream": False
            },
            timeout=120
        )

        if response.status_code != 200:
            return jsonify({"error": "Error al comunicarse con el modelo"}), 500

        print("Entre al try para la api")
        respuesta_llm = response.json().get("response", "")
        return jsonify({"respuesta": respuesta_llm})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error de conexión: {str(e)}"}), 500



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
    