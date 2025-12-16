# Object_Reconstruction

## 1) Data Download

### Download Pretrained Weights for Segmentation Network

[XMem-s012.pth](https://drive.google.com/file/d/1LJ6U3NmI9MoUKG27mzqlgP1ioHWq-a5e/view?usp=sharing)

place them under `./XMem/saves/`

### Download Pretrained Weights for LoFTR

[outdoor_ds.ckpt](https://drive.google.com/drive/folders/11b1-Wzxcn7LpmTgHPqlC3H1ZzGsB6j6R?usp=sharing)

place them under `./BundleSDF/BundleTrack/LoFTR/weights/`


## 2) Docker Setup

To set up the Docker environment, run the following command:

```bash
docker build --network host -t nvcr.io/nvidian/bundlesdf .
```
## 3) Methodology
### Capture Data from RealSense Depth Camera

To capture data from a RealSense depth camera, run the `rec_con_mask.py` script.

<br>1)Install [librealsense SDK](https://github.com/IntelRealSense/librealsense) 
<br>2)Install dependencies for Xmem and Realsense
<br> conda environment (optional) 
```bash
conda create -n obj_recon python=3.10
```
```bash
pip install -r requirements.txt
```

#### Prepare Input Directory

Run
```bash
conda info --base
```
to get conda base directory. Copy the path and paste it in `capture.sh`. Then, run the following. 

```bash
sudo bash capture.sh
```
<br>Note : (Don't run in Docker Container)<br/>

Press `Enter` to start recording RGB and depth frames. Then, create a boundary by selecting points on the window to create a mask for the first image.

### Steps to Run

1. Run the container:

    ```bash
    bash run_container.sh
    ```

2. Build the project:

    ```bash
    bash build.sh
    ```

3. Run the project:

    ```bash
    bash run.sh
    ```
