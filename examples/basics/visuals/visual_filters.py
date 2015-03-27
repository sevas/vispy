# -*- coding: utf-8 -*-
# vispy: gallery 1
# Copyright (c) 2014, Vispy Development Team.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.

"""
Demonstration of Line visual with arbitrary transforms.

Several Line visuals are displayed that all have the same vertex position
information, but different transformations.
"""

import numpy as np
from vispy import app, gloo, visuals
from vispy.visuals.transforms import (STTransform, LogTransform,
                                      AffineTransform, PolarTransform)
from vispy.visuals.components import Clipper, Alpha, ColorFilter
from vispy.visuals.shaders import Function
import vispy.util

# vertex positions of data to draw
N = 400
pos = np.zeros((N, 2), dtype=np.float32)
pos[:, 0] = np.linspace(0, 350, N)
pos[:, 1] = np.random.normal(size=N, scale=20, loc=0)


class Canvas(app.Canvas):
    def __init__(self):

        # Define several Line visuals that use the same position data
        self.lines = [visuals.LineVisual(pos=pos)
                      for i in range(6)]

        self.lines[0].transform = STTransform(translate=(0, 50))
        
        self.lines[1].transform = STTransform(translate=(400, 50))
        self.lines[1].attach(Clipper([500, 725, 200, 50]))
        
        self.lines[2].transform = STTransform(translate=(0, 150))
        self.lines[2].attach(Alpha(0.4))
        
        self.lines[3].transform = STTransform(translate=(400, 150))
        self.lines[3].attach(ColorFilter([1, 0, 0, 1]))
        
        # a custom filter
        class Hatching(object):
            def __init__(self):
                self.shader = Function("""
                    void screen_filter() {
                        float f = gl_FragCoord.x * 0.4 + gl_FragCoord.y;
                        f = mod(f, 20);
                        
                        if( f < 5.0 ) {
                            discard;
                        }
                        
                        if( f < 20.0 ) {
                            gl_FragColor.g = gl_FragColor.g + 0.05 * (20-f);
                        }
                    }
                """)
            
            def _attach(self, visual):
                visual._get_hook('frag', 'post').add(self.shader())

        self.lines[4].transform = STTransform(translate=(0, 250))
        self.lines[4].attach(Hatching())
        
        # mixing filters
        self.lines[5].transform = STTransform(translate=(400, 250))
        self.lines[5].attach(ColorFilter([1, 0, 0, 1]))
        self.lines[5].attach(Hatching())
        
        

        app.Canvas.__init__(self, keys='interactive')
        self.size = (800, 800)
        
        for line in self.lines:
            tr_sys = visuals.transforms.TransformSystem(self)
            tr_sys.visual_to_document = line.transform
            line.tr_sys = tr_sys

        self.show(True)

    def on_draw(self, ev):
        gloo.clear('black', depth=True)
        gloo.set_viewport(0, 0, *self.size)
        for line in self.lines:
            line.draw(line.tr_sys)


if __name__ == '__main__':
    win = Canvas()
    import sys
    if sys.flags.interactive != 1:
        app.run()
