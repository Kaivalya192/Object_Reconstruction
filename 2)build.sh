ROOT=$(pwd)
cd /kaolin && pip install -e .
cd ${ROOT}/BundleSDF/mycuda && rm -rf build *egg* && pip install -e .
cd ${ROOT}/BundleSDF/BundleTrack && rm -rf build && mkdir build && cd build && cmake .. && make -j11
conda install gcc=12.1.0 -y
pip install PyOpenGL-accelerate
