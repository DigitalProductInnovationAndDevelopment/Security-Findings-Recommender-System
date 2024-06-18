FROM ollama/ollama:latest

# Run ollama serve in the background, wait for 5 seconds, then pull the specified model
RUN ollama serve & sleep 5 && \
    model_name=llama3:instruct && \
    ollama pull $model_name && \
    echo ${pwd} && \
    echo "Killing 'ollama serve' process" && \
    ps -ef | grep 'ollama serve' | grep -v grep | awk '{print $2}' | xargs -r kill -9