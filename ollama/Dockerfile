FROM ollama/ollama:latest

EXPOSE 11434

ARG MODEL_NAME=llama:instruct

# Run ollama serve in the background, wait for 5 seconds, then pull the specified model
RUN ollama serve & sleep 5 && \
    model_name=${MODEL_NAME}  && \
    ollama pull $model_name && \
    echo ${pwd} && \
    echo "Killing 'ollama serve' process" && \
    ps -ef | grep 'ollama serve' | grep -v grep | awk '{print $2}' | xargs -r kill -9