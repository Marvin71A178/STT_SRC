activate python venv 
    C:/Marvin/env/Scripts/activate.ps1


gdown mood analyzation dataset 
    gdown --id 1ryICuZAnZPVhO1ncrImRt9yiFYy7Nzg2

docker run --gpus all -it --name audiocraft_test318 story_img_audiocraft bash
python3 -m demos.musicgen_app --share
docker run --gpus all -it --name audiocraft_container7860 -p 7860:7860 story_img_audiocraft_xformers bash