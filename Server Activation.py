from flask import Flask,render_template,request

app = Flask(__name__,static_folder='./static',template_folder='./templates')

client=None
broker=None
port=None

@app.route('/')
def intro():
  global client,broker,port
  return render_template('intro.html',client=client,IP=broker,port=port)

@app.route('/choice',methods=['POST'])
def introNext():
  global client,broker,port
  client=request.form['client']
  broker=request.form['broker']
  port=request.form['port']
  print(client,broker,port)
  return render_template('choice.html',client=client,IP=broker,port=port)

@app.route('/back')
def back():
  return render_template('intro.html')

@app.route('/disatnce')
def distance():
  global client,broker,port
  print(client,broker,port)
  return render_template('distance.html',client=client,IP=broker,port=port)

@app.route('/cctv')
def cctv():
  global client,broker,port
  print(client,broker,port)
  return render_template('cctv.html',client=client,IP=broker,port=port)

@app.route('/illumination')
def illumination():
  global client,broker,port
  print(client,broker,port)
  return render_template('illumination.html',client=client,IP=broker,port=port)

@app.route('/choicepage')
def choicepage():
  global client,broker,port
  print(client,broker,port)
  return render_template('choice.html',client=client,IP=broker,port=port)

if __name__=="__main__":
  app.run(host= '0.0.0.0',port=1999,debug=True)