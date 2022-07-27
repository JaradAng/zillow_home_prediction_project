# from statistics import LinearRegression
from calendar import c
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler, QuantileTransformer
from sklearn.model_selection import train_test_split
import wrangle
import seaborn as sns
from sklearn.feature_selection import SelectKBest, RFE, f_regression, SequentialFeatureSelector
from sklearn.linear_model import LinearRegression, LassoLars, TweedieRegressor



# This is a function to plot the variable pairs with a rough fitting reggesion line to explore and determine what features to include in module
def variable_pairs_plot(df, columns):
    sns.pairplot(df[columns] , corner=True ,kind='reg', plot_kws={'line_kws':{'color':'red'}, 'scatter_kws':{'s': 1, 'alpha': 0.5}}) 



# This function is used to plot categorical and continuous variables to help the exploration process and see how each variable compares to each other
def plot_categorical_and_continuous_vars(df, cat_cols, cont_cols):
    #designated coloumns to explore in my notebook. this for loops cycles through both continuous and categorical variables
    for cont in cont_cols:
        for cat in cat_cols:
            #setting the chart size and titles
            fig = plt.figure(figsize= (20, 10))
            fig.suptitle(f'{cont} vs {cat}')
            
            # using a violin plot for the first graph
            plt.subplot(131)
            sns.violinplot(data=df, x = cat, y = cont)
           
            # makes a histogram for the third graph
            plt.subplot(1, 3, 3)
            sns.histplot(data = df, x = cont, bins = 50, hue = cat)
            
            #makes a bar chart for the second graph
            plt.subplot(1, 3, 2)
            sns.barplot(data = df, x = cat, y = cont)


def distribution_check(df, cat_cols, cont_cols):
    #designated coloumns to explore in my notebook. this for loops cycles through both continuous and categorical variables
    for cont in cont_cols:
        for cat in cat_cols:
            #setting the chart size and titles
            fig = plt.figure(figsize= (20, 10))
            fig.suptitle(f'{cont} vs {cat}')
            
         
           
            # makes a histogram for the second graph
            sns.histplot(data = df, x = cont, bins = 50, hue = cat)
            
            




# Function to help select the features to use in the model using recursive feature engineering
def select_rfe(x, y, k):
    model = LinearRegression()
    rfe = RFE(model, n_features_to_select= k)
    rfe.fit(x, y)
    return x.columns[rfe.get_support()]

# Function to help select best features to use in the model using select k best 
def select_kbest(x, y, k):
     kbest = SelectKBest(f_regression, k=k)
     kbest.fit(x , y)
     return x.columns[kbest.get_support()] 


# Function to plot my features against the target variable
def plot_against_home_vlaue(col1, col2, col3,col4, df):
    plt.figure(figsize=(15,10))

    plt.subplot(2,2,1)
    sns.regplot(x=col1, y="home_value", data=df, scatter_kws={"color": "black"}, line_kws={"color": "red"})

    plt.subplot(2,2,2)
    sns.regplot(x=col2, y="home_value", data=df, scatter_kws={"color": "black"}, line_kws={"color": "red"})

    plt.subplot(2,2,3)
    sns.barplot(x = col3, y='home_value', data = df, palette = 'Greys')
        
    plt.subplot(2,2,4)
    sns.regplot(x=col4, y="home_value", data=df, scatter_kws={"color": "black"}, line_kws={"color": "red"})

# Function to preform spearman test
def spearman_test(feat, df):
    corr, p = stats.spearmanr(df[feat], df.home_value)
    a= 0.05
    # print(p)
    if p < a:
        print("We reject the null hypothesis and this variable is statistically significant")
    else:
        print("We fail to reject the null hypothesis and this feature is not statisitcally significant")

#function to preform t test
def t_test(feat, df):
    t, p = stats.ttest_ind(df[feat],df.home_value, equal_var=False)
    t, p / 2
    a=0.05
    if p < a:
        print("We reject the null hypothesis and this variable is statistically significant")
    else:
        print("We fail to reject the null hypothesis and this feature is not statisitcally significant")