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
  if os.path.isfile("dati/pulcini.json") and os.path.getsize("dati/pulcini.json") > 0:  
    with open("dati/pulcini.json", "r",encoding='utf-8') as f:
      # ielasām un pārvēršam par json
      dati = json.loads(f.read())
    # veidojas skolotajuTabula.json
      if os.path.isfile("dati/skolotajuTabula.json") and os.path.getsize("dati/skolotajuTabula.json") > 0:
        with open("dati/skolotajuTabula.json", "r", encoding='utf-8') as g:
          skolotaji = json.loads(g.read()) 
      else:
        skolotaji=[]
      for ieraksts in dati:
        sk={"skolotID": ieraksts["id"],"skolotajs":ieraksts["skolotajs"],"epasts":ieraksts["epasts"],"talrunis":ieraksts["talrunis"]}  
        skolotaji.append(sk)
    with open("dati/skolotajuTabula.json", "w", encoding='utf-8') as f:
      f.write(json.dumps(skolotaji,ensure_ascii=False))
    
    # veidojas pulcTabula.json
      if os.path.isfile("dati/pulcTabula.json") and os.path.getsize("dati/pulcTabula.json") > 0:
        with open("dati/pulcTabula.json", "r", encoding='utf-8') as g:
          pulcini = json.loads(g.read()) 
      else:
        pulcini=[]

      for ieraksts in dati:
        pulc={
          "pulcID": ieraksts["id"],
          "skolotID":ieraksts["id"],
          "iicID":ieraksts["id"],
          "nosaukums":ieraksts["nosaukums"],
          "joma":ieraksts["joma"],
          "maxAudzekni":ieraksts["maxAudzekni"],
          "vecums":ieraksts["vecums"]
          }  
        pulcini.append(pulc)
    with open("dati/pulcTabula.json", "w", encoding='utf-8') as g:
      g.write(json.dumps(pulcini,ensure_ascii=False))
    
    
    # veidojas laikaTabula.json
    if os.path.isfile("dati/laikaTabula.json") and os.path.getsize("dati/laikaTabula.json") > 0:
      with open("dati/laikaTabula.json", "r", encoding='utf-8') as f:
        laiki = json.loads(f.read()) 
    else:
      laiki=[]

    for d in dati:
      jauns={"pulcID": d["id"],"skolotID": d["id"],"adrese":d["adrese"],"stunduSkaits":d["stunduSkaits"],"laiks":d["laiks"]}  
      laiki.append(jauns)

    with open("dati/laikaTabula.json", "w", encoding='utf-8') as f:
      f.write(json.dumps(laiki,ensure_ascii=False)) 
  return jsonify(laiki) 






@app.route('/registret_IIC')
def regIIC():
  return 1

if __name__ == "__main__":

  files = [
    "dati/laikaTabula.json",
    "dati/pulcTabula.json",
    "dati/skolotajuTabula.json"]

  for file in files:
    if os.path.isfile(file):
      os.remove(file)

  app.run("0.0.0.0", debug=True)