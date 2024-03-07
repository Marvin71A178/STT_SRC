FROM storyteller123/cuda118_cudnn_pytorch210_simpletransformer:latest
COPY . /mood_analized/
RUN pip install fastapi
RUN pip install uvicorn psutil
RUN pip install python.dotenv
WORKDIR /mood_analized/
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8050"]