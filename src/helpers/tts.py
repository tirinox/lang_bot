import io

import gtts


def tts(text, lang='ja') -> io.BytesIO:
    tts_instance = gtts.gTTS(text, lang=lang)  # request google to get synthesis
    audio_file = io.BytesIO()
    tts_instance.write_to_fp(audio_file)
    audio_file.seek(0)
    return audio_file
