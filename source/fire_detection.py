import requests
from dotenv import load_dotenv
import os


def detect_fire(file):
    load_dotenv()

    API_URL = "https://api-inference.huggingface.co/models/EdBianchi/vit-fire-detection"
    API_TOKEN = os.environ["API_TOKEN"]

    # berisi header permintaan HTTP yang akan digunakan dalam permintaan API. Header Authorization akan berisi token API yang digunakan untuk otentikasi
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    # melakukan permintaan ke API menggunakan metode POST. Fungsi ini menerima argumen file, yang merupakan path file gambar yang akan dikirim ke model

    data = file.read()

    response = requests.post(API_URL, headers=headers, data=data)
    output_json = response.json()

    for i, data in enumerate(output_json):
        if data["label"] == "Fire":
            fireScore = output_json[i]["score"]
        if data["label"] == "Normal":
            normalScore = output_json[i]["score"]
        if data["label"] == "Smoke":
            smokeScore = output_json[i]["score"]

    return [fireScore, normalScore, smokeScore]
