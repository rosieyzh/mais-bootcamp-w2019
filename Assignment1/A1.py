{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Assignment 1"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "This assignment provides a brief introduction to the machine learning process that we will cover in depth in this course. We want to show a simple workflow of how you can use the sklearn library for machine learning. We will be using the MNIST handwritten digits dataset to dive into the machine learning process."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Imports"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "First let us import some libraries.\n",
    "\n",
    "1) numpy - http://www.numpy.org/ - A library for dealing with N-dimensional arrays in python. Numpy provides efficient implementations of common numerical computations used in linear algebra.\n",
    "\n",
    "2) sklearn - https://scikit-learn.org/stable/ - A data analysis library that provides implementations of many machine learning algorithms (and much more!).\n",
    "\n",
    "3) matplotlib - https://matplotlib.org/ - A python 2D plotting library used for visualizations (data, charts, etc.)\n",
    "\n",
    "These libraries (and many more) are often used together and built on top of each other. For example, sklearn depends on numpy and uses numpy arrays under the hood."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "%matplotlib inline\n",
    "\n",
    "from scipy import io\n",
    "from sklearn.datasets import fetch_mldata\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.preprocessing import OneHotEncoder\n",
    "from sklearn.metrics import accuracy_score\n",
    "from sklearn.linear_model import LinearRegression, Ridge, LogisticRegression\n",
    "from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier\n",
    "from sklearn.svm import LinearSVC, SVC\n",
    "from sklearn.decomposition import PCA\n",
    "from sklearn.neural_network import MLPClassifier"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "For this homework assignment, we will be using the MNIST dataset. The MNIST data is a collection of black and white 28x28 images, each picturing a handwritten digit. These were collected from digits people write at the post office, and now this dataset is a standard benchmark to evaluate models against used in the machine learning community. We have provided the .mat file in the assignment repository."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "mnist = io.loadmat('mnist-original.mat', struct_as_record=True)\n",
    "X = mnist['data'].astype('float64').T # Transpose the matrix because we want each row to be an example\n",
    "y = mnist['label'].astype('int64').T"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Data Exploration"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Let us first explore this data a little bit."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(70000, 784) (70000, 1)\n"
     ]
    }
   ],
   "source": [
    "print(X.shape, y.shape)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The X matrix here contains all the digit pictures. The data is (n_samples x n_features), meaning this data contains 70000 pictures, each with 784 features (the 28x28 image is flattened into a single row). The y vector contains the label for each digit, so we know which digit (or class - class means category) is in each picture."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Let's try and visualize this data a bit. Change around the index variable to explore more."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[[  0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.\n",
      "    0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.\n",
      "    0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.\n",
      "    0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.\n",
      "    0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.\n",
      "    0.  51. 159. 253. 159.  50.   0.   0.   0.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.\n",
      "   48. 238. 252. 252. 252. 237.   0.   0.   0.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.  54.\n",
      "  227. 253. 252. 239. 233. 252.  57.   6.   0.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.  10.  60. 224.\n",
      "  252. 253. 252. 202.  84. 252. 253. 122.   0.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0. 163. 252. 252.\n",
      "  252. 253. 252. 252.  96. 189. 253. 167.   0.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.   0.   0.   0.   0.  51. 238. 253. 253.\n",
      "  190. 114. 253. 228.  47.  79. 255. 168.   0.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.   0.   0.   0.  48. 238. 252. 252. 179.\n",
      "   12.  75. 121.  21.   0.   0. 253. 243.  50.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.   0.   0.  38. 165. 253. 233. 208.  84.\n",
      "    0.   0.   0.   0.   0.   0. 253. 252. 165.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.   0.   7. 178. 252. 240.  71.  19.  28.\n",
      "    0.   0.   0.   0.   0.   0. 253. 252. 195.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.   0.  57. 252. 252.  63.   0.   0.   0.\n",
      "    0.   0.   0.   0.   0.   0. 253. 252. 195.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.   0. 198. 253. 190.   0.   0.   0.   0.\n",
      "    0.   0.   0.   0.   0.   0. 255. 253. 196.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.  76. 246. 252. 112.   0.   0.   0.   0.\n",
      "    0.   0.   0.   0.   0.   0. 253. 252. 148.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.  85. 252. 230.  25.   0.   0.   0.   0.\n",
      "    0.   0.   0.   0.   7. 135. 253. 186.  12.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.  85. 252. 223.   0.   0.   0.   0.   0.\n",
      "    0.   0.   0.   7. 131. 252. 225.  71.   0.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.  85. 252. 145.   0.   0.   0.   0.   0.\n",
      "    0.   0.  48. 165. 252. 173.   0.   0.   0.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.  86. 253. 225.   0.   0.   0.   0.   0.\n",
      "    0. 114. 238. 253. 162.   0.   0.   0.   0.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.  85. 252. 249. 146.  48.  29.  85. 178.\n",
      "  225. 253. 223. 167.  56.   0.   0.   0.   0.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.  85. 252. 252. 252. 229. 215. 252. 252.\n",
      "  252. 196. 130.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.  28. 199. 252. 252. 253. 252. 252. 233.\n",
      "  145.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.   0.  25. 128. 252. 253. 252. 141.  37.\n",
      "    0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.\n",
      "    0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.\n",
      "    0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.\n",
      "    0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.]\n",
      " [  0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.\n",
      "    0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.]]\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "<matplotlib.image.AxesImage at 0x156e8685748>"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAP8AAAEICAYAAACQ6CLfAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADl0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uIDMuMC4yLCBodHRwOi8vbWF0cGxvdGxpYi5vcmcvOIA7rQAAEQJJREFUeJzt3X2QVfV9x/H3xyfiEwS1KhWJqcVOTaurIGUaJxLTpFbtQMZBZYzQyXSwM3FibOpULQpptck4an3o6EiUig8BVDSg1RBHjKZTa13RKolNwjiIhC2IT6wx1Qjf/nHPdhbc+7t379O5y+/zmtnZu+d7zr1fLvvZc+79nXN/igjMLD97lN2AmZXD4TfLlMNvlimH3yxTDr9Zphx+s0w5/GaZcvh3Q5J+JOkvW72tpMsl3d7AfYakX0m6us71v1WsH5L2Gu7jWX0c/i4mab2kPym7jwER8Y8R0dAfFeD4iPi7gR8k9Uh6XtL7xfeeQY8zH/hMs/1amsNvHSdpH2AFcA8wFlgMrCiWW4c4/COQpLGSHpH0hqS3i9vjd1ntaEn/KeldSSskHTRo+6mS/l3SO5L+S9K0Oh93gaR7itufkHSPpDeL+3lO0mF1/hOmAXsBN0TEBxFxEyDg1Dq3txZw+EemPYB/AT4FTAB+DfzzLuvMBr4K/DbwEXATgKQjgH8FrgIOAv4GWC7pt4bZwxxgDHAkcDDwV0Uf9fgM8FLsfGHJS/hQv6Mc/hEoIt6MiOUR8X5E9ANXA6fsstrdEbE2In4FXAGcLWlP4CvAoxHxaETsiIjHgV7g9GG28Rsqof/diNgeEc9HxLY6tz0AeHeXZe8CBw6zB2uCwz8CSdpP0m2SXpO0DXga+GQR7gGvD7r9GrA3cAiVo4WZxaH6O5LeAU4Gxg2zjbuBVcBSSZskXSNp7zq3fQ8Yvcuy0UD/MHuwJjj8I9M3gd8D/igiRgOfK5Zr0DpHDro9gcqeeiuVPwp3R8QnB33tHxHfGU4DEfGbiPhWRBwL/DFwJpWXGvX4CXCcpMH9Hlcstw5x+Lvf3sWbawNfe1E5PP418E7xRt78Ibb7iqRjJe0H/D3wQERsp/IO+59L+lNJexb3OW2INwyTJH1e0h8WRxvbqPxx2V7n5j8q1v26pFGSLiyWrx5OD9Ych7/7PUol6ANfC4AbgH2p7Mn/A/jBENvdDdwJ/A/wCeDrABHxOjAduBx4g8qRwCUM/3fhcOABKsF/BXiKyh+WmiLiQ2AGlSOFd6i8MTmjWG4dIn+Sj7WbpP8FPgBuiogr6lh/PvDXwChg/+KIxVrM4TfLlA/7zTLl8JtlqqNXTEnyawyzNosI1V6ryT2/pNMk/UzSOkmXNnNfZtZZDb/hV4zv/hz4IrAReA6YFRE/TWzjPb9Zm3Vizz8FWBcRrxbjs0upjB+b2QjQTPiPYOfzxzcWy3Yiaa6kXkm9TTyWmbVYM2/4DXVo8bHD+ohYCCwEH/abdZNm9vwb2fnikfHApubaMbNOaSb8zwETJX26+Pilc4GVrWnLzNqt4cP+iPiouBprFbAnsCgifEmm2QjR0XP7/ZrfrP06cpKPmY1cDr9Zphx+s0w5/GaZcvjNMuXwm2XK4TfLlMNvlimH3yxTDr9Zphx+s0w5/GaZcvjNMuXwm2XK4TfLlMNvlimH3yxTDr9Zphx+s0w5/GaZcvjNMtXRKbpt9zNp0qRk/cILL6xamz17dnLbu+66K1m/+eabk/U1a9Yk67nznt8sUw6/WaYcfrNMOfxmmXL4zTLl8JtlyuE3y5Rn6bWknp6eZH316tXJ+ujRo1vZzk7efffdZP3ggw9u22N3s3pn6W3qJB9J64F+YDvwUURMbub+zKxzWnGG3+cjYmsL7sfMOsiv+c0y1Wz4A/ihpOclzR1qBUlzJfVK6m3yscyshZo97P9sRGySdCjwuKT/joinB68QEQuBheA3/My6SVN7/ojYVHzfAjwETGlFU2bWfg2HX9L+kg4cuA18CVjbqsbMrL2aOew/DHhI0sD9fC8iftCSrqxjpkxJH6wtX748WR8zZkyynjqPpL+/P7nthx9+mKzXGsefOnVq1Vqta/1rPfbuoOHwR8SrwPEt7MXMOshDfWaZcvjNMuXwm2XK4TfLlMNvlilf0rsb2G+//arWTjzxxOS299xzT7I+fvz4ZL0Y6q0q9ftVa7jtmmuuSdaXLl2arKd6mzdvXnLbb3/728l6N6v3kl7v+c0y5fCbZcrhN8uUw2+WKYffLFMOv1mmHH6zTHmK7t3AbbfdVrU2a9asDnYyPLXOQTjggAOS9aeeeipZnzZtWtXacccdl9w2B97zm2XK4TfLlMNvlimH3yxTDr9Zphx+s0w5/GaZ8jj/CDBp0qRk/Ywzzqhaq3W9fS21xtIffvjhZP3aa6+tWtu0aVNy2xdeeCFZf/vtt5P1U089tWqt2edld+A9v1mmHH6zTDn8Zply+M0y5fCbZcrhN8uUw2+WKX9ufxfo6elJ1levXp2sjx49uuHHfuyxx5L1Wp8HcMoppyTrqevmb7/99uS2b7zxRrJey/bt26vW3n///eS2tf5dteYcKFPLPrdf0iJJWyStHbTsIEmPS/pF8X1sM82aWefVc9h/J3DaLssuBZ6IiInAE8XPZjaC1Ax/RDwNvLXL4unA4uL2YmBGi/syszZr9Nz+wyKiDyAi+iQdWm1FSXOBuQ0+jpm1Sdsv7ImIhcBC8Bt+Zt2k0aG+zZLGARTft7SuJTPrhEbDvxKYU9yeA6xoTTtm1ik1x/klLQGmAYcAm4H5wPeB+4AJwAZgZkTs+qbgUPeV5WH/Mccck6zPnz8/WT/33HOT9a1bt1at9fX1Jbe96qqrkvUHHnggWe9mqXH+Wr/3y5YtS9bPO++8hnrqhHrH+Wu+5o+Iamd5fGFYHZlZV/HpvWaZcvjNMuXwm2XK4TfLlMNvlil/dHcLjBo1KllPfXw1wOmnn56s9/f3J+uzZ8+uWuvt7U1uu++++ybruZowYULZLbSd9/xmmXL4zTLl8JtlyuE3y5TDb5Yph98sUw6/WaY8zt8CJ5xwQrJeaxy/lunTpyfrtabRNhuK9/xmmXL4zTLl8JtlyuE3y5TDb5Yph98sUw6/WaY8zt8C119/fbIupT9JudY4vcfxG7PHHtX3bTt27OhgJ93Je36zTDn8Zply+M0y5fCbZcrhN8uUw2+WKYffLFMe56/TmWeeWbXW09OT3LbWdNArV65sqCdLS43l1/o/efHFF1vdTtepueeXtEjSFklrBy1bIOmXkl4svpr7tAoz67h6DvvvBE4bYvk/RURP8fVoa9sys3arGf6IeBp4qwO9mFkHNfOG34WSXipeFoyttpKkuZJ6JaUnjTOzjmo0/LcCRwM9QB9wXbUVI2JhREyOiMkNPpaZtUFD4Y+IzRGxPSJ2AN8FprS2LTNrt4bCL2ncoB+/DKyttq6Zdaea4/ySlgDTgEMkbQTmA9Mk9QABrAcuaGOPXSE1j/0+++yT3HbLli3J+rJlyxrqaXc3atSoZH3BggUN3/fq1auT9csuu6zh+x4paoY/ImYNsfiONvRiZh3k03vNMuXwm2XK4TfLlMNvlimH3yxTvqS3Az744INkva+vr0OddJdaQ3nz5s1L1i+55JJkfePGjVVr111X9aRUAN57771kfXfgPb9Zphx+s0w5/GaZcvjNMuXwm2XK4TfLlMNvlimP83dAzh/NnfpY81rj9Oecc06yvmLFimT9rLPOStZz5z2/WaYcfrNMOfxmmXL4zTLl8JtlyuE3y5TDb5Ypj/PXSVJDNYAZM2Yk6xdddFFDPXWDiy++OFm/4oorqtbGjBmT3Pbee+9N1mfPnp2sW5r3/GaZcvjNMuXwm2XK4TfLlMNvlimH3yxTDr9ZpuqZovtI4C7gcGAHsDAibpR0ELAMOIrKNN1nR8Tb7Wu1XBHRUA3g8MMPT9ZvuummZH3RokXJ+ptvvlm1NnXq1OS2559/frJ+/PHHJ+vjx49P1jds2FC1tmrVquS2t9xyS7Juzalnz/8R8M2I+H1gKvA1SccClwJPRMRE4IniZzMbIWqGPyL6ImJNcbsfeAU4ApgOLC5WWwykT2Mzs64yrNf8ko4CTgCeBQ6LiD6o/IEADm11c2bWPnWf2y/pAGA58I2I2FbrfPZB280F5jbWnpm1S117fkl7Uwn+vRHxYLF4s6RxRX0csGWobSNiYURMjojJrWjYzFqjZvhV2cXfAbwSEdcPKq0E5hS35wDpj1I1s66iWsNUkk4Gfgy8TGWoD+ByKq/77wMmABuAmRHxVo37Sj9YF5s5c2bV2pIlS9r62Js3b07Wt23bVrU2ceLEVrezk2eeeSZZf/LJJ6vWrrzyyla3Y0BE1PWavOZr/oj4N6DanX1hOE2ZWffwGX5mmXL4zTLl8JtlyuE3y5TDb5Yph98sUzXH+Vv6YCN4nD916er999+f3Pakk05q6rFrnUrdzP9h6nJggKVLlybrI/ljx3dX9Y7ze89vlimH3yxTDr9Zphx+s0w5/GaZcvjNMuXwm2XK4/wtMG7cuGT9ggsuSNbnzZuXrDczzn/jjTcmt7311luT9XXr1iXr1n08zm9mSQ6/WaYcfrNMOfxmmXL4zTLl8JtlyuE3y5TH+c12Mx7nN7Mkh98sUw6/WaYcfrNMOfxmmXL4zTLl8Jtlqmb4JR0p6UlJr0j6iaSLiuULJP1S0ovF1+ntb9fMWqXmST6SxgHjImKNpAOB54EZwNnAexFxbd0P5pN8zNqu3pN89qrjjvqAvuJ2v6RXgCOaa8/Myjas1/ySjgJOAJ4tFl0o6SVJiySNrbLNXEm9knqb6tTMWqruc/slHQA8BVwdEQ9KOgzYCgTwD1ReGny1xn34sN+szeo97K8r/JL2Bh4BVkXE9UPUjwIeiYg/qHE/Dr9Zm7Xswh5VPjr2DuCVwcEv3ggc8GVg7XCbNLPy1PNu/8nAj4GXgR3F4suBWUAPlcP+9cAFxZuDqfvynt+szVp62N8qDr9Z+/l6fjNLcvjNMuXwm2XK4TfLlMNvlimH3yxTDr9Zphx+s0w5/GaZcvjNMuXwm2XK4TfLlMNvlimH3yxTNT/As8W2Aq8N+vmQYlk36tbeurUvcG+NamVvn6p3xY5ez/+xB5d6I2JyaQ0kdGtv3doXuLdGldWbD/vNMuXwm2Wq7PAvLPnxU7q1t27tC9xbo0rprdTX/GZWnrL3/GZWEoffLFOlhF/SaZJ+JmmdpEvL6KEaSeslvVxMO17q/ILFHIhbJK0dtOwgSY9L+kXxfcg5EkvqrSumbU9MK1/qc9dt0913/DW/pD2BnwNfBDYCzwGzIuKnHW2kCknrgckRUfoJIZI+B7wH3DUwFZqka4C3IuI7xR/OsRHxt13S2wKGOW17m3qrNq38X1Dic9fK6e5boYw9/xRgXUS8GhEfAkuB6SX00fUi4mngrV0WTwcWF7cXU/nl6bgqvXWFiOiLiDXF7X5gYFr5Up+7RF+lKCP8RwCvD/p5IyU+AUMI4IeSnpc0t+xmhnDYwLRoxfdDS+5nVzWnbe+kXaaV75rnrpHp7lutjPAPNZVQN403fjYiTgT+DPhacXhr9bkVOJrKHI59wHVlNlNMK78c+EZEbCuzl8GG6KuU562M8G8Ejhz083hgUwl9DCkiNhXftwAPUXmZ0k02D8yQXHzfUnI//y8iNkfE9ojYAXyXEp+7Ylr55cC9EfFgsbj0526ovsp63soI/3PAREmflrQPcC6wsoQ+PkbS/sUbMUjaH/gS3Tf1+EpgTnF7DrCixF520i3TtlebVp6Sn7tum+6+lDP8iqGMG4A9gUURcXXHmxiCpN+hsreHyuXO3yuzN0lLgGlULvncDMwHvg/cB0wANgAzI6Ljb7xV6W0aw5y2vU29VZtW/llKfO5aOd19S/rx6b1mefIZfmaZcvjNMuXwm2XK4TfLlMNvlimH3yxTDr9Zpv4PJP0oHivqnmcAAAAASUVORK5CYII=\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "index = 0 #15000, 28999, 67345\n",
    "image = X[index].reshape((28, 28))\n",
    "print(image) # Shows the pixel values at each cell in the matrix. Ranges from 0-255\n",
    "plt.title('Label is ' + str(y[index]))\n",
    "plt.imshow(image, cmap='gray')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Notice that each pixel value ranges from 0-255. When we train our models, a good practice is to *standardize* the data so different features can be compared more equally (it also speeds up computation). Here we will use a simple standardization, squeezing all values into the [0, 1] interval range. This kind of standardization is called min-max normalization. For other methods, see https://en.wikipedia.org/wiki/Feature_scaling"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "X = X / 255 # Shorthand for dividing all values in the X matrix by 255. Numpy provides lots of shortcuts like this."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "When we train our model, we want it to have the lowest error. Error presents itself in 2 ways: bias (how close our model is to the ideal model), and variance (how much our model varies with different datasets). If we train our model on a chunk of data, and then test our model on that same data, we will only witness the first type of error - bias. However, if we test on new, unseen data, that will reflect both bias and variance. This is the reasoning behind cross validation."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "So, we want to have 2 datasets, train and test, each used for the named purpose exclusively."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(52500, 784) (17500, 784)\n"
     ]
    }
   ],
   "source": [
    "print(X_train.shape, X_test.shape)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Applying Models"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now we will walk you through applying various models to try and achieve the lowest error rate on this data."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Each of our labels is a number from 0-9. That is, our labels are categorical. If we simply did regression on this data, the labels would imply some sort of ordering and distance between the classes (imagine we were classing colors instead, there is no notion of distance or order i.e. 8 is not \"more\" of a digit than 7). We can fix this issue by one-hot encoding our labels. So, instead of each label being a simple digit, each label is a vector of 10 entries. 9 of those entries are zero, and only 1 entry is equal to one, corresponding to the index of the digit. This way, the distance between the labels are the same."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\georg\\.mais-env\\lib\\site-packages\\sklearn\\preprocessing\\_encoders.py:368: FutureWarning: The handling of integer data will change in version 0.22. Currently, the categories are determined based on the range [0, max(values)], while in the future they will be determined based on the unique values.\n",
      "If you want the future behaviour and silence this warning, you can specify \"categories='auto'\".\n",
      "In case you used a LabelEncoder before this OneHotEncoder to convert the categories to integers, then you can now use the OneHotEncoder directly.\n",
      "  warnings.warn(msg, FutureWarning)\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "(70000, 10)"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "enc = OneHotEncoder(sparse=False)\n",
    "y_hot = enc.fit_transform(y.reshape(-1, 1))\n",
    "y_train_hot = enc.transform(y_train.reshape(-1, 1))\n",
    "y_hot.shape"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Remember how the first sample is the digit zero? Let's now look at the new label at that index."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([1., 0., 0., 0., 0., 0., 0., 0., 0., 0.])"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "y_hot[0]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Linear Regression"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "There are 3 steps to build your model: \n",
    "\n",
    "1) Create the model\n",
    "\n",
    "2) Train the model\n",
    "\n",
    "3) Use your model to make predictions\n",
    "\n",
    "In the sklearn API, this is made very clear. First you instantiate the model (constructor), then you call train it with the `fit` method, then you can make predictions on new data with the `test` method."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "First, let's do a basic linear regression."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "LinearRegression(copy_X=True, fit_intercept=True, n_jobs=None,\n",
       "         normalize=False)"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Instantiate the model\n",
    "linear = LinearRegression()\n",
    "# Fit the model (train)\n",
    "linear.fit(X_train, y_train_hot)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "train acc:  0.8597142857142858\n",
      "test acc:  0.8502857142857143\n"
     ]
    }
   ],
   "source": [
    "# use trained model to predict both train and test sets\n",
    "y_train_pred = linear.predict(X_train)\n",
    "y_test_pred = linear.predict(X_test)\n",
    "\n",
    "# print accuracies\n",
    "print('train acc: ', accuracy_score(y_train_pred.argmax(axis=1), y_train))\n",
    "print('test acc: ', accuracy_score(y_test_pred.argmax(axis=1), y_test))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Note on interpretability: you can view the weights of your model with `linear.coef_`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Ridge Regression"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Ridge Regression (L2) is one method of preventing a common problem in machine learning called \"overfitting\". Remember when we split our examples into training and test sets? Overfitting occurs when the model performs well on the training set but not on the test set. This means that the model does not generalize well to previously unseen examples.\n",
    "\n",
    "Let us try Ridge Regression and see if we get better results"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "train acc:  0.8602857142857143\n",
      "test acc:  0.8512\n"
     ]
    }
   ],
   "source": [
    "ridge = Ridge(alpha=0.3)\n",
    "ridge.fit(X_train, y_train_hot)\n",
    "print('train acc: ', accuracy_score(ridge.predict(X_train).argmax(axis=1), y_train))\n",
    "print('test acc: ', accuracy_score(ridge.predict(X_test).argmax(axis=1), y_test))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The alpha controls how much to penalize the weights. Play around with it to see if you can improve the test accuracy."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now you have seen how to use some basic models to fit and evaluate your data. You will now walk through working with more models. Fill in code where needed."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Logistic Regression"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We will now do logistic regression. From now on, the models will automatically one-hot the labels (so we don't need to worry about it)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\georg\\.mais-env\\lib\\site-packages\\sklearn\\utils\\validation.py:761: DataConversionWarning: A column-vector y was passed when a 1d array was expected. Please change the shape of y to (n_samples, ), for example using ravel().\n",
      "  y = column_or_1d(y, warn=True)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "train acc:  0.929847619047619\n",
      "test acc:  0.9212\n"
     ]
    }
   ],
   "source": [
    "logreg = LogisticRegression(C=0.25, multi_class='multinomial', solver='saga', tol=0.1)\n",
    "logreg.fit(X_train, y_train)\n",
    "print('train acc: ', accuracy_score(logreg.predict(X_train), y_train))\n",
    "print('test acc: ', accuracy_score(logreg.predict(X_test), y_test))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Our accuracy has jumped ~5%! Why is this? Logistic Regression is a more complex model - instead of computing raw scores as in linear regression, it does one extra step and squashes values between 0 and 1. This means our model now optimizes over *probabilities* instead of raw scores. This makes sense since our vectors are 1-hot encoded."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The C hyperparameter controls inverse regularization strength (inverse for this model only). Reguralization is important to make sure our model doesn't overfit (perform much better on train data than test data). Play around with the C parameter to try and get better results! You should be able to hit 92%."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Question 1) Random Forest"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Decision Trees are a completely different type of classifier. They essentially break up the possible space by repeatedly \"splitting\" on features to keep narrowing down the possibilities. Decision Trees are normally individually very week, so we typically average them together in bunches called Random Forest."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now you have seen many examples for how to construct, fit, and evaluate a model. Now do the same for Random Forest using the [documentation here](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html). You should be able to create one easily without needing to specify any constructor parameters."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 48,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\georg\\.mais-env\\lib\\site-packages\\ipykernel_launcher.py:4: DataConversionWarning: A column-vector y was passed when a 1d array was expected. Please change the shape of y to (n_samples,), for example using ravel().\n",
      "  after removing the cwd from sys.path.\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "train acc:  0.9998095238095238\n",
      "test acc:  0.9694857142857143\n"
     ]
    }
   ],
   "source": [
    "## YOUR CODE HERE - call the constructor\n",
    "ranfor = RandomForestClassifier(n_estimators=150, min_samples_split=5, max_features='sqrt')\n",
    "## YOUR CODE HERE - fit the rf model (just like logistic regression)\n",
    "ranfor.fit(X_train, y_train)\n",
    "## YOUR CODE HERE - print training accuracy\n",
    "print('train acc: ', accuracy_score(ranfor.predict(X_train), y_train))\n",
    "## YOUR CODE HERE - print test accuracy\n",
    "print('test acc: ', accuracy_score(ranfor.predict(X_test), y_test))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "That train accuracy is amazing, let's see if we can boost up the test accuracy a bit (since that's what really counts). Try and play around with the hyperparameters to see if you can edge out more accuracy (look at the documentation for parameters in the constructor). Focus on `n_estimators`, `min_samples_split`, `max_features`. You should be able to hit ~97%."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### SVC"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "A support vector classifier is another completely different type of classifier. It tries to find the best separating hyperplane through your data."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The SVC will toast our laptops unless we reduce the data dimensionality. Let's keep 80% of the variation, and get rid of the rest. (This will cause a slight drop in performance, but not by much)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 49,
   "metadata": {},
   "outputs": [],
   "source": [
    "pca = PCA(n_components=0.8, whiten=True)\n",
    "X_train_pca = pca.fit_transform(X_train)\n",
    "X_test_pca = pca.transform(X_test)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Great! Now let's take a look at what that actually did."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 62,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(52500, 43)\n",
      "(17500, 43)\n",
      "(52500, 1)\n",
      "(17500, 1)\n"
     ]
    }
   ],
   "source": [
    "print(X_train_pca.shape)\n",
    "print(X_test_pca.shape)\n",
    "print(y_train.shape)\n",
    "print(y_test.shape)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Remember, before we had 784 (28x28) features! However, PCA found just 43 basis features that explain 80% of the data. So, we went to just 5% of the original input space, but we still retained 80% of the information! Nice."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "This [blog post](http://colah.github.io/posts/2014-10-Visualizing-MNIST/) explains dimensionality reduction with MNIST quite well. It's a short read (<10 mins), and it contains some pretty cool visualizations."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now let's train our first SVC. The LinearSVC can only find a linear decision boundary (the hyperplane)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 51,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\georg\\.mais-env\\lib\\site-packages\\sklearn\\utils\\validation.py:761: DataConversionWarning: A column-vector y was passed when a 1d array was expected. Please change the shape of y to (n_samples, ), for example using ravel().\n",
      "  y = column_or_1d(y, warn=True)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "train acc:  0.8939238095238096\n",
      "test acc:  0.8886285714285714\n"
     ]
    }
   ],
   "source": [
    "lsvc = LinearSVC(dual=False, tol=0.01)\n",
    "lsvc.fit(X_train_pca, y_train)\n",
    "print('train acc: ', accuracy_score(lsvc.predict(X_train_pca), y_train))\n",
    "print('test acc: ', accuracy_score(lsvc.predict(X_test_pca), y_test))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "SVMs are really interesting because they have something called the *dual formulation*, in which the computation is expressed as training point inner products. This means that data can be lifted into higher dimensions easily with this \"kernel trick\". Data that is not linearly separable in a lower dimension can be linearly separable in a higher dimension - which is why we conduct the transform. Let us experiment."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "A transformation that lifts the data into a higher-dimensional space is called a *kernel*. A polynomial kernel expands the feature space by computing all the polynomial cross terms to a specific degree."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Question 2) Poly SVC"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 55,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\georg\\.mais-env\\lib\\site-packages\\sklearn\\utils\\validation.py:761: DataConversionWarning: A column-vector y was passed when a 1d array was expected. Please change the shape of y to (n_samples, ), for example using ravel().\n",
      "  y = column_or_1d(y, warn=True)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "train acc:  0.9963047619047619\n",
      "test acc:  0.9801142857142857\n"
     ]
    }
   ],
   "source": [
    "psvc = SVC(kernel='poly', degree=3, tol=0.01, cache_size=4000)\n",
    "## YOUR CODE HERE - fit the psvc model\n",
    "psvc.fit(X_train_pca, y_train)\n",
    "## YOUR CODE HERE - print training accuracy\n",
    "print('train acc: ', accuracy_score(psvc.predict(X_train_pca), y_train))\n",
    "## YOUR CODE HERE - print test accuracy\n",
    "print('test acc: ', accuracy_score(psvc.predict(X_test_pca), y_test))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Play around with the degree of the polynomial kernel to see what accuracy you can get."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Question 3) RBF SVC"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The RBF kernel uses the gaussian function to create an infinite dimensional space - a gaussian peak at each datapoint. Now fiddle with the `C` and `gamma` parameters of the gaussian kernel below to see what you can get. [Here's documentation](http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 66,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\georg\\.mais-env\\lib\\site-packages\\sklearn\\utils\\validation.py:761: DataConversionWarning: A column-vector y was passed when a 1d array was expected. Please change the shape of y to (n_samples, ), for example using ravel().\n",
      "  y = column_or_1d(y, warn=True)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "train acc:  0.9932952380952381\n",
      "test acc:  0.9824\n"
     ]
    }
   ],
   "source": [
    "rsvc = SVC(kernel='rbf', tol=0.01, cache_size=4000)\n",
    "## YOUR CODE HERE - fit the rsvc model\n",
    "rsvc.fit(X_train_pca, y_train)\n",
    "## YOUR CODE HERE - print training accuracy\n",
    "print('train acc: ', accuracy_score(rsvc.predict(X_train_pca), y_train))\n",
    "## YOUR CODE HERE - print test accuracy\n",
    "print('test acc: ', accuracy_score(rsvc.predict(X_test_pca), y_test))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Isn't that just amazing accuracy?"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Basic Neural Network"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "You should never do neural networks in sklearn. Use Pytorch, Keras, etc. However, we will use sklearn for demonstrative purposes."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Basic neural networks proceed in layers. Each layer has a certain number of nodes, representing how expressive that layer can be. Below is a sample network, with an input layer, one hidden (middle) layer of 50 neurons, and finally the output layer."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Question 4) Neural Network"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 79,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\georg\\.mais-env\\lib\\site-packages\\sklearn\\neural_network\\multilayer_perceptron.py:916: DataConversionWarning: A column-vector y was passed when a 1d array was expected. Please change the shape of y to (n_samples, ), for example using ravel().\n",
      "  y = column_or_1d(y, warn=True)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Iteration 1, loss = 0.66195598\n",
      "Iteration 2, loss = 0.21324900\n",
      "Iteration 3, loss = 0.15016558\n",
      "Iteration 4, loss = 0.11713219\n",
      "Iteration 5, loss = 0.09590056\n",
      "Iteration 6, loss = 0.08135747\n",
      "Iteration 7, loss = 0.07013110\n",
      "Iteration 8, loss = 0.06129464\n",
      "Iteration 9, loss = 0.05414248\n",
      "Iteration 10, loss = 0.04803033\n",
      "Iteration 11, loss = 0.04311194\n",
      "Iteration 12, loss = 0.03883364\n",
      "Iteration 13, loss = 0.03509431\n",
      "Iteration 14, loss = 0.03183316\n",
      "Iteration 15, loss = 0.02893341\n",
      "Iteration 16, loss = 0.02622350\n",
      "Iteration 17, loss = 0.02409021\n",
      "Iteration 18, loss = 0.02205986\n",
      "Iteration 19, loss = 0.02000343\n",
      "Iteration 20, loss = 0.01823356\n",
      "Iteration 21, loss = 0.01639604\n",
      "Iteration 22, loss = 0.01506113\n",
      "Iteration 23, loss = 0.01377816\n",
      "Iteration 24, loss = 0.01268729\n",
      "Iteration 25, loss = 0.01152386\n",
      "Iteration 26, loss = 0.01049587\n",
      "Iteration 27, loss = 0.00960918\n",
      "Iteration 28, loss = 0.00890195\n",
      "Iteration 29, loss = 0.00808395\n",
      "Iteration 30, loss = 0.00735719\n",
      "Iteration 31, loss = 0.00675649\n",
      "Iteration 32, loss = 0.00615897\n",
      "Iteration 33, loss = 0.00561180\n",
      "Iteration 34, loss = 0.00498748\n",
      "Iteration 35, loss = 0.00479353\n",
      "Iteration 36, loss = 0.00443051\n",
      "Iteration 37, loss = 0.00386105\n",
      "Iteration 38, loss = 0.00348770\n",
      "Iteration 39, loss = 0.00335658\n",
      "Iteration 40, loss = 0.00308287\n",
      "Iteration 41, loss = 0.00285235\n",
      "Iteration 42, loss = 0.00270142\n",
      "Iteration 43, loss = 0.00256267\n",
      "Iteration 44, loss = 0.00224537\n",
      "Iteration 45, loss = 0.00204670\n",
      "Iteration 46, loss = 0.00188310\n",
      "Iteration 47, loss = 0.00176196\n",
      "Iteration 48, loss = 0.00167618\n",
      "Iteration 49, loss = 0.00158613\n",
      "Iteration 50, loss = 0.00155523\n",
      "Iteration 51, loss = 0.00141458\n",
      "Iteration 52, loss = 0.00130767\n",
      "Iteration 53, loss = 0.00128939\n",
      "Iteration 54, loss = 0.00127592\n",
      "Iteration 55, loss = 0.00225716\n",
      "Iteration 56, loss = 0.00575347\n",
      "Iteration 57, loss = 0.00233839\n",
      "Iteration 58, loss = 0.00108859\n",
      "Iteration 59, loss = 0.00090095\n",
      "Iteration 60, loss = 0.00084979\n",
      "Iteration 61, loss = 0.00081226\n",
      "Iteration 62, loss = 0.00078485\n",
      "Iteration 63, loss = 0.00075913\n",
      "Iteration 64, loss = 0.00074664\n",
      "Iteration 65, loss = 0.00073260\n",
      "Iteration 66, loss = 0.00070832\n",
      "Iteration 67, loss = 0.00069890\n",
      "Iteration 68, loss = 0.00068381\n",
      "Iteration 69, loss = 0.00067238\n",
      "Iteration 70, loss = 0.00066490\n",
      "Training loss did not improve more than tol=0.000100 for 10 consecutive epochs. Stopping.\n",
      "train acc:  1.0\n",
      "test acc:  0.9803428571428572\n"
     ]
    }
   ],
   "source": [
    "nn = MLPClassifier(hidden_layer_sizes=(255,), solver='adam', verbose=1)\n",
    "## YOUR CODE HERE - fit the nn\n",
    "nn.fit(X_train_pca, y_train)\n",
    "## YOUR CODE HERE - print training accuracy\n",
    "print('train acc: ', accuracy_score(nn.predict(X_train_pca), y_train))\n",
    "## YOUR CODE HERE - print test accuracy\n",
    "print('test acc: ', accuracy_score(nn.predict(X_test_pca), y_test))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Fiddle around with the hiddle layers. Change the number of neurons, add more layers, experiment. You should be able to hit 98% accuracy."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Neural networks are optimized with a technique called gradient descent (a neural net is just one big function - so we can take the gradient with respect to all its parameters, then just go opposite the gradient to try and find the minimum). This is why it requires many iterations to converge."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Turning In"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "1. Convert this notebook to a regular python file (file -> download as -> python)\n",
    "\n",
    "2. Submit both the notebook and python file via a pull request as specified in the README"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python (MAIS-202)",
   "language": "python",
   "name": ".mais-env"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.1"
  },
  "toc": {
   "base_numbering": 1,
   "nav_menu": {},
   "number_sections": false,
   "sideBar": false,
   "skip_h1_title": false,
   "title_cell": "Table of Contents",
   "title_sidebar": "Contents",
   "toc_cell": false,
   "toc_position": {},
   "toc_section_display": false,
   "toc_window_display": false
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
