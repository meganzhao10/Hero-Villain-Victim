from flask import Flask, jsonify, request
from role_assignment import assign_roles, NewspaperError

app = Flask(__name__)


# Allow cross-origin resource sharing
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


# Run role assignment algorithm
@app.route('/')
def role_assignment():
    url = request.args.get("url")
    try:
        role_names, top_words = assign_roles(url, 0.2, 0.1)
        top_entity_names = []
        for name in role_names:
            name_string = name if name else "None"
            top_entity_names.append(name_string)
        return jsonify(top_entity_names, top_words)
    except NewspaperError:
        return jsonify("Extraction error")
    except:
        return jsonify("Entity recognition/role assignment errors")


if __name__ == '__main__':
    app.run(debug=True)
