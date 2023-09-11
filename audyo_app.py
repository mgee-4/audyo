from kivy.app import App
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.lang import Builder
from chord_extractor.extractors import Chordino

class FileChoosePopup(Popup):
    load = ObjectProperty()

class Audyo(App):
    file_path = StringProperty('Choose File')
    sound = ObjectProperty()
    cchord = StringProperty('None')
    clist = ObjectProperty()
    idx = ObjectProperty(0)

    def build(self):
        return Builder.load_file('audyo_app.kv')

    def open_popup(self):
        self.the_popup = FileChoosePopup(load=self.load)
        self.the_popup.open()

    def load(self, selection):
        chordino = Chordino(roll_on=1)
        self.file_path = str(selection[0])
        self.the_popup.dismiss()
        self.sound = SoundLoader.load(self.file_path)
        chords = chordino.extract(self.file_path)
        self.clist = chords

    def play(self):
        if self.clist:
            self.sound_pos = 0
            self.sound.play()

    def pause(self):
        if self.clist:
            self.sound_pos = self.sound.get_pos()
            self.sound.stop()

    def resume(self):
        if self.clist:
            self.sound.play()
            Clock.schedule_once(self.do_seek)

    def do_seek(self, dt):
        self.sound.seek(self.sound_pos)

    def chords(self):
        print(self.clist)

    def nc(self):
        if self.idx < len(self.clist):
            self.cchord = self.clist[self.idx][0]
            self.idx += 1

if __name__ == "__main__":
    Audyo().run()
