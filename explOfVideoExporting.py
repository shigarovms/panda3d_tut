import subprocess, sys
from direct.showbase.ShowBase import ShowBase
from panda3d.core import ClockObject

cmdstring = ('ffmpeg.exe',  # put it in the same dir
             '-y',  # overwrite the file w/o warning
             '-r', '%f' % 30.0,  # frame rate of encoded video
             '-an',  # no audio
             '-analyzeduration', '0',  # skip auto codec analysis
             # input params
             '-s', '800x600',  # default panda window size
             '-f', 'rawvideo',  # RamImage buffer is raw buffer
             '-pix_fmt', 'rgba',  # format of panda texure RamImage buffer
             '-i', '-',  # this means a pipe
             # output params
             # '-vtag', 'xvid',
             '-vcodec', 'mpeg4',
             'test.avi')

p = subprocess.Popen(
    cmdstring,
    stdin=subprocess.PIPE,
    bufsize=-1,
    shell=False,
)


class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.enclosure = loader.loadModel("models/enclosure/enclosure.egg")
        self.enclosure.reparentTo(render)

        self.accept("escape", self.OnQuit)  # Escape quits

        fps = 30.0
        globalClock = ClockObject.getGlobalClock()
        globalClock.setMode(ClockObject.MNonRealTime)
        globalClock.setDt(1.0 / float(fps))
        t = taskMgr.add(self.updateTask, "ffmpegTask")
        t.setUponDeath(lambda state: globalClock.setMode(ClockObject.MNormal))

    def OnQuit(self):
        p.stdin.close()  # close the pipe so that ffmpeg will clsoe the avi file properly
        sys.exit()  # finally exits.

    def updateTask(self, task):
        # https://www.panda3d.org/reference/1.9.0/python/panda3d.core.GraphicsOutput#a340026249c6d0c504da743305c7db94a
        tex = base.win.getScreenshot()  # this gives you a texture object
        buf = tex.getRamImage().getData()  # 800*600*4 = 1920000
        p.stdin.write(buf)  # pass it to ffmpeg as text buffer
        return task.cont


app = App()
base.run()  # start panda loop

