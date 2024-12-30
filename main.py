import os
from dotenv import load_dotenv
from moviepy import VideoFileClip
import google.generativeai as genai

LANGUAGE = "spanish"

load_dotenv()

videos_folder = "videos"
output_folder = "output"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process each video in the videos folder
for file_name in os.listdir(videos_folder):
    if file_name.endswith((".mp4", ".mkv", ".avi", ".mov")):
        video_path = os.path.join(videos_folder, file_name)
        output_path = os.path.join(output_folder, os.path.splitext(file_name)[0] + ".mp3")
        
        print(f"Processing: {file_name}")
        
        try:
            # Load video file and extract audio
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(output_path)
            video.close()
            print(f"Saved MP3: {output_path}")
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
            
GEMINI_KEY = os.getenv("API_KEY")

genai.configure(api_key=GEMINI_KEY)

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
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
  system_instruction="make a transcription with the audio to text, in spanish, make sure the transcription is time stamped, the text must be ordered and well structured with punctuations",
)

# TODO Make these files available on the local file system
# You may need to update the file paths

while True:
  filename = input("Enter the filename to be transcribed: ") + ".mp3"
  if os.path.exists(os.path.join(output_folder, filename)):
    break
  else:
    print(f"The file {filename} doesn't exists in the folder 'videos'. Please try again.")

files = [
  upload_to_gemini(f"output/{filename}", mime_type="audio/mp3"),
]

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        files[0],
      ],
    },
    {
      "role": "model",
      "parts": [
        "This is a test \n",
      ],
    },
  ]
)

response = model.generate_content([files[0], f"transcribe in {LANGUAGE}"])

# Save response to resumen.txt
with open("summary.txt", "w", encoding="utf-8") as f:
  f.write(response.text)

print(response.text)

exit()