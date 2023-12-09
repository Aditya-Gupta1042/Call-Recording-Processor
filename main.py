from fileinput import filename 
from flask import *
import assemblyai as aai     # openAI API

aai.settings.api_key = "0037f7b7bd364e339486d5fea752c9b1"  #assemblyai API key token

app = Flask(__name__, template_folder="templateFiles", static_folder="staticFiles") 

@app.route('/') 
def main(): 
    return render_template("main.html") 

def transcribe_audio(fileName):
    config = aai.TranscriptionConfig(
        summarization=True,
        summary_model=aai.SummarizationModel.informative,
        summary_type=aai.SummarizationType.bullets
    )

    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(fileName)

    return transcript

@app.route('/success', methods = ['POST']) 
def success(): 
    if request.method == 'POST': 
        f = request.files['file'] 
        f.save(f.filename)          # saves the file to the folder.
        
        transcript_object = transcribe_audio(f.filename)
        
        transcript = transcript_object.text
        summary = transcript_object.summary
        
        return render_template("acknowledgement.html", name = f.filename, transcript=transcript, summary = summary) 

if __name__ == '__main__': 
    app.run(debug=True)