<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="logo.png" alt="Logo" width="100" height="100">
  </a>

  <h3 align="center">Style Transfer</h3>

  <p align="center">
    Photo Realistic Style Transfer
    <br />
    <a href="./docs/_build/html/index.html"><strong>Explore the docs »</strong></a>
    <br />
    <br />

</div>






<!-- ABOUT THE PROJECT -->
## About The Project

The project consists of two different stages that are connected using internal APIs. The first stage generates image semantic segmentation masks for both input images. The second stage which is based on the WCT2 model, preforms the style transfer using the base images and their masks. Note that the purpose of this project is too preform photo realistic style transfer so the results are far less dramatic than traditional models.

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- GETTING STARTED -->
## Getting Started


### Installation

To install all of the requirement, use the install.sh script.

  ```sh
  ./install.sh
  ```



<!-- USAGE EXAMPLES -->
## Usage

After seting up the conda env and downloading the weights using the script, run the main.py file in the parrent dir and setup the fast API server, then use the given API address to test the program using tester/main.py.

``` bash

# run inference server
python3 main.py

# run test module
python3 ./tester/main.py --api_url http://127.0.0.1:8000/upload_images/ --content_image content.png --style_image style.png --alpha 1 --size 400
          
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>






## Challenges

### Data Preprocessing

As this is a general task, collecting data and training a model from scratch is not reasonable. As such I'm using two modified versions of resnet50 for the encoder and decoder stage of the segmentation model. WCT2 also comes with pretrained weights, though you could construct a coco dataset to fine-tune it further.

### Algorithm

The semantic segmentation stage of the pipeline could be swapped for almost any model that preforms the same task but this model specifically was chosen as a compromise between performance and inference latency. As for WCT2, you can find the detailed explanation of its workings [here](https://arxiv.org/pdf/1903.09760.pdf), but in essence it is based on VGG (VGG is used as a backbone in most style transfer models. Although other CNN-based or Vision Transformers do outperform it in most tasks, it's many convolution layers, make it superior for style transfer tasks) and uses a novel idea called *Wavelet Transform*.

### Metrics

Due to nature of this task, there really isn't an objective measurement for checking the model’s performance, the only way practical approach is to use focus groups.

### Limitations

1. Hardware access: To truly be able to assess different models and solutions GPUs with lots and lots of VRAM is a must. Although solutions like Kaggle, Google colab, Azure, etc., exist, they are not really suitable for large projects.

2. Slow and Broken Connections: simple thing like downloading model weights, installing pip packages or a simple driver can be a headache if some link in the middle is broken. Downloading a 5GB toolkit is no fun at 240KB/s. It can slow down the process immensely and it is extremely frustrating.

3. Old Broken code: Many models are simply implementations of research papers and not only they are not actively maintained, they are often poorly written implementations, resulting in excessive VRAM use, being difficult to integrate into active projects, reliance on deprecated tools or simply not working. So, I have had to spend a substantial amount of time refactoring code.

