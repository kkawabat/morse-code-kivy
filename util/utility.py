from util.mic_engine import AudioEngine
from util.sound_engine import SoundEngine
from .morse_engine import MorseEngine
from util.auto_morse_recognizer import AutoMorseRecognizer

training_prompt_dict = {
    'letter': list('abcdefghijklmnopqrstuvwxyz'),
    'word': ['almost', 'already', 'benefit', 'between', 'book', 'born', 'capital', 'cause',
             'central', 'certain', 'church', 'cold', 'color', 'current', 'current', 'death',
             'deep', 'develop', 'develop', 'develop', 'door', 'dream', 'drive', 'drive', 'during',
             'east', 'easy', 'exist', 'fact', 'fast', 'focus', 'good', 'hair', 'herself', 'improve',
             'level', 'light', 'lose', 'lose', 'loss', 'matter', 'member', 'middle', 'middle',
             'middle', 'moment', 'move', 'music', 'music', 'music', 'nature', 'nice', 'north',
             'note', 'note', 'office', 'only', 'onto', 'other', 'perhaps', 'player', 'police',
             'problem', 'process', 'program', 'rather', 'really', 'really', 'recent', 'relate',
             'remain', 'rich', 'rise', 'risk', 'section', 'sense', 'shake', 'sister', 'society',
             'soldier', 'some', 'space', 'spring', 'stage', 'start', 'street', 'surface', 'system',
             'talk', 'throw', 'treat', 'trouble', 'various', 'walk', 'water', 'well', 'whether',
             'wish', 'woman', 'worker'],
    'sentence': ['a bullet she answered',
                 'a sleepy voice answered',
                 'come home right away',
                 'have you got our keys handy',
                 'he will allow a rare lie',
                 'hey come back he shouted',
                 'how do oysters make pearls',
                 'it sounded silly why go on',
                 'nobody likes snakes',
                 'none should ask less',
                 'now forget all this other',
                 'perfect he thought',
                 'shall we teach him some',
                 'stoneware clay for tiles',
                 'the hotel owner shrugged',
                 'the oasis was a mirage',
                 'turn shaker upside down']
}

mnemonic_dict = {'a': 'a-PART',
                 'b': 'BOOT-to-the-head',
                 'c': 'CO-co-CO-la',
                 'd': 'DOCK-wor-ker',
                 'e': 'eh',
                 'f': 'for-the-FAIR-es',
                 'g': 'GOOD-GRAV-y',
                 'h': 'hi-pi-ty-hop',
                 'i': 'aye-aye',
                 'j': 'lets-JUMP-JUMP-JUMP',
                 'k': 'KIN-ga-ROO',
                 'l': 'to-HELL-with-it',
                 'm': 'MMM-MMM',
                 'n': 'NAV-y',
                 'o': 'ONE-OF-US',
                 'p': 'a-POO-PEE-smell',
                 'q': 'GOD-SAVE-the-QUEEN',
                 'r': 'ro-TA-tion',
                 's': 'si-si-si',
                 't': 'TALL',
                 'u': 'un-der-WHERE',
                 'v': 'du-du-du-DUUU (beethoven\'s V\'th Symphony',
                 'w': 'a-WHITE-WHALE',
                 'x': 'X-marks-the-SPOT',
                 'y': 'YELL-ow-YO-YO',
                 'z': 'ZINC-ZOO-kee-per'}


class Utility(object):
    def __init__(self):
        self.training_difficulty = ''
        self.sound_engine = SoundEngine()
        self.morse_helper = MorseEngine(self.sound_engine)

        self.mic_engine = AudioEngine()
        self.auto_morse_recognizer = AutoMorseRecognizer(self.mic_engine)

        self.training_prompt_dict = training_prompt_dict
        self.mnemonic_dict = mnemonic_dict