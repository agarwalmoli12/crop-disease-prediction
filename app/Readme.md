
---

# 🌿 Plant Disease Detection AI

<p align="center">
  <img src="https://your-image-url-here.com/plant-ai-logo.gif" alt="Plant AI Logo" width="200" height="200">
</p>

<div align="center">

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.0.1-brightgreen.svg)
![Torch](https://img.shields.io/badge/torch-v1.9.0-red.svg)
![Ollama](https://img.shields.io/badge/ollama-latest-orange.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

</div>

## 🌟 Introduction

This project is a cutting-edge web application for plant disease detection using AI technology. It empowers farmers and gardeners to swiftly and accurately identify plant diseases, offering valuable insights and tailored recommendations.

<p align="center">
  <img src="https://your-image-url-here.com/plant-disease-demo.gif" alt="Plant Disease Detection Demo" width="600">
</p>

## ⭐ Features

- 🔬 AI-powered plant disease detection
- 📸 Image upload and analysis
- 📊 Detailed disease information and prevention steps
- 💊 Supplement recommendations
- 🤖 Interactive AI chatbot for plant health queries
- 📱 Responsive design for various devices

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/plant-disease-detection.git
   cd plant-disease-detection
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure you have the trained model file:**
   - Place the `plant_disease_model_1_latest.pt` file in the project root directory.

5. **Set up the database files:**
   - Place `disease_info.csv` and `supplement_info.csv` in the project root directory.

## 📦 Dependencies

The main dependencies for this project are:

- Flask
- Torch
- Torchvision
- Pillow
- Pandas
- Numpy
- Ollama

For a complete list, refer to the `requirements.txt` file.

## 🏃‍♂️ Running the Application

1. **Start the Flask development server:**
   ```bash
   python app.py
   ```

2. **Open a web browser and navigate to:** `http://localhost:5000`

## 🤖 AI Chatbot Implementation

The AI chatbot uses the Ollama library for natural language processing. Here's a brief overview of the implementation:

```python
import ollama

# Chatbot system prompt
system_prompt = """
You are an AI assistant specializing in plant diseases and health...
"""

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
```

Ensure you have Ollama set up and running on your system for the chatbot to function properly.

## 🔧 Configuration

- **Modify `app.py`** to adjust Flask configurations or AI model parameters.
- **Update `disease_info.csv` and `supplement_info.csv`** to modify disease information and supplement recommendations.

## 📱 Mobile Support

The application is designed to be responsive and works seamlessly on various devices, including mobile phones and tablets.

## 🚨 Important Notes

- Train the model on your local machine and place the `plant_disease_model_1_latest.pt` file in the project root before running the application.
- For deployment, consider using a production-ready web server like Gunicorn and a reverse proxy like Nginx.
- Ensure all static files and uploads are properly served in a production environment.

## 🤝 Contributing

We welcome contributions to improve the project! Please follow the standard fork-and-pull request workflow.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## 👥 Authors

- **Manthan Bhikadiya**
- **Krishna Baldaniya**

For any queries, please contact: krsikx@gmail.com

---

### Project Structure:

```
plant-disease-detection/
│
├── app.py                 # Main Flask application file
├── CNN.py                 # CNN model definition
├── requirements.txt       # Python dependencies
├── plant_disease_model_1_latest.pt  # Trained model file
├── disease_info.csv       # Disease information database
├── supplement_info.csv    # Supplement information database
│
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/           # Uploaded images directory
│
└── templates/
    ├── base.html
    ├── index.html
    └── submit.html
```

---

This `README.md` should now provide clear and detailed instructions for setting up and running your Plant Disease Detection AI project.