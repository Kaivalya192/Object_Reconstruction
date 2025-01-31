ROOT=$(pwd)
cd /kaolin && CXX=g++-9 CC=gcc-9 LD=g++-9 pip install -e .
cd ${ROOT}/BundleSDF/mycuda && rm -rf build *egg* && CXX=g++-9 CC=gcc-9 LD=g++-9 pip install -e .
pip install yacs
cp -r /usr/include/flann /usr/local/include/flann
cp -r /usr/include/boost /usr/local/include/boost
cp  /usr/include/zmq_addon.hpp /usr/local/include/
cp  /usr/include/zmq.h /usr/local/include/
cp  /usr/include/zmq.hpp /usr/local/include/
cd ${ROOT}/BundleSDF/BundleTrack && rm -rf build && mkdir build && cd build && cmake .. && make -j11
