from flask import Flask, render_template, request, jsonify
from source.fire_detection import detect_fire
from source.handle_image import get_uri, read_image, open_image, UMatToPIL
from source.fire_segmentation import combinate_hsv_threshold

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/process_image", methods=["POST"])
def process():
    if request.method == "POST":
        file = request.files["file-image"]

        if file:
            output = detect_fire(file)

            return jsonify(
                {
                    "html": render_template(
                        "firepercentage.html",
                        converted=get_uri(
                            UMatToPIL(combinate_hsv_threshold(read_image(file)))
                        ),
                        firescore=output[0],
                        normalscore=output[1],
                        smokescore=output[2],
                    )
                }
            )


@app.route("/example")
def example():
    return render_template("example.html")


@app.route("/<not_found>")
def notfound(not_found):
    return render_template("notfound.html")


if __name__ == "__main__":
    app.run(debug=True)
