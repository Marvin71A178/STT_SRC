FROM storyteller123/cuda118_cudnn_pytorch210_simpletransformer
WORKDIR /src/
COPY ./audiocraft/ /src/
USER root

RUN python3 -m pip install --upgrade pip
RUN cd audiocraft
RUN python3 -m pip install -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg
RUN pip3 install -U xformers --index-url https://download.pytorch.org/whl/cu118
RUN pip3 install torchaudio==2.2.1+cu118 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install torchvision==0.17.1+cu118 -f https://download.pytorch.org/whl/torch_stable.html
