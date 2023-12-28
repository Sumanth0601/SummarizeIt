from flask import Flask, render_template, request, send_file
from pytube import YouTube
from pydub import AudioSegment
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_link = request.form.get('link')
        summary_type = request.form.get('summary-type', 'normal')
        audio_language = request.form.get('audio-language', 'english')

        if youtube_link:
            try:
                yt = YouTube(youtube_link)
                audio_stream = yt.streams.filter(only_audio=True).first()

                if audio_stream:
                    audio_stream.download(app.config['UPLOAD_FOLDER'])
                    mp4_filename = audio_stream.default_filename
                    mp4_filepath = os.path.join(app.config['UPLOAD_FOLDER'], mp4_filename)
                    mp3_filename = mp4_filename.replace('mp4', 'mp3')
                    mp3_filepath = os.path.join(app.config['UPLOAD_FOLDER'], mp3_filename)

                    # Convert to MP3 using pydub
                    audio = AudioSegment.from_file(mp4_filepath, format='mp4')
                    audio.export(mp3_filepath, format='mp3')

                    # Remove the original MP4 file
                    os.remove(mp4_filepath)

                    return render_template('index.html', link=youtube_link, summary_type=summary_type,
                                           audio_language=audio_language, file_name=mp3_filename)
                else:
                    return render_template('index.html', link=None, error_message="No audio stream found.")
            except Exception as e:
                print(f"Error: {e}")
                return render_template('index.html', link=None, error_message="Error processing YouTube link.")
        else:
            return render_template('index.html', link=None, error_message="Please enter a valid YouTube link.")

    else:
        return render_template('index.html', link=None)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)













# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         youtube_link = request.form.get('link')
#         summary_type = request.form.get('summary-type', 'normal')
#         audio_language = request.form.get('audio-language', 'english')

#         if youtube_link:
#             try:
#                 yt = YouTube(youtube_link)
#                 audio_stream = yt.streams.filter(only_audio=True).first()

#                 if audio_stream:
#                     audio_stream.download(app.config['UPLOAD_FOLDER'])
#                     mp4_filename = audio_stream.default_filename
#                     mp4_filepath = os.path.join(app.config['UPLOAD_FOLDER'], mp4_filename)
#                     mp3_filename = mp4_filename.replace('mp4', 'mp3')
#                     mp3_filepath = os.path.join(app.config['UPLOAD_FOLDER'], mp3_filename)

#                     # Convert to MP3 using pydub
#                     audio = AudioSegment.from_file(mp4_filepath, format='mp4')
#                     audio.export(mp3_filepath, format='mp3')

#                     # Remove the original MP4 file
#                     os.remove(mp4_filepath)

#                     return render_template('index.html', link=youtube_link, summary_type=summary_type,
#                                            audio_language=audio_language, file_name=mp3_filename)
#                 else:
#                     return render_template('index.html', link=None)
#             except Exception as e:
#                 print(f"Error: {e}")
#                 return render_template('index.html', link=None)

#         # No valid input
#         else:
#             return render_template('index.html', link=None)

#     else:
#         return render_template('index.html', link=None)