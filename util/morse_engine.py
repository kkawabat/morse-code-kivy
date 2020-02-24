import os

from kivy.core.audio import SoundLoader


class MorseEngine:
    def __init__(self):
        self.__letter_to_morse = {'a': '.-', 'b': '-...', 'c': '-.-.',
                                  'd': '-..', 'e': '.', 'f': '..-.',
                                  'g': '--.', 'h': '....', 'i': '..',
                                  'j': '.---', 'k': '-.-', 'l': '.-..',
                                  'm': '--', 'n': '-.', 'o': '---',
                                  'p': '.--.', 'q': '--.-', 'r': '.-.',
                                  's': '...', 't': '-', 'u': '..-',
                                  'v': '...-', 'w': '.--', 'x': '-..-',
                                  'y': '-.--', 'z': '--..', '0': '-----',
                                  '1': '.----', '2': '..---', '3': '...--',
                                  '4': '....-', '5': '.....', '6': '-....',
                                  '7': '--...', '8': '---..', '9': '----.',
                                  ' ': '/'}
        self.__morse_to_letter = {morse: letter for letter, morse in self.__letter_to_morse.items()}

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
                morse_code += '/?/ '
        return morse_code

    def get_letter_as_morse_sound(self, letter):
        sound_path = os.path.join('data', 'morse_alphabets', f'{letter}.wav')
        return SoundLoader.load(sound_path)
