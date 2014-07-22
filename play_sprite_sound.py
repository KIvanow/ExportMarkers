import sublime, sublime_plugin, binascii, re, math, os
import subprocess
import threading
import ast, json


class RunAsync(threading.Thread):
    def __init__(self, cb):
        self.cb = cb
        threading.Thread.__init__(self)

    def run(self):
        self.cb()

def run_async(cb):
    res = RunAsync(cb)
    res.start()
    return res

class Player():
    url = None
    popen = None
    _enabled = False
    last_view = None

    def __init__(self, url=None):
        self.url = url

    def setTrack( self, start, duration ):
        self.start = start
        self.duration = duration

    def _play(self):
        self.popen = subprocess.Popen(["ffplay", "-ss", str( self.start ),  "-t", str( self.duration ), "-nodisp", "-autoexit", self.url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        out, err = self.popen.communicate()

    def play(self ):
        if self.url is None:
            return
        self._enabled = True
        # self.load_to_view(sublime.active_window().active_view())
        run_async(self._play)

    def stop(self):
        if self._enabled:
            self._enabled = False
            self.unload_view()
            self.popen.kill()
            self.popen = None

    def set_url(self, url):
        was_enabled = self._enabled
        self.stop()
        self.url = url
        if was_enabled:
            self.play()

    def enabled(self):
        return self._enabled

    def unload_view(self):
        if self.last_view is not None:
            self.last_view.erase_status("SublimePlayer")
            self.last_view = None

    def load_to_view(self, view):
        self.unload_view()
        if not self._enabled:
            return
        view.set_status("SublimePlayer", "Playing: %s" % (self.url))
        self.last_view = view

player = Player()

class PlaySpriteSound(sublime_plugin.TextCommand):
    def run(self, edit):
        spriteMap = self.view.substr( sublime.Region( 0, self.view.size() ))
        spriteMap = spriteMap[ spriteMap.index('return') + len('return '): spriteMap.index('})')].replace("'", "\"")
        fileName = spriteMap[ spriteMap.index('resources: [ \"') + len('resources: [ \"') : spriteMap.index('.mp3') + len( '.mp3' )]
        audioFile = os.sep.join(self.view.file_name().split(os.sep)[0:-1]) + os.sep + fileName
        player.set_url( audioFile )

        soundParts = self.view.substr( self.view.sel()[0] ).split()
        start = 0
        end = 0
        for i in range( 0, len( soundParts ) ):
            if 'start' in soundParts[i]:
                start = float( soundParts[i + 1][0: -1] )
            if 'end' in soundParts[i]:
                end = float( soundParts[i + 1][0: -1] )

        player.setTrack( start, end - start )
        player.play()