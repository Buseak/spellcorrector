from flask import Flask, json, g, request, jsonify, json
import spellcorrector

app = Flask(__name__)

@app.route("/evaluate", methods=["POST"])
def correct_spelling():
    json_data = json.loads(request.data)
    spellcorrector_instance = spellcorrector.SpellCorrector()
    response=spellcorrector_instance.correct_spelling(json_data['text'])

    result = {"Response": response}
    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0',threaded=False,)

