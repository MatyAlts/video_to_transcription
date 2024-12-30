
# Video to Audio Transcription App

This application extracts audio from video files and transcribes it using Google's Generative AI.

## Installation

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required Python packages:

`pip install -r requirements.txt`

## Setup

1. Create a `.env` file in the project directory with your Google API key:
`API_KEY="your_google_api_key_here"`
2. Ensure you have a `videos` folder in the project directory containing the video files you want to process.
3. Change the language settings to improve the transcription:
`LANGUAGE = "spanish"`

## Usage

1. Run the `main.py` script:
`python main.py`
2. Follow the prompts to enter the name of the MP3 file you want to transcribe.
3. The transcribed text will be saved in `summary.txt`.

## Notes
* Supported video formats: `.mp4`, `.mkv`, `.avi`, `.mov`
* The output audio files will be saved in the `output` folder.
* Ensure your API key has the necessary permissions to use Google's Generative AI services.