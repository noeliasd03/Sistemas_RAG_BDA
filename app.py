import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from transformers import AutoTokenizer
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.llms import OllamaLLM
from langchain_core.runnables import RunnablePassthrough

app = Flask(__name__)

client = MongoClient(os.environ['MONGO_URI'])
db = client['sample_airbnb']
collection = db['listingsAndReviews']  

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

vector_store = Chroma.from_mongo_collection(
    collection,
    embedding=embeddings
)

retriever = vector_store.as_retriever()

prompt_template = """Responde a la pregunta basándote únicamente en el siguiente contexto:
{context}

Pregunta: {question}
"""
prompt = ChatPromptTemplate.from_template(prompt_template)
model = OllamaLLM(model="gemma:2b", base_url='http://localhost:11434')

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    question = data['question']
    response = chain.invoke(question)
    return jsonify({'answer': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

