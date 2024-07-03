from flask import Flask, render_template, jsonify
import sqlite3
import plotly.graph_objs as go
import plotly
import json
from datetime import datetime
import random

app = Flask(__name__)

# Function to create and populate the database
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS readings
                 (timestamp TEXT, value REAL)''')
    conn.commit()
    conn.close()

# Function to add a new data point
def add_data_point():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    value = random.uniform(0, 100)  # Random value for demonstration
    c.execute("INSERT INTO readings VALUES (?, ?)", (now, value))
    conn.commit()
    conn.close()

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to get updated data
@app.route('/data')
def get_data():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM readings ORDER BY timestamp DESC LIMIT 50")
    data = c.fetchall()
    conn.close()
    
    timestamps = [row[0] for row in data][::-1]
    values = [row[1] for row in data][::-1]
    
    trace = go.Scatter(x=timestamps, y=values, mode='lines+markers')
    layout = go.Layout(title='Real-time Data')
    fig = go.Figure(data=[trace], layout=layout)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify(graphJSON)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
