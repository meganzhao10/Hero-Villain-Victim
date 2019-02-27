from flask import Flask, jsonify, request
from nltk import pos_tag, sent_tokenize, word_tokenize
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
    # headline, article = role_assignment.extract_by_newspaper(url)
    # tokenized_article = sent_tokenize(article)
    # top_entities = entity_recognition.get_top_entities(headline, tokenized_article)
    # top_entity_names = [entity.name for entity in top_entities]
    # return jsonify(top_entity_names)
    try:
        top_entity_names_scores, top_words = role_assignment.main2(url, 0.2, 0.1)
        if top_entity_names_scores == top_words == 0:
            return jsonify("Extraction error")
        elif top_entity_names_scores == top_words == 1:
            return jsonify("Entity recognition/role assignment errors")
        else:
            top_entity_names = ["None", "None", "None"]
            for i in range(len(top_entity_names_scores)):
                if top_entity_names_scores[i]:
                    top_entity_names[i] = top_entity_names_scores[i][0]
            return jsonify(top_entity_names, top_words)
    except:
        return jsonify("Entity recognition/role assignment errors")



if __name__ == '__main__':
    app.run(debug=True)
