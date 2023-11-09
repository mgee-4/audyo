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
    idx = ObjectProperty(0)
    clist = ObjectProperty()
    is_playing = ObjectProperty(False)
    sound_pos = ObjectProperty(0)

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
        self.cchord = self.clist[0][0]

    def toggle_play(self):
        if not self.clist:
            return
        if self.is_playing:
            self.pause()
        else:
            self.play()

    def play(self):
        if self.clist:
            if self.sound_pos == 0:
                self.sound.play()
            else:
                self.sound.seek(self.sound_pos)
                self.sound.play()
            self.is_playing = True
            Clock.schedule_interval(self.update_chord, 0.1)

    def pause(self):
        if self.clist:
            self.sound_pos = self.sound.get_pos()
            self.sound.stop()
            self.is_playing = False
            Clock.unschedule(self.update_chord)

    def update_chord(self, dt):
        if self.idx < len(self.clist) and self.sound.get_pos() >= self.clist[self.idx][1]:
            self.cchord = self.clist[self.idx][0]
            self.idx += 1

    def chords(self):
        print(self.clist)

if __name__ == "__main__":
    Audyo().run()
