
import requests
from bs4 import BeautifulSoup
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from transformers import AutoTokenizer
from langchain_huggingface import HuggingFaceEmbeddings 
import chromadb
from langchain_chroma import Chroma
import ollama
from langchain_ollama.llms import OllamaLLM
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

url = "https://en.wikipedia.org/wiki/2024_Formula_One_World_Championship"

# realizar solicitud http
respuesta = requests.get(url)
pagina = BeautifulSoup(respuesta.text, 'html.parser')

# tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# extraer textos de la página
textos = [p.text for p in pagina.find_all('p')]

textos_limpios = [texto.strip() for texto in textos]
textos_minusculas = [texto.lower() for texto in textos_limpios]
textos_sin_caracteres_especiales = [re.sub(r'[^A-Za-z0-9\s]', '', texto) for texto in textos_minusculas]
textos_sin_stopwords = [' '.join([word for word in texto.split() if word not in ENGLISH_STOP_WORDS]) for texto in textos_sin_caracteres_especiales]
textos_tokenizados = [tokenizer.tokenize(texto) for texto in textos_sin_stopwords]

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# base de datos vectorial
vector_store = Chroma.from_texts(
    texts=textos_limpios, 
    collection_name="web_data", 
    embedding=embeddings, 
    persist_directory="./chroma_web_data"
)

# crea el retriever
recuperador = vector_store.as_retriever()

# definir la plantilla del prompt 
plantilla = """Answer the question based only on the following context: 
{context} 

Question: {question} 
""" 
prompt = ChatPromptTemplate.from_template(plantilla) 

# seleccionar el modelo 
modelo_local = OllamaLLM(model="gemma:2b", base_url='http://localhost:11434')

# crear la cadena RAG
cadena = ( 
    {"context": recuperador, "question": RunnablePassthrough()} 
    | prompt 
    | modelo_local 
    | StrOutputParser() 
)

