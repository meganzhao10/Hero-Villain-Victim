from flask import Flask, render_template, jsonify, request
import ./entity_recognition
import sys

#import psycopg2
import json
app = Flask(__name__)


@app.route('/')
def comps():
    return render_template('index.html')


#@app.route('/results/', methods = ["POST", "GET"])
#def test():
#    name = ""
#    normalized_name = ""
#    top = entity_recognition.Entity(name, normalized_name, sentence_number=None, index_list=None, headline=False, headline_index_list=None)
#    return render_template('index.html')


@app.route('/getURL',methods = ["POST", "GET"])
def getURL():
    if request.method == 'POST':
        url= request.form["url"]
        #headline = "Armistice Day: Macron and Merkel mark end of World War One"
        #article = "French President Emmanuel Macron and German Chancellor Angela Merkel have left their own mark of reconciliation at the start of events to mark the centenary of the end of World War One. They signed a book of remembrance in a railway carriage identical to the one in which the 1918 Armistice was sealed. US President Donald Trump is among world leaders attending the events. But Mr Trump caused controversy by cancelling a trip to a US cemetery on Saturday because of bad weather. The day had a tense beginning amid a row between Mr Trump and Mr Macron over European defence. The French leader said the EU needed a joint army now that the US was pulling out of a key disarmament treaty with Russia. Mr Trump described the comments as insulting and said Europe should pay its share of costs within Nato, the Euro-Atlantic alliance. After a meeting at the Elysée Palace, Mr Macron said he agreed that Europe should pay more. Mrs Merkel became the first German leader since World War Two to visit the forest near the town of Compiègne in northern France where the Armistice was signed. She and Mr Macron unveiled a plaque to Franco-German reconciliation, laid a wreath and signed a book of remembrance in a railway carriage similar to that used 100 years ago. "
        
        top_entities = entity_recognition.get_top_three_entities(url) 
        
        #return jsonify({"top_entities": [entity.name for entity in top_entities]})
        top_entities_name = {}
        for i in range(3):
            top_entities_name[i] = top_entities[i].name
    return render_template('results.html', top_entities_name = top_entities_name)

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
'''
#
#host = sys.argv[1]
#port= sys.argv[2]
#app.run(host=host, port=port)
#

if __name__=='__main__':
    app.run(debug=True)
