#!/usr/bin/env python
# coding: utf-8

# # Assignment 2

# In this assignment, we will start with utilizing Sci-Kit learn to implement a linear regression model similar to what we did in Assignment 1. Afterwards, we will be dropping Sci-Kit learning and implementing these algorithms from scratch without the use of machine learning libraries. While you would likely never have to implement your own linear regression algorithm from scratch in practice, such a skill is valuable to have as you progress further into the field and find many scenarios where you actually may need to perform such implementations manually. Additionally, implementing algorithms from scratch will help you better understand the underlying mathematics behind each model.     

# ## Import Libraries

# We will be using the following libraries for this homework assignment. For the questions requiring manual implementation, the pre-existing implementations from Sci-Kit Learn should *not* be used.

# In[82]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import operator
get_ipython().run_line_magic('matplotlib', 'inline')

from sklearn.linear_model import LinearRegression as lr
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
from numpy.linalg import inv


# ## Preparing Data

# The file named **dataset1.csv** includes data that was generated from an n-degree polynomial with some gaussian noise. The data has 2 columns - first column is the feature (input) and the second column is its label (output). The first step is to load the data and split them into training, validation, and test sets. A reminder that the purpose of each of the splitted sets are as follows:
# 
# * **Training Set**: The sample of data used to fit the model
# * **Validation Set**: The sample of data used to provide an unbiased evaluation of a model fit on the training dataset while tuning model hyperparameters.
# * **Test Set**: The sample of data used to provide an unbiased evaluation of a final model fit on the training dataset.
# 
# In the section below, we load the csv file and split the data randomnly into 3 equal sets. 
# 
# *Note that in practice, we usually aim for around a 70-20-10 split for train, valid, and test respectively, but due to limited data in our case, we will do an even split in order to have sufficient data for evaluation* 

# In[12]:


# Load the data and split into 3 equal sets
data = pd.read_csv('dataset1.csv', header=None)
print(data.head())
data = data.iloc[:, :-1]
print(data.head())
train, valid, test = np.split(data, [int(.33*len(data)), int(.66*len(data))])


# We sort the data in order for plotting purposes later
train.sort_values(by=[0], inplace=True)
print(train)
valid.sort_values(by=[0], inplace=True)
test.sort_values(by=[0], inplace=True)


# Let's take a look at what our data looks like

# In[4]:


plt.scatter(train[0], train[1], s=10)
plt.show()


# Let's apply a linear regression model using Sci-Kit learn and see what the results look like.

# In[17]:


# Reshape arrays since sci-kit learn only takes in 2D arrays
train_x = np.array(train[0])
print(train_x.shape)
train_y = np.array(train[1])
valid_x = np.array(valid[0])
valid_y = np.array(valid[1])
train_x = train_x.reshape(-1, 1)
print(train_x.shape)
train_y = train_y.reshape(-1, 1)
valid_x = valid_x.reshape(-1, 1)
valid_y = valid_y.reshape(-1, 1)

# Apply linear regression model
model = lr()
model.fit(train_x, train_y)
y_pred = model.predict(train_x)

# Plot the results
plt.scatter(train_x, train_y, s=10)
plt.plot(train_x, y_pred, color='r')
plt.show()


# By analyzing the line of best fit above, we can see that a straight line is unable to capture the patterns of the data. This is an example of underfitting. As seen in the latest lecture, we can generate a higher order equation by adding powers of the original features as new features. 
# 
# The linear model,: 
# 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ** $y(x)$ = $w_1 x$ + $w_0$ ** 
# 
# can be transformed to a polynomial model such as:
# 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ** $y(x)$ = $w_2 x^2$ + $w_1 x$ + $w_0$ ** 
# 
# Note that this is still considered to be linear model as the coefficients/weights associated with the features are still linear. x<sup>2</sup> is only a feature. However the curve that we would be fitting in this case is quadratic in nature.
# 
# Below we show an example of a quadratic curve being fit to the data

# In[20]:


# Create polynomial features with degree 2
polynomial_features = PolynomialFeatures(degree=2)
x_poly = polynomial_features.fit_transform(train_x)

# Apply linear regression
model = lr()
model.fit(x_poly, train_y)
y_poly_pred = model.predict(x_poly)

# Plot the results
plt.scatter(train_x, train_y, s=10)
plt.plot(train_x, y_poly_pred, color='r')
plt.show()


# As you can see, we get a slightly better fit with a quadratic curve. Let's use the model to make predictions on our validation set and compute the mean squared error, which is the error which we wish to minimize.

# In[19]:


