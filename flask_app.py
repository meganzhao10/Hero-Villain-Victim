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
    headline, article = role_assignment.extract_by_newsplease(url)
    top_entities = entity_recognition.get_top_entities(headline, article)
    top_entity_names = [entity.name for entity in top_entities]
    print(top_entity_names)
    # return tuple(top_entities_name)
    # return "\n".join(top_entity_names)
    return jsonify(top_entity_names)
    # return render_template('results.html', top_entities_name = top_entities_name)


if __name__ == '__main__':
    app.run(debug=True)
