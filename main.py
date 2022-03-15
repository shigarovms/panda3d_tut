from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Disable the camera trackball controls.
        self.disableMouse()

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # Load and transform the panda actor.
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        # Loop its animation.
        self.pandaActor.loop("walk")

        # Create the 8 lerp intervals needed for the panda to
        # walk by square.
        SECS_PER_LINE = 1.0
        SECS_FOR_ROTATE = 0.4
        SQ_LNTH = 5
        posInterval1 = self.pandaActor.posInterval(SECS_PER_LINE,
                                                   Point3(SQ_LNTH, -SQ_LNTH, 0),
                                                   startPos=Point3(SQ_LNTH, SQ_LNTH, 0))
        posInterval2 = self.pandaActor.posInterval(SECS_PER_LINE,
                                                   Point3(-SQ_LNTH, -SQ_LNTH, 0),
                                                   startPos=Point3(SQ_LNTH, -SQ_LNTH, 0))
        posInterval3 = self.pandaActor.posInterval(SECS_PER_LINE,
                                                   Point3(-SQ_LNTH, SQ_LNTH, 0),
                                                   startPos=Point3(-SQ_LNTH, -SQ_LNTH, 0))
        posInterval4 = self.pandaActor.posInterval(SECS_PER_LINE,
                                                   Point3(SQ_LNTH, SQ_LNTH, 0),
                                                   startPos=Point3(-SQ_LNTH, SQ_LNTH, 0))
        hprInterval1 = self.pandaActor.hprInterval(SECS_FOR_ROTATE,
                                                   Point3(-90, 0, 0),
                                                   startHpr=Point3(0, 0, 0))
        hprInterval2 = self.pandaActor.hprInterval(SECS_FOR_ROTATE,
                                                   Point3(-180, 0, 0),
                                                   startHpr=Point3(-90, 0, 0))
        hprInterval3 = self.pandaActor.hprInterval(SECS_FOR_ROTATE,
                                                   Point3(-270, 0, 0),
                                                   startHpr=Point3(-180, 0, 0))
        hprInterval4 = self.pandaActor.hprInterval(SECS_FOR_ROTATE,
                                                   Point3(-360, 0, 0),
                                                   startHpr=Point3(-270, 0, 0))

        # Create and play the sequence that coordinates the intervals.
        self.pandaPace = Sequence(posInterval1, hprInterval1,
                                  posInterval2, hprInterval2,
                                  posInterval3, hprInterval3,
                                  posInterval4, hprInterval4,
                                  name="pandaPace")
        self.pandaPace.loop()

        global REC, VIDEO_DURATION

        if REC == 'on':
            self.movie(namePrefix = 'mediaContent/framesForMovie/moviePanda', duration = VIDEO_DURATION, fps = 12,
                  format = 'png', sd = 3, source = None)



    # Define a procedure to move the camera.

    def spinCameraTask(self, task):
        CAMERA_HIGHT = 20
        CAMERA_DEPTH = 47
        CAMERA_ANGLE = -22
        CAMERA_ROTATION_SPEED = 24.0
        angleDegrees = task.time * CAMERA_ROTATION_SPEED
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(CAMERA_DEPTH * sin(angleRadians), -CAMERA_DEPTH * cos(angleRadians), CAMERA_HIGHT)
        self.camera.setHpr(angleDegrees, CAMERA_ANGLE, 0)
        return Task.cont


REC = 'on'
VIDEO_DURATION = 5.0

app = MyApp()
app.run()

