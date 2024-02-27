from flask import Flask, render_template, request, jsonify, send_file
from gtts import gTTS
import os
import time

app = Flask(__name__)

def text_to_speech(text, language='en', filename='output.mp3'):
    """
    Convert text to speech and save it to an audio file.
    
    Args:
        text (str): The text to be converted to speech.
        language (str): The language code (e.g., 'en' for English, 'fr' for French).
        filename (str): The name of the output audio file.
    """

    root_folder = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(root_folder, filename)


    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(filename)
    print(f"Text converted to speech and saved as '{filename}'")
    return filename

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/convert_text_to_speech', methods=['POST'])
def convert_text_to_speech():
    data = request.get_json()
    text = data.get('text')
    language = data.get('language', 'en')
    filename = data.get('filename', 'output.mp3')

    generated_filename = text_to_speech(text, language, filename)
    #os.stat('output.mp3')
    
    return jsonify({'message': 'Text converted to speech successfully', 'filename': generated_filename})

@app.route('/output.mp3')
def get_audio():
    # Serve the file for download
    try:
        return send_file('output.mp3', as_attachment=True)
    finally:
        # Delete the file after it's served
        time.sleep(2)
#os.remove('output.mp3')
        
@app.route('/delete_file', methods=['DELETE'])
def delete_file():
    try:
        os.remove('output.mp3')
        return jsonify({'message': 'File deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
