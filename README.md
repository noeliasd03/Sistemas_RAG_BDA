# Proyecto de Construcción de RAGs

Este proyecto construye estos diferentes RAGs:

1. **RAG en inglés** que crea un vector store a partir de datos de una página web.
2. **RAG en castellano** que crea un vector store a partir de uno o varios archivos PDF.
3. **Crear una GUI** para el RAG número 1.
4. **RAG dockerizado contra Mongo Atlas.**

## Crear el Entorno para el Proyecto y clonar el repositorio

Asegúrate de tener Python 3.8 instalado:   
Creamos y activamos el entorno:
```bash
conda create -n rags python=3.8
conda activate rags
```
Instalamos las dependencias (requirements.txr) dentro de nuestro entorno:
```bash
conda install pip
pip install -r requirements.txt
```
Clonar el repositorio:
```bash
git clone https://github.com/noeliasd03/Sistemas_RAG_BDA.git
cd Sistemas_RAG_BDA
```

### Tener el servidor funcionando
Tenemos que crear un servidor de Ollama del que extraeremos nuestro modelo LLM para nuestros RAGs:
```bash
docker network create ollama_network
docker run -d -v ollama://root/.ollama -p 11434:11434 --name ollama --net=ollama_network ollama/ollama
```
Extraemos el modelo LLM para nuestro proyecto en segund plano: Gemma:2b, un LLM ligero: (Espera un par de minutos antes de ejecutar los notebooks para asegurarte que se descargó todo el LLM)
```bash
docker exec -it ollama ollama run gemma:2b &
```

### Ya se pueden ejecutar los notebooks

## 1. RAG en Inglés

**Descripción**: Este RAG crea un vector store a partir de los datos obtenidos de una página web en inglés. Utiliza técnicas de scraping para extraer textos, los procesa y los almacena en una base de datos vectorial. Finalmente, utiliza un modelo de lenguaje para responder preguntas basadas en el contenido extraído.

**Implementación**: Sólo hay que seguir las instrucciones del notebook: 1_RAG_web.ipynb

## 2. RAG en Castellano

**Descripción**: Este RAG crea un vector store a partir de uno o varios archivos PDF en castellano. Procesa los textos contenidos en los PDFs y los almacena en una base de datos vectorial. Luego, utiliza un modelo de lenguaje para responder preguntas basadas en el contenido de los PDFs.

**Implementación**: Sólo hay que seguir las instrucciones del notebook: 2_RAG_pdf.ipynb

## 3. Crear una GUI

**Descripción**: Este notebook se centra en crear una interfaz gráfica de usuario (GUI) para uno de los RAGs anteriores. La GUI permite a los usuarios interactuar con el RAG de manera visual e intuitiva.

**Implementación**: Sólo hay que seguir las instrucciones del notebook: 3_RAG_GUI.ipynb

## 4. RAG Dockerizado contra Mongo Atlas

**Descripción**: Este RAG está configurado para funcionar en un entorno Docker y utilizar Mongo Atlas como base de datos. Integra todos los componentes del RAG en un contenedor Docker y almacena los datos en Mongo Atlas, lo que permite una implementación escalable y distribuida.

**Implementación**: Primero hay que construír la imagen de docker:
```bash
docker-compose build
```
Iniciar el contenedor Docker:
```bash
docker-compose up -d
```
Verificar el funcionamiento:
```bash
docker ps
```
Realizar consultas:
```bash
curl -X POST http://localhost:5000/query -H "Content-Type: application/json" -d '{"question": "¿Cuántos listados hay en Nueva York?"}'
```
