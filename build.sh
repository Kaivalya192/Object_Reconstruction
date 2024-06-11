ROOT=$(pwd)
cd /kaolin && pip install -e .
cd ${ROOT}/BundleSDF/mycuda && rm -rf build *egg* && pip install -e .
cd ${ROOT}/BundleSDF/BundleTrack && rm -rf build && mkdir build && cd build && cmake .. && make -j11
