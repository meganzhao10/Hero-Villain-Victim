from flask import Flask, render_template, jsonify, request  # TODO remove jsonify if remains unused
import entity_recognition

app = Flask(__name__)


# allow cross-origin resource sharing
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/')
def comps():
    return render_template('index.html')


@app.route('/newssite/')
def top_entities():
    url = request.args.get("url")
    top_entities = entity_recognition.get_top_entities(url)
    top_entity_names = [entity.name for entity in top_entities]
    # return tuple(top_entities_name)
    return "\n".join(top_entity_names)
    # return render_template('results.html', top_entities_name = top_entities_name)

# TODO remove old app routes used for testing
'''
@app.route('/randomPoints/<number>/')
def getRandomData(number):
    number = int(number)
    colors = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628']
    data = []
    for i in range(number):
        point = {}
        point['x'] = random.randint(1,400)
        point['y'] = random.randint(1,400)
        point['r'] = random.randint(5,10)
        point['c'] = random.choice(colors)
        data.append(point)
    return jsonify({'data':data})


@app.route('/random/<number>')
def random_points(number):
    return render_template('index.html', number = number)

host = sys.argv[1]
port= sys.argv[2]
app.run(host=host, port=port)
'''

if __name__ == '__main__':
    app.run(debug=True)