# Make predictions using pretrained model
valid_y_poly_pred = model.predict(polynomial_features.fit_transform(valid_x))

# Calculate root mean squared error
mse = mean_squared_error(valid_y, valid_y_poly_pred)
print("Mean Squared Error: {}".format(mse))

# Plot the prediction results
plt.scatter(valid_x, valid_y, s=10)
plt.plot(valid_x, valid_y_poly_pred, color='r')
plt.show()


# ## Question 1: Polynomial Regression Using Sci-Kit Learn
# 
# Now it is your turn! Following the same format as above, implement a 10-degree polynomial regression model on the training data and plot your results. Use your model to predict the output of the validation set and calculate the mean square error. Report and plot the results. 

# In[107]:


def fit_and_plot():
    x_poly = polynomial_features.fit_transform(train_x)
    model = lr()
    model.fit(x_poly, train_y)

    ### YOUR CODE HERE - Plot your the curve on the training data set
    plt.scatter(train_x, train_y, s=10)
    plt.plot(train_x, model.predict(x_poly), color='r')

    ### YOUR CODE HERE - Use model to predict output of validation set
    valid_y_model = model.predict(polynomial_features.fit_transform(valid_x))

    ### YOUR CODE HERE - Calculate the RMSE. Report and plot the curve on the validation set.
    mse = mean_squared_error(valid_y, valid_y_model)
    print("Mean Squared Error: {}".format(mse))

### YOUR CODE HERE - Fit a 10-degree polynomial using Sci-Kit Learn
polynomial_features = PolynomialFeatures(degree=10)
#polynomial_features.degree = 13
fit_and_plot()


# #### Did the root mean squared error go up or down as compared to the 2-degree polynomial curve? Why do you think this is the case?
# Down. It is probably a better fit to represent the data. Also as we increase the number the polynomial degree we get a more complex/accurate fit until we hit a point where we start overfitting. For example increasing degree to 13 will give a worse value.

# Now repeat the above for a 20-degree polynomial regression model.

# In[31]:


polynomial_features.degree = 20
fit_and_plot()


# #### How does the mean square error compare to the previous two models? Why do you think this is the case?
# 
# Like explained above we are overfitting the data such that our validation error is increasing.

# ## Question 2: Manual Implementation

# Now it's time to appreciate the hard work that open source developers have put, in order to allow you to implemenent machine learning models without doing any math! No more Sci-Kit learn (or any other libraries like Tensorflow, Pytorch, etc) for the rest of this assignment!

# Your first step is to fit a **10-degree polynomial** to the dataset we have been using above. Then using your results, calculate the mean squared error on both the training and validation set. You may use general utility libraries like numpy and pandas matrix computations and data manipulation, but pre-existing implementations of the model itself is prohibited.
# 
# A reminder that in polynomial regression, we are looking for a solution for the equation:
# 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ** $Y(X)$ = $W^T$ * $\phi(X)$ ** 
# 
# where
# 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ** $\phi(X)$ = [ $1$, $X$, $X^2$, $X^3$, ..... $X^n$ ] **
#  
# and the ordinary least square solution in closed form is:
# 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;** $W$ = $(X^T X)^{-1}X^TY$ **
# 
# Make sure to review the slides, do some research, and/or ask for clarification if this doesn't make sense. You must understand the underlying math before being able to implement this properly.
# 
# *Suggestion - Use the original pandas dataframes variables named train, valid, and test instead of the reshaped arrays that were used specifically for Sci-Kit Learn. It will make your computations cleaner and more inuitive.*

# In[110]:


### YOUR CODE HERE - Create the polynomial matrix ϕ(X)
def poly_transform(x_val, degree):
    x_transform= np.matrix(([np.array(x_val)**i for i in range(0, degree+1)])).T
    return x_transform

def mean_square_err(y1, y2):
    return sum(np.array(y1 - y2)**2)/len(y1)

x_transform = poly_transform(train[0], degree=10)

### YOUR CODE HERE - Find the weighted matrix W
W = np.matmul(np.matmul(inv(np.matmul(x_transform.T, x_transform)), x_transform.T), train_y)
y_pred_train = np.matmul(x_transform, W)

### YOUR CODE HERE - Make predictions on the training set and calculate the root mean squared error. Plot the results.
plt.scatter(train_x, train_y, s=10)
plt.plot(train_x, y_pred_train, color='r')
print(mean_square_err(y_pred_train, train_y))

### YOUR CODE HERE - Make predictions on the validation set and calculate the mean squared error. Plot the results.
x_transform = poly_transform(valid[0], degree=10)
y_pred_valid = np.matmul(x_transform, W)
plt.scatter(valid_x, valid_y, s=10)
plt.plot(valid_x, y_pred_valid, color='b')
print(mean_square_err(y_pred_valid, valid_y))


# For the rest of the assignment, we will use the other dataset named **dataset2.csv**. First load the csv and split the model into train, valid, and test sets as shown earlier in the assignment.

# In[160]:


### YOUR CODE HERE - Load dataset2.csv and split into 3 equal sets
data2 = pd.read_csv('dataset2.csv', header=None)
print(data2.head())
data2 = data2.iloc[:, :-1]
print(data2.head())

### YOUR CODE HERE - Sort the data in order for plotting purposes later
# copied from above *** using same split ratios
data2.sort_values(by=[0], inplace=True)
train_x = data2.iloc[:, 0]
train_y = data2.iloc[:, 1]

# to get a general sense of mse 
model = lr()
model.fit(np.array(train_x).reshape(-1, 1), np.array(train_y).reshape(-1, 1))
y_pred = model.predict(np.array(train_x).reshape(-1, 1))
mse = mean_squared_error(np.array(train_y).reshape(-1, 1), y_pred)
print("Mean Squared Error: {}".format(mse))


# Plot the data below to see what it looks like

# In[161]:


### YOUR CODE HERE - Plot the points for dataset2
plt.scatter(train_x, train_y)


# If done properly, you should see that the points fall under a relatively straight line with minor deviations. Looks like a perfect example to implement a linear regression model using the **gradient descent** method ..... without the use of any machine learning libraries!
# 
# Since the data falls along a straight line, we can assume the solution follows the form:
# 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ** $y(x)$ = $m x$ + $b$ **
# 
# A reminder that in gradient descent, we essentially want to iteratively get closer to the minimum of our objective function (the mean squared error), such that:
#  
#  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ** MSE($w_0$) > MSE($w_1$) > MSE($w_2$) > ...**
# 
# The algorithm is as follows:
# 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ** 1) Pick initial $w_0$ randomnly. **
# 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ** 2) For $k=1,2..$ $\Rightarrow$ $w_{k+1}$ = $w_k$ - $\alpha$  $g(w_k)$  where $\alpha > 0$ is the learning rate and $g(w_k)$ is the gradient. **
# 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ** End when | $w_k$ + $1$ - $w_k$ | < $\epsilon$ **
# 
# 
# Make sure to review the slides, do some research, and/or ask for clarification if this doesn't make sense. There are many resources online for gradient descent. You must understand the underlying math before being able to implement this properly.
# 
# Now once you understand, it is time to implement the gradient descent below. You may set the learning rate to 1e-6 or whatever value you think is best. As usual, calculate the mean squared error and plot your results. This time, training should be done using the training and validation sets, while the final mean squared error should be computed using the testing set.

# In[164]:


### YOUR CODE HERE - Implement gradient decent
# y = mx + b
# E (error) = 1/N * sum([y - (mx+b)]^2) --> cost funtcion
# dE/dm = 2/N * -x*(y - (mx+b)) ~ 1/N * sum([-x*y + m*x^2 +b*x])
# dE/db = 2/N * -(y - (mx+b)) ~ 1/N *sum([-y + mx + b])
def lin_reg_gradient(x, y, m, b):
    x = np.array(x)
    y = np.array(y)
    dE_dm = (1/len(x))*sum(-1*x*y+m*x**2+b*x)
    dE_db = (1/len(x))*sum(-1*y+m*x+b)
    return (dE_dm, dE_db)

def dist_to_origin(x):
    return sum(np.array(x)**2)


error = 0.0000001
alpha = 0.01
m = 0
b = 0
grad = lin_reg_gradient(train_x, train_y, m, b)
current_error = dist_to_origin(list(grad))
while(current_error > error):
    m = m - alpha*grad[0]
    b = b - alpha*grad[1]
    grad = lin_reg_gradient(train_x, train_y, m, b)
    current_error = dist_to_origin(list(grad))

### YOUR CODE HERE - Calculate the the mean squared error and plot the results.
plt.scatter(train_x, train_y)
y_pred = m*np.array(train_x)+b
plt.plot(train_x, y_pred, 'r')
mse = mean_squared_error(train_y, y_pred)
print("Mean Squared Error: {}".format(mse))


# ## Turning In

# 1. Convert this notebook to a regular python file (file -> download as -> python)
# 
# 2. Submit both the notebook and python file via a pull request as specified in the README
