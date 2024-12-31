import os
import webbrowser
from dotenv import load_dotenv
from moviepy import VideoFileClip
import gradio as gr
import google.generativeai as genai

LANGUAGE = "spanish"

load_dotenv()

output_folder = "output"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)
        
GEMINI_KEY = os.getenv("API_KEY")

genai.configure(api_key=GEMINI_KEY)

def upload_to_gemini(path, mime_type=None):
  #Uploads the given file to Gemini.
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
  system_instruction=f"make a transcription with the audio to text, in {LANGUAGE}, make sure the transcription is time stamped, the text must be ordered and well structured with punctuations",
)

def process_video(video_file):
  output_path = os.path.join(output_folder, "audio.mp3")
  
  try:
    # Load video file and extract audio
    video = VideoFileClip(video_file.name)
    video.audio.write_audiofile(output_path)
    video.close()
    print(f"Saved MP3: {output_path}")
    
    # Upload to Gemini and generate content
    uploaded_file = upload_to_gemini(output_path, mime_type="audio/mp3")
    response = model.generate_content([uploaded_file, f"transcribe in {LANGUAGE}"])
    
    # Save response to summary.txt
    with open("summary.txt", "w", encoding="utf-8") as f:
      f.write(response.text)
    
    return response.text
  except Exception as e:
    return f"Error processing video: {e}"

# Create Gradio interface
iface = gr.Interface(
  fn=process_video,
  inputs=gr.File(label="Upload MP4 Video", type="filepath", file_count="single", file_types=[".mp4", ".mkv", ".avi", ".mov"]),
  outputs="text",
  title="Video to Audio Transcription",
  allow_flagging='never',
  description="Upload a video file to transcribe its audio content."
)

# Launch the interface
webbrowser.open("http://127.0.0.1:7860")
iface.launch()
