import json
import os
from threading import Thread

from kivy.app import App
from kivy.clock import Clock
from kivy.utils import platform

from .morse_helper import MorseHelper
from auto_morse_recognizer.auto_morse_recognizer import AutoMorseRecognizer

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


class Utility(object):
    def __init__(self):
        self.calibration = 0.5

        # used in training screens
        self.morse_helper = MorseHelper()
        self.training_prompt_dict = training_prompt_dict
        self.training_difficulty = ''
        self.auto_morse_recognizer = AutoMorseRecognizer(active_threshold=self.calibration)
