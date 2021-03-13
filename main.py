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

@app.route('/pulcina_info')
def pulcina_info():
  return render_template('pulcina_info.html')  
  
@app.route('/vecaku_pieteikums')
def vPieteikums():
  return render_template('vecaku_pieteikums.html')

# lasa no datnes vecaku_pieteikums.txt un parāda
@app.route('/vecaku_pieteikums/lasa', methods=['GET'])
def lasaDatus():
    with open("dati/vecaku_pieteikums.txt", "r",encoding='utf-8') as f:
      # ielasām un pārvēršam par json
      dati = json.loads(f.read())
    
    # pārveidojam par string pirms atgriežam
    return jsonify(dati)

# Pieraksta Vecāku pieteikuma datus klāt esošā datnē vecPietGatavs.json
@app.route('/vecaku_pieteikums',methods=['POST'])
def jaunsPieteikums():
    with open("dati/vecPietGatavs.json", "r", encoding='utf-8') as f:
      dati = json.loads(f.read())
    
    # ielasām ienākošos datus un pārvēršam par json
    jaunsPieteikums = json.loads(request.data)
    # šeit vajadzētu veikt pārbaudi vai ir visi nepieciešamie dati
    if len(jaunsPieteikums) < 13:
        return jsonify("Aizpildiet visus laukus!")
    # pievienojam jauno pieteikumu pie datiem
    dati.append(jaunsPieteikums)
    # ierakstam atjaunotos datus atpakaļ datnē
    with open("dati/vecPietGatavs.json", "w", encoding='utf-8') as f:
        # šeit nevar izmantot jsonify, jo rakstām datnē nevis atgriežam no Flask
        f.write(json.dumps(dati))
    # atgriežam jauno ID
    return jsonify(jaunsPieteikums)

# no Oksanas datnes iic.json nolasa un papildina ar formas datiem
@app.route('/registret_IIC', methods=['POST'])
def regIIC():
  with open("dati/iic.json", "r", encoding='utf-8') as f:
    dati = json.loads(f.read())
  jaunsIIC= json.loads(request.data)

  for d in dati:
    if d["klubs"]==jaunsIIC["klubs"]:
      #d["forma"]=render_template("forma.html")
      atbilde={"statuss":"Šī IIC jau ir reģistrēta"}
      atbilde["pulcins"]=render_template('pulcina_info.html')
      return jsonify(atbilde)
  
  if len(dati):
    visi_id = [iic['iicID'] for iic in dati]
    jaunsIIC['iicID']=int(max(visi_id))+1
  else:
    jaunsIIC['iicID']=0

  dati.append(jaunsIIC)

  with open("dati/iic.json", "w", encoding='utf-8') as f:
    f.write(json.dumps(dati))

  atbilde={"statuss":"IIC veiksmīgi piereģistrēta"}
  atbilde["pulcins"]=render_template('pulcina_info.html')
  return jsonify(atbilde)

# lasa no datnēm pulcTabula.json, laikaTabula.json, skolotajuTabula.json un 
#papildina tās ar datiem no formas pulcina_info.html
@app.route('/pulcini/lasa', methods=['POST'])
def lasaSkiroVisusDatus():
  print('Palaidaaaaaaaaaaaaaas')
  if os.path.isfile("dati/skolotajuTabula.json") and os.path.getsize("dati/skolotajuTabula.json") > 0:
    with open("dati/skolotajuTabula.json", "r", encoding='utf-8') as g:
      skolotaji = json.loads(g.read()) 
  else:
    skolotaji=[]
  if os.path.isfile("dati/laikaTabula.json") and os.path.getsize("dati/laikaTabula.json") > 0:
    with open("dati/laikaTabula.json", "r", encoding='utf-8') as g:
      laiki = json.loads(g.read()) 
  else:
    laiki=[]
  if os.path.isfile("dati/pulcTabula.json") and os.path.getsize("dati/pulcTabula.json") > 0:
    with open("dati/pulcTabula.json", "r", encoding='utf-8') as g:
     pulcini = json.loads(g.read()) 
  else:
    pulcini=[]

  jaunsPieteikums= json.loads(request.data)
  
  if len(skolotaji):
    visi_id = [skolot['skolotID'] for skolot in skolotaji]
    skolotID=int(max(visi_id))+1
  else:
    skolotID=0
  sk={
    "skolotID": skolotID,
    "skolotajs":jaunsPieteikums.get("skolotajs"),
    "epasts":jaunsPieteikums.get("epasts"),
    "talrunis":jaunsPieteikums.get("talrunis")
  } 
  skolotaji.append(sk)

  with open("dati/skolotajuTabula.json", "w", encoding='utf-8') as f:
    f.write(json.dumps(skolotaji,ensure_ascii=False))
    
  
  if len(pulcini):
    visi_id = [pulc['pulcID'] for pulc in pulcini]
    pulcID=int(max(visi_id))+1
  else:
    pulcID=0
  
  # veidojas pulcTabula.json
  pulc={
      "pulcID": pulcID,
      "skolotID":skolotID,       
      "nosaukums":jaunsPieteikums.get("nosaukums"),
      "joma":jaunsPieteikums.get("joma"),
      "stunduSkaits":jaunsPieteikums.get("stunduSkaits"),
      "maxAudzekni":jaunsPieteikums.get("maxAudzekni"),
      "vecumsno":jaunsPieteikums.get("vecums").get("no"),
      "vecumslidz":jaunsPieteikums.get("vecums").get("lidz")
      }  
  pulcini.append(pulc)

  with open("dati/pulcTabula.json", "w", encoding='utf-8') as g:
    g.write(json.dumps(pulcini,ensure_ascii=False))
  
  # veidojas laikaTabula.json
  
  for ieraksts in jaunsPieteikums.get("laiks"):
    jauns={
      "pulcID": pulcID,
      "skolotID": skolotID,
      "adrese":jaunsPieteikums.get("adrese"),
      "diena":ieraksts.get("diena"),
      "lidz":ieraksts.get("lidz"),
      "no":ieraksts.get("no")
    }  
    laiki.append(jauns)

  with open("dati/laikaTabula.json", "w", encoding='utf-8') as f:
    f.write(json.dumps(laiki,ensure_ascii=False)) 
  return jsonify(laiki) 


if __name__ == "__main__":
  # šis un for jāizdzēš
  #files = [
  # "dati/pulcTabula.json",
  # "dati/skolotajuTabula.json"]

  # for file in files:
  #  if os.path.isfile(file):
  #    os.remove(file)
  # faila dzesanas beigas

  app.run("0.0.0.0", debug=True)