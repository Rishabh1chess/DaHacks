from flask import Flask, render_template, jsonify
import planet  # Replace with your actual simulation script

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate')
def simulate():
    # Run your simulation
    result = planet.run_simulation()  # Adjust based on your script
    # Assuming 'result' is serializable (e.g., dict, list)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

