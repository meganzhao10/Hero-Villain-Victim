from flask import Flask, jsonify, request
import entity_recognition
import role_assignment

app = Flask(__name__)


# allow cross-origin resource sharing
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/')
def top_entities():
    url = request.args.get("url")
    headline, article = role_assignment.extract_by_newspaper(url)
    top_entities = entity_recognition.get_top_entities(headline, article)
    top_entity_names = [entity.name for entity in top_entities]
    return jsonify(top_entity_names)


if __name__ == '__main__':
    app.run(debug=True)
