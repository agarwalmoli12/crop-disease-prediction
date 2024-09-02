import os
from flask import Flask, redirect, render_template, request, url_for, jsonify, Response, stream_with_context
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd
from werkzeug.utils import secure_filename
from datetime import datetime
import ollama

disease_info = pd.read_csv('disease_info.csv', encoding='cp1252')
supplement_info = pd.read_csv('supplement_info.csv', encoding='cp1252')

model = CNN.CNN(39)    
model.load_state_dict(torch.load("plant_disease_model_1_latest.pt"))
model.eval()

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

system_prompt = """
You are an AI assistant specializing in plant diseases and health. Your knowledge base includes information about various plant diseases, their symptoms, prevention methods, and treatments. Provide concise, relevant, and precise responses based on the following guidelines:

1. When discussing a specific plant disease, provide accurate information about its symptoms, causes, and impact on plant health.
2. Offer practical advice for preventing and treating plant diseases, including both organic and chemical methods when appropriate.
3. If asked about a healthy plant, provide tips for maintaining its health and optimizing growth.
4. When recommending supplements or fertilizers, explain their benefits and proper usage.
5. If you're unsure about a specific detail, clearly state that you don't have enough information rather than making assumptions.
6. Maintain a professional yet friendly tone, and tailor your language to be accessible to both gardening enthusiasts and professionals.
7. If asked about topics unrelated to plants or gardening, politely redirect the conversation to plant-related subjects.

Your primary goal is to assist users in understanding plant diseases, promoting plant health, and providing actionable advice for plant care.
"""

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_and_rename_image(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        new_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
        file_path = os.path.join('uploads', new_filename)
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(full_path)
        return file_path
    return None

def prediction(image_path):
    image = Image.open(os.path.join('static', image_path))
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    return index

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact-us.html')

@app.route('/index')
def ai_engine_page():
    return render_template('index.html')

@app.route('/mobile-device')
def mobile_device_detected_page():
    return render_template('mobile-device.html')

@app.route('/submit', methods=['POST'])
def submit():
    if 'image' not in request.files:
        return redirect(url_for('ai_engine_page'))
    file = request.files['image']
    if file.filename == '':
        return redirect(url_for('ai_engine_page'))
    
    file_path = save_and_rename_image(file)
    if file_path is None:
        return redirect(url_for('ai_engine_page'))
    
    pred = prediction(file_path)
    title = disease_info['disease_name'][pred]
    description = disease_info['description'][pred]
    prevent = disease_info['Possible Steps'][pred]
    image_url = disease_info['image_url'][pred]
    supplement_name = supplement_info['supplement name'][pred]
    supplement_image_url = supplement_info['supplement image'][pred]
    supplement_buy_link = supplement_info['buy link'][pred]
    
    return render_template('submit.html', title=title, desc=description, prevent=prevent, 
                           image_path=file_path, pred=pred, sname=supplement_name, 
                           simage=supplement_image_url, buy_link=supplement_buy_link)

@app.route('/market', methods=['GET', 'POST'])
def market():
    return render_template('market.html', supplement_image=list(supplement_info['supplement image']),
                           supplement_name=list(supplement_info['supplement name']), 
                           disease=list(disease_info['disease_name']), 
                           buy=list(supplement_info['buy link']))

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data['message']
    disease_context = data.get('disease_context', '')
    
    conversation = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': f"Disease Context: {disease_context}\n\nUser Question: {message}"}
    ]
    
    def generate():
        for chunk in ollama.chat(model='dolphin-llama3', messages=conversation, stream=True):
            yield chunk['message']['content']
    
    return Response(stream_with_context(generate()), content_type='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
