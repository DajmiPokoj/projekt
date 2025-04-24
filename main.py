rom io import BytesIO
from flask import Flask, send_file, request, send_from_directory
from ves import render_ves
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def serve_pil_image(img):
  
  img_io = BytesIO()
  img.save(img_io, 'PNG', quality=70)
  img_io.seek(0)
  return send_file(img_io, mimetype='image/png')



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
  
  if (len(path) == 0): 
    return send_from_directory('public', 'index.html')

  return send_from_directory('public', path)


@app.route('/render', methods=['post'])
def render():
  
  ves = request.form.get('ves') 
  width = request.form.get('width') 
  print(ves)
  img = render_ves() 
  return serve_pil_image(img) # vratime vyrenderovany obrazok ako jpg

if __name__ == "__main__":
  app.run(debug=True)
