import os
import sys
import inspect
import pyrender
import pyrender.platforms.pyglet_platform as pyglet_mod
import pyrender.viewer as viewer_mod

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
        patch_pyglet()
        patch_viewer()
        print("Patched pyrender successfully")
    except Exception as e:
        print(f"Error patching pyrender: {e}")
        sys.exit(1)