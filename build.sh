ROOT=$(pwd)
export CC=/usr/bin/gcc
export CXX=/usr/bin/g++
export CUDAHOSTCXX=/usr/bin/g++

cd /kaolin && pip install -e .
cd ${ROOT}/BundleSDF/mycuda && rm -rf build *egg* && pip install -e .
cd ${ROOT}/BundleSDF/BundleTrack && rm -rf build && mkdir build && cd build && cmake .. && make -j11
