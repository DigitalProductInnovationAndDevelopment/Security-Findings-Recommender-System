from flask import Flask
import time

app = Flask(__name__)

start_time = time.time()

@app.route('/')
def health():
    system_info = {
        'status': 'UP',
        'uptime': round(time.time() - start_time, 2)
    }
    return system_info, 200

if __name__ == '__main__':
    app.run(debug=True)