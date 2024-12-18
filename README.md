# Sistemas_RAG_BDA

docker network create ollama_network
docker run -d -v ollama://root/.ollama -p 11434:11434 --name ollama --net=ollama_network ollama/ollama
docker exec -it ollama ollama run gemma:2b &
