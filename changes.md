### Pyrender Offscreen Rendering Error
Similar to this https://github.com/Genesis-Embodied-AI/Genesis/issues/259


[BUG FIX] Fix EGL device detection. #807 https://github.com/Genesis-Embodied-AI/Genesis/pull/807#issue-2886569485

### Ensure the following
```bash
(py38) root@iitgn:/# pip install --upgrade PyOpenGL PyOpenGL_accelerate
(py38) root@iitgn:/# python 
Python 3.8.20 | packaged by conda-forge | (default, Sep 30 2024, 17:52:49) 
[GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pyrender
>>> pyrender.__version__
'0.1.45'
>>> import networkx
>>> networkx.__version__
'2.8'
>>> import OpenGL
>>> OpenGL.__version__
'3.1.10'
>>> exit()
```

### Resources:
https://pyrender.readthedocs.io/en/latest/examples/offscreen.html
