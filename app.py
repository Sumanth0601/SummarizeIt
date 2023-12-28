from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_link = request.form.get('link')
        audio_file = request.files.get('audio-file')  # Use request.files to get the uploaded file
        summary_type = request.form.get('summary-type', 'normal')
        audio_language = request.form.get('audio-language', 'english')

        if youtube_link and not audio_file:  # YouTube link is present and audio file is not present
            print(f'YouTube Link: {youtube_link}')
            print(f'Summary Type: {summary_type}')
            print(f'Audio Language: {audio_language}')

            # You can process the YouTube link further or redirect to another page
            return render_template('index.html', link=youtube_link, summary_type=summary_type, audio_language=audio_language, file_name=None)

        elif audio_file and not youtube_link:  # Audio file is present and YouTube link is not present
            file_name = audio_file.filename
            print(f'Uploaded File: {file_name}')
            print(f'Summary Type: {summary_type}')
            print(f'Audio Language: {audio_language}')

            # You can process the audio file further or redirect to another page
            return render_template('index.html', link=None, summary_type=summary_type, audio_language=audio_language, file_name=file_name)

        else:  # Handle the case when both YouTube link and audio file are present
            print('Both YouTube Link and Audio File are present. Prioritizing YouTube Link.')
            print(f'YouTube Link: {youtube_link}')
            print(f'Summary Type: {summary_type}')
            print(f'Audio Language: {audio_language}')

            # You can process the YouTube link further or redirect to another page
            return render_template('index.html', link=youtube_link, summary_type=summary_type, audio_language=audio_language, file_name=None)

    else:
        return render_template('index.html', link=None)

if __name__ == '__main__':
    app.run(debug=True)
