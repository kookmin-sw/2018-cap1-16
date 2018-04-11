# Installing GPU Version of TensorFlow on Windows

* * *

## Requirements
* Python 3.6.2 or Anaconda 5.1
* CUDA® Toolkit 9.0
* cuDNN v7.0
* TensorFlow r1.5

## How to install
### Python
1. Download installer [Python 3.6.2](https://www.python.org/downloads/release/python-362/).
![PYTHON_1](./resource/Python/PYTHON_1.png)
2. Execute downloaded installer.
![PYTHON_2](./resource/Python/PYTHON_2.png)
3. Check "Add Python 3.6 to Path" and click "Insall Now" button.
![PYTHON_3](./resource/Python/PYTHON_3.png)
4. Click "Close" button and finish installation.
![PYTHON_4](./resource/Python/PYTHON_4.png)

### CUDA® Toolkit
1. Download [CUDA Toolkit 9.0](https://developer.nvidia.com/cuda-90-download-archive) that matches your version.
![CUDA_1](./resource/CUDA®_Toolkit/CUDA_1.png)
2. Execute downloaded installer.
![CUDA_2](./resource/CUDA®_Toolkit/CUDA_2.png)
3. Click "OK" and "Next" to proceed with the installation.
![CUDA_3](./resource/CUDA®_Toolkit/CUDA_3.png)
![CUDA_4](./resource/CUDA®_Toolkit/CUDA_4.png)
![CUDA_5](./resource/CUDA®_Toolkit/CUDA_5.png)
![CUDA_6](./resource/CUDA®_Toolkit/CUDA_6.png)
![CUDA_7](./resource/CUDA®_Toolkit/CUDA_7.png)
![CUDA_8](./resource/CUDA®_Toolkit/CUDA_8.png)
![CUDA_9](./resource/CUDA®_Toolkit/CUDA_9.png)
![CUDA_10](./resource/CUDA®_Toolkit/CUDA_10.png)
![CUDA_11](./resource/CUDA®_Toolkit/CUDA_11.png)
4. Execute patch file.
![CUDA_12](./resource/CUDA®_Toolkit/CUDA_12.png)
5. Click "OK" and "Next" to proceed with the installation.
![CUDA_13](./resource/CUDA®_Toolkit/CUDA_13.png)
![CUDA_14](./resource/CUDA®_Toolkit/CUDA_14.png)
![CUDA_15](./resource/CUDA®_Toolkit/CUDA_15.png)
![CUDA_16](./resource/CUDA®_Toolkit/CUDA_16.png)

### cuDNN
1. Download [cuDNN](https://developer.nvidia.com/cudnn) Version 7.0.
![cuDNN_1](./resource/cuDNN/cuDNN_1.png)
![cuDNN_2](./resource/cuDNN/cuDNN_2.png)
![cuDNN_3](./resource/cuDNN/cuDNN_3.png)
2. Extract downloaded file and place them in `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.0`.
![cuDNN_4](./resource/cuDNN/cuDNN_4.png)
![cuDNN_5](./resource/cuDNN/cuDNN_5.png)

### GPU Version of TensorFlow r1.7 - Python
1. Open command prompt, enter `pip3 install --upgrade tensorflow-gpu` to install TensorFlow.
![TensorFlow_1](./resource/Tensorflow/Tensorflow_1.png)
2. Enter `python` to run `python` and enter the following code to verify installed.
![TensorFlow_2](./resource/Tensorflow/Tensorflow_2.png)
```Python
import tensorflow as tf
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))
```
