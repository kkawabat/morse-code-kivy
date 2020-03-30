import numpy as np


class MorseEngine:
    def __init__(self, sound_engine):
        self.__letter_to_morse = {'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 'g': '--.',
                                  'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.',
                                  'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.', 's': '...', 't': '-', 'u': '..-',
                                  'v': '...-', 'w': '.--', 'x': '-..-', 'y': '-.--', 'z': '--..',
                                  '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
                                  '6': '-....', '7': '--...', '8': '---..', '9': '----.', ' ': '/'}
        self.__morse_to_letter = {morse: letter for letter, morse in self.__letter_to_morse.items()}
        self.speaker = sound_engine
        self.rate = 16000
        self.morse_unit = .08
        self.beep_pitch = 200
        self.morse_duration_info = self.get_morse_duration(morse_unit=self.morse_unit)
        self.morse_signal_templates = self.gen_morse_signal_template(self.beep_pitch, self.morse_unit)

    def get_morse_duration(self, morse_unit):
        return {'dot': morse_unit, 'dash': morse_unit*3, 'short_pause': morse_unit*3, 'long_pause': morse_unit*7}

    def gen_morse_signal_template(self, frequency, morse_time_unit):
        morse_time_sample = int(self.rate * morse_time_unit)
        short_short_pause = np.zeros(morse_time_sample * 1)
        short_pause = np.zeros(morse_time_sample * 2).astype(np.float32).tostring()
        long_pause = np.zeros(morse_time_sample * 6).astype(np.float32).tostring()

        dot_sig = np.sin(frequency * 2 * np.pi * np.arange(morse_time_sample) / self.rate)
        dot_sig[:100] = dot_sig[:100] * np.linspace(0, 1, 100)
        dot_sig[-100:] = dot_sig[-100:] * np.linspace(1, 0, 100)
        dot_sig = np.concatenate([dot_sig, short_short_pause]).astype(np.float32).tostring()

        dash_sig = np.sin(frequency * 2 * np.pi * np.arange(morse_time_sample * 3) / self.rate)
        dash_sig[:100] = dash_sig[:100] * np.linspace(0, 1, 100)
        dash_sig[-100:] = dash_sig[-100:] * np.linspace(1, 0, 100)
        dash_sig = np.concatenate([dash_sig, short_short_pause]).astype(np.float32).tostring()
        return {'dot': dot_sig, 'dash': dash_sig, 'short_pause': short_pause, 'long_pause': long_pause}

    def morse_to_text(self, morse_code):
        text = ''
        morse_words = [word.strip() for word in morse_code.split('/') if word.strip() != '']
        for morse_word in morse_words:
            for morse_letter in morse_word.split(' '):
                if morse_letter in self.__morse_to_letter:
                    text += self.__morse_to_letter[morse_letter]
                else:
                    text += '?'
            text += ' '
        return text.strip().strip('/')

    def text_to_morse(self, text):
        morse_code = ''
        text = text.lower()
        for letter in text:
            if letter in self.__letter_to_morse:
                morse_code += self.__letter_to_morse[letter] + ' '
            else:
                morse_code += '?'
        return morse_code

    def text_to_morse_sound(self, text):
        self.morse_to_sound(self.text_to_morse(text))

    def morse_to_sound(self, morse_code):
        signal_list = []
        for code in morse_code:
            if code == '.':
                signal_list.append(self.morse_signal_templates['dot'])
            elif code == '-':
                signal_list.append(self.morse_signal_templates['dash'])
            elif code == ' ':
                signal_list.append(self.morse_signal_templates['short_pause'])
            elif code == '/':
                signal_list.append(self.morse_signal_templates['long_pause'])
        self.speaker.play_audio(signal_list)

    def clear_sound(self):
        self.speaker.stop_audio()


if __name__ == '__main__':
    me = MorseEngine()
    me.text_to_morse_sound('hello')
    me.text_to_morse_sound('      ')
    # me.text_to_morse_sound('soasdfasdfs')
    # me.text_to_morse_sound('soasdfasdfs')
