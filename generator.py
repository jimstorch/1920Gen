#!/usr/bin/python3

from random import randint, shuffle, choice
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

STAT_COLOR = (.0, .4, .7)
TEXT_COLOR = (.0, .4, .7)
DEFAULT_FONT = 'FellEnglish-Bold'
pdfmetrics.registerFont(
    TTFont('FellEnglish-Bold', 'data/FellEnglish-Bold.ttf'))

with open('data/male.txt') as f:
    males = f.read().splitlines()

with open('data/female.txt') as f:
    females = f.read().splitlines()

with open('data/surnames.txt') as f:
    surnames = f.read().splitlines()

with open('data/towns1920.txt') as f:
    towns = f.read().splitlines()


def male_name():
    return choice(males) + ' ' + choice(surnames)


def female_name():
    return choice(females) + ' ' + choice(surnames)


class Character(object):

    def d6(self, count=1):
        sum = 0
        for x in range(count):
            sum += randint(1, 6)
        return sum

    def improvement_check(self, count):
        for x in range(count):
            improv = randint(1, 100)
            if improv > self.education:
                self.education += randint(1, 10)

        if self.education > 99:
            self.education = 99

    def deduct(self, point_list):
        shuffle(point_list)
        self.strength -= point_list[0]
        self.constitution -= point_list[1]
        self.dexterity -= point_list[2]

    def sex(self, sex):
        self.sex = sex

    def name(self, name):
        self.name = name


class Character1920(Character):

    def __init__(self):

        self.birthplace = choice(towns)
        self.strength = self.d6(3) * 5
        self.size = (self.d6(2) + 6) * 5
        self.dexterity = self.d6(3) * 5
        self.appearance = self.d6(3) * 5
        self.constitution = self.d6(3) * 5
        self.intelligence = (self.d6(2) + 6) * 5
        self.education = (self.d6(2) + 6) * 5
        self.power = self.d6(3) * 5
        self.luck = (self.d6(2) + 6) * 5
        self.age = 15 + randint(0, 64)

        if self.age >= 15 and self.age <= 19:
            self.education -= 5
            l1 = randint(1, 5)
            l2 = 5 - l1
            self.strength -= l1
            self.size -= l2
            luck2 = (self.d6(2) + 6) * 5
            if self.luck < luck2:
                self.luck = luck2

        elif self.age >= 20 and self.age <= 39:
            self.improvement_check(1)

        elif self.age >= 40 and self.age <= 49:
            self.improvement_check(2)
            self.deduct([1, 2, 2])
            self.appearance -= 5

        elif self.age >= 50 and self.age <= 59:
            self.improvement_check(3)
            self.deduct([3, 3, 4])
            self.appearance -= 10

        elif self.age >= 60 and self.age <= 69:
            self.improvement_check(4)
            self.deduct([6, 7, 7])
            self.appearance -= 15

        elif self.age >= 70 and self.age <= 79:
            self.improvement_check(4)
            self.deduct([13, 13, 14])
            self.appearance -= 20

        elif self.age >= 80:
            self.improvement_check(4)
            self.deduct([26, 27, 27])
            self.appearance -= 25

        self.hitpoints = int((self.size + self.constitution) / 10)

        if self.dexterity < self.size and self.strength < self.size:
            self.movement = 7

        if self.strength >= self.size or self.dexterity >= self.size:
            self.movement = 8

        if self.strength > self.size and self.dexterity > self.size:
            self.movement = 9

        if self.age >= 40 and self.age <= 49:
            self.movement -= 1
        elif self.age >= 50 and self.age <= 59:
            self.movement -= 2
        elif self.age >= 60 and self.age <= 69:
            self.movement -= 3
        elif self.age >= 70 and self.age <= 79:
            self.movement -= 4
        elif self.age >= 80:
            self.movement -= 5


class PDF1920(object):

    def __init__(self, width=612, height=792):
        self.c = canvas.Canvas('sample.pdf')
        self.c.setPageSize((width, height))

    def save_pdf(self):
        self.c.save()

    def font_size(self, size):
        self.c.setFontSize(size)

    def font_color(self, r, g, b):
        self.c.setFillColorRGB(r, g, b)

    def draw_string(self, x, y, text):
        self.c.drawString(x, y, str(text))

    def _add_stat(self, x, y, value):
        self.font_color(*STAT_COLOR)
        self.font_size(13)
        self.draw_string(x, y, value)
        one_half = str(int(value / 2))
        one_fifth = str(int(value / 5))
        self.font_size(9)
        self.draw_string(x+26, y+8, one_half)
        self.draw_string(x+26, y-6, one_fifth)

    def _add_text(self, x, y, text):
        self.font_size(12)
        self.font_color(*TEXT_COLOR)
        self.draw_string(x, y, str(text))

    def name(self, text):
        self._add_text(142, 739, text)

    def player(self, text):
        self._add_text(142, 719, text)

    def occupation(self, text):
        self._add_text(164, 699, text)

    def age(self, text):
        self._add_text(136, 680, text)

    def sex(self, text):
        self._add_text(220, 680, text)

    def residence(self, text):
        self._add_text(155, 658, text)

    def birthplace(self, text):
        self._add_text(155, 639, text)

    def str(self, value):
        self._add_stat(332, 710, value)

    def dex(self, value):
        self._add_stat(419, 710, value)

    def int(self, value):
        self._add_stat(511, 710, value)

    def con(self, value):
        self._add_stat(332, 678, value)

    def app(self, value):
        self._add_stat(419, 678, value)

    def pow(self, value):
        self._add_stat(511, 678, value)

    def siz(self, value):
        self._add_stat(332, 647, value)

    def edu(self, value):
        self._add_stat(419, 647, value)

    def mov(self, value):
        self.font_color(*STAT_COLOR)
        self.font_size(13)
        self.draw_string(511, 647, value)

    def hp(self, value):
        self.font_color(*STAT_COLOR)
        self.font_size(13)
        self.draw_string(100, 582, value)

    def luck(self, value):
        self.font_color(*STAT_COLOR)
        self.font_size(13)
        self.draw_string(100, 510, value)

    def sanity(self, value):
        self.font_color(*STAT_COLOR)
        self.font_size(13)
        self.draw_string(480, 582, value)

    def magic(self, value):
        self.font_color(*STAT_COLOR)
        self.font_size(13)
        self.draw_string(480, 510, value)

    def add_character(self, char):

        self.c.drawImage('data/1920blank.png', 0, 0, 612, 792)
        self.c.setFont(DEFAULT_FONT, 12)
        self.name(char.name)
        self.age(char.age)
        self.sex(char.sex)
        #o.player('Henry Armitage')
        # o.occupation('Librarian')
        #o.residence('Arkham, MA')
        self.birthplace(char.birthplace)
        self.str(char.strength)
        self.dex(char.dexterity)
        self.int(char.intelligence)
        self.con(char.constitution)
        self.app(char.appearance)
        self.pow(char.power)
        self.sanity(char.power)
        self.magic(int(char.power / 5))
        self.siz(char.size)
        self.edu(char.education)
        self.mov(char.movement)
        self.hp(char.hitpoints)
        self.luck(char.luck)
        self.c.showPage()


p = PDF1920()

for x in range(200):

    c = Character1920()
    c.sex('Male')
    c.name(male_name())
    p.add_character(c)

    c = Character1920()
    c.sex('Female')
    c.name(female_name())
    p.add_character(c)

p.save_pdf()
