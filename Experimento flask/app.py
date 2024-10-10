from flask import Flask, render_template

app = Flask (__name__)

links = [
{"titulo": "Die With A Smile", "link": "https://www.youtube.com/watch?v=kPa7bsKwL-c"},
{"titulo": "V de Vilão", "link": "https://www.youtube.com/watch?v=QGSdmEsv4G0"}
]

#Rota principal (HOME) -- decorator
@app.route('/')
def index():
    usuario = "Mariazinha"
    assinatura = "gratis"
    if assinatura == "premium":
        conteudo = links
    else:
        conteudo = ""
    return render_template ('index.html', usuario = usuario, conteudo = conteudo) 

@app.route('/sobre')
def sobre():
    return render_template ('sobre.html')


#Final do código
app.run(debug = True)