#!/usr/bin/env python
import vapoursynth as vs
core = vs.get_core()

clip = core.ffms2.Source("tests/test.webm")
clip.set_output()