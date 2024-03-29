# test.py
import Music.api.demos.predict as music_pd

def main():
    music_pd.load_model()
    a = music_pd._do_predictions(texts=['I am so happy in such a good day.'] , duration = 20)
    print(a)
    print(type(a))

if __name__ == "__main__":
    main()
