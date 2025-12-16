import os
import sys
import inspect
import pyrender
import pyrender.platforms.egl as egl_mod
import pyrender.platforms.pyglet_platform as pyglet_mod
import pyrender.viewer as viewer_mod

def patch_egl():
    egl_file = inspect.getfile(egl_mod)
    print(f"Patching {egl_file}")
    with open(egl_file, 'r') as f:
        content = f.read()

    # Patch 1: __init__
    old_init = """        if device is None:
            device = get_default_device()
        self._egl_device = device"""
    new_init = """        self._egl_device = None"""
    
    if old_init in content:
        content = content.replace(old_init, new_init)
    else:
        print("Warning: Could not find __init__ block in egl.py")

    # Patch 2: Import EGLError
    if "eglCreateContext, EGLConfig" in content and "EGLError" not in content:
        content = content.replace("eglCreateContext, EGLConfig", "EGLConfig, EGLError")

    # Patch 3: init_context logic
    old_block = """        # Cache DISPLAY if necessary and get an off-screen EGL display
        orig_dpy = None
        if 'DISPLAY' in os.environ:
            orig_dpy = os.environ['DISPLAY']
            del os.environ['DISPLAY']

        self._egl_display = self._egl_device.get_display()
        if orig_dpy is not None:
            os.environ['DISPLAY'] = orig_dpy

        # Initialize EGL
        assert eglInitialize(self._egl_display, major, minor)"""

    new_block = """        # Get the list of devices to try on
        if self._egl_device is None:
            if _eglQueryDevicesEXT is None:
                devices = (EGLDevice(None),)
            else:
                devices = query_devices()
        else:
            devices = (self._egl_device,)

        # Get the first EGL device that is working
        for i, device in enumerate(devices):
            # Cache DISPLAY if necessary and get an off-screen EGL display
            orig_dpy = None
            if 'DISPLAY' in os.environ:
                orig_dpy = os.environ['DISPLAY']
                del os.environ['DISPLAY']

            egl_display = device.get_display()
            if orig_dpy is not None:
                os.environ['DISPLAY'] = orig_dpy

            # Initialize EGL
            try:
                assert eglInitialize(egl_display, major, minor)
            except EGLError:
                # Ignore the error unless there is no device left to check
                if i == len(devices) - 1:
                    raise
                continue

            # Backup the device and display that will be used
            self._egl_device = device
            self._egl_display = egl_display
            break"""

    if old_block in content:
        content = content.replace(old_block, new_block)
    else:
        print("Warning: Could not find init_context block in egl.py")

    with open(egl_file, 'w') as f:
        f.write(content)

def patch_pyglet():
    pyglet_file = inspect.getfile(pyglet_mod)
    print(f"Patching {pyglet_file}")
    with open(pyglet_file, 'r') as f:
        content = f.read()
    
    old_except = "except pyglet.window.NoSuchConfigException as e:"
    new_except = "except (pyglet.window.NoSuchConfigException, pyglet.gl.ContextException):"
    
    if old_except in content:
        content = content.replace(old_except, new_except)
    else:
        print("Warning: Could not find except block in pyglet_platform.py")

    with open(pyglet_file, 'w') as f:
        f.write(content)

def patch_viewer():
    viewer_file = inspect.getfile(viewer_mod)
    print(f"Patching {viewer_file}")
    with open(viewer_file, 'r') as f:
        content = f.read()
    
    old_except = "except pyglet.window.NoSuchConfigException:"
    new_except = "except (pyglet.window.NoSuchConfigException, pyglet.gl.ContextException):"
    
    if old_except in content:
        content = content.replace(old_except, new_except)
    else:
        print("Warning: Could not find except block in viewer.py")

    with open(viewer_file, 'w') as f:
        f.write(content)

if __name__ == "__main__":
    try:
        patch_egl()
        patch_pyglet()
        patch_viewer()
        print("Patched pyrender successfully")
    except Exception as e:
        print(f"Error patching pyrender: {e}")
        sys.exit(1)
