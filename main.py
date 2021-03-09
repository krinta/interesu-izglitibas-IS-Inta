from flask import Flask, json, jsonify, render_template, request
import dati
import os
app = Flask(__name__)
app.config['JSON_AS_ASCII']=False

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/skolenu_izvelne')
def skIzvele():
  return render_template('skolenu_izvelne.html')

@app.route('/IIC')
def iic():
  return render_template('IIC.html')  
  
@app.route('/vecaku_pieteikums')
def vPieteikums():
  return render_template('vecaku_pieteikums.html')

# lasa no datnes un parāda
@app.route('/vecaku_pieteikums/lasa', methods=['GET'])
def lasaDatus():
    # atveram datni
    with open("dati/vecaku_pieteikums.txt", "r",encoding='utf-8') as f:
        # ielasām un pārvēršam par json
        dati = json.loads(f.read())
    
    # pārveidojam par string pirms atgriežam
    return jsonify(dati)

# Pieraksta datus klāt esošā datnē
@app.route('/vecaku_pieteikums',methods=['POST'])
def jaunsPieteikums():
    # atveram datni, lai ielasītu esošos datus
    with open("dati/vecPietGatavs.json", "r", encoding='utf-8') as f:
        # ielasām un pārvēršam par json
        dati = json.loads(f.read())
    
    # ielasām ienākošos datus un pārvēršam par json
    jaunsPieteikums = json.loads(request.data)
    #print(jaunsPieteikums["vecVards"])
    # šeit vajadzētu veikt pārbaudi vai ir visi nepieciešamie dati
    if len(jaunsPieteikums) < 13:
        return jsonify("Aizpildiet visus laukus!")
    # pievienojam jauno vielu pie datiem
    dati.append(jaunsPieteikums)
    # ierakstam atjaunotos datus atpakaļ datnē
    with open("dati/vecPietGatavs.json", "w", encoding='utf-8') as f:
        # ielasām un pārvēršam par json
        # šeit nevar izmantot jsonify, jo rakstām datnē nevis atgriežam no Flask
        f.write(json.dumps(dati))
    # atgriežam jauno ID
    return jsonify(jaunsPieteikums)

# lasa no datnes pulcini.json un parāda
@app.route('/pulcini/lasa', methods=['GET'])
def lasaVisusDatus():
    # atveram datni
    with open("dati/pulcini.json", "r",encoding='utf-8') as f:
      # ielasām un pārvēršam par json
      dati = json.loads(f.read())
    # pārveidojam par string pirms atgriežam
    #return jsonify(dati)
    rezultats = []
    for ieraksts in dati:
      rezultats.append(ieraksts['laiks'])
#append vai extend
    

    return jsonify(rezultats)




@app.route('/registret_IIC')
def regIIC():
  return 1

if __name__ == "__main__":
   app.run("0.0.0.0", debug=True)