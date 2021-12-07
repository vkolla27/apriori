from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from apriori import runApriori, dataFromFile, to_str_results

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.csv']
app.config['UPLOAD_PATH'] = 'uploads'
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
       f = request.files['file']
       support = request.form.get("text")
       if f.filename != '':
           f.save(secure_filename(f.filename))
           inFile = dataFromFile(str(f.filename))
           items, rules = runApriori(inFile,float(int(support)/1000), 0.1)
           i, r = to_str_results(items, rules)
           res = [sub.replace('item:', '') for sub in i]
           res = [sub.replace('\'',"") for sub in res]
           res = [sub.replace(' ',"") for sub in res]
           res = [sub.replace('""',"") for sub in res]
           res = [sub.replace(',',"") for sub in res]
           res = [sub.replace('(', '{') for sub in res]
           res = [sub.replace(')','}') for sub in res]

           out =[]
           for sub in res:
               out.append(sub.split('}',1)[0]+'}')
           l=str(len(out))
           return render_template("upload.html",output=out,total="Total items:"+l,filen=f.filename)
       else:
           return render_template("index.html",output="No file selected")
# main code
if __name__ == '__main__':
    app.run()
