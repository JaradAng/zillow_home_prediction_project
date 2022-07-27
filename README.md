# Zillow Home Prediction Model

--- 

## Project Goal 

- The goal of this project is to create a reproducible  machine learning regression model to predict the ‘tax assed value’ of a single family home within three regions. 
- In order to achieve an accurate prediction, the project will identify key drivers of property values. This notebook serves as a way to understand why and how I made the prediction model.

---

## Project Description

- The residential real estate market accounts for $8.5 billion with a projected growth rate of 50% by the end of 2020's. However, the price of single family homes can vary drastically despite having the same size and features. Using the available Zillow data, this project will select key features such as bed/bath ratio and square footage try and accurately predict a homes value. 

---

### Key Questions

1. How does the house value relate the overall square foot? Is it better than the home's square footage

2. How does the house value reflected by the bed to bath ratio?

3. How does the house value reflect how many garages the house has?

4. How does having a pool affect house value?

5. to what extent does the age of the house affect house value? 

---

### How to Replicate the Results

- You will need an env.py file that contains the hostname, username and password of the mySQL database that contains the Zillow table. Store that env file locally in the repository.
- Clone my repo (including the wrangle.py, and exploration.py) (confirm .gitignore is hiding your env.py file)
- Libraries used are pandas, matplotlib, seaborn, numpy, sklearn.
- You should be able to run final_zillow_prediction

---

### The plan

1. Wrangle the data using the wrangle.py folder and performing a mySQL query to pull multiple tables to find the key drivers of price preditcions into the notebook.
    - The tables I pulled from mySQL are: properties_2017, predicitions_2017, and propertylandusetype
2. Additionally inside of the wrangle.py folder, I prepped, cleaned, and removed the outliers within the dataset to still include 99% of data entries. I also       featured engineered columns to help resolve multicollinearity. 
3. During the exploration phase in explore.ipynb, I visualize multiple features to asses which features to include in the model and to find if the features are statistically significant. Inside my explore notebook, I make multiple models and compare the results against each other to determine the final models to include within the final report.
4. Move and organize all important and useful features to a final notebook to deliver a streamlined product for stakeholders and management.  
5. Deliver a final report notebook with all required .py files

---

### Data Dictionary

Variable | Definiton | 
--- | --- | 
TaxAmount | The total property tax assessed for that year |
--- | --- | 
RegionCountyID | The county in which the property is located |
--- | --- | 
Fed_Code | Federal Information Processing Stardard code |
--- | --- | 
Bed_Bath_Ratio | The ratio of bedrooms to bathrooms the house has |
--- | --- | 
Home_Value | The target variable and how much the assesment value of the home  |
--- | --- | 
Sq_ft | The total sqaure footage of the house | 
--- | --- | 
Lot_Size | The size of the lot the house sits on |
--- | --- | 
Pool_Encoded | 1 - The property has a pool, 2 - The property does not have a pool |
--- | --- | 
House_Age | How old the house is in years |
--- | --- | 
Garages | The count of garage size in 'cars' |
--- | --- | 
Overall_Size | The overall property size ie: the lot square footage plus the house square footage |


---

### Exploring the Questions and Hypothesis


1. How does the house value relate the overall square foot? Is it better than the home's square footage
- Overall size does have a positive correlation with home value, however, I a wanted to see how it compared to the house's square footage. The overall size has more variance as we see with the line of best fit having a larger band. Although overall size is statistically significant, it does not have a better correlation than square feet. So I will use square feet in the model instead of overall size.

2. How is the house value reflected by the bed to bath ratio?
- We can confidently say the home price is affected by the bed_bath_ratio. There is a negative correlation to home value as the number of bedrooms increase against the number of bathrooms 
- Null Hypothesis: Home value is independent of the bed bath ratio. Alt Hypothesis: Home Value is dependent on the bed bath ratio. Result: We reject the null. 

3. How does the house value reflect how many garages the house has?
- There is a positive relationship with the increase in garages and the home value
- Null Hypothesis: Home value is independent of the amount of garages. Alt Hypothesis: Home value is dependent on the amount of garages. Result: We reject the null

4. How does having a pool affect house value?
- There is a positive correlation between having a pool and an increase in home value. If the pool has a pool the value should be higher
- Null Hypothesis: Home value is independent of the whether or not the house as pool. Alt: The home value is dependent on if the whether the house has a pool or not. Result: We reject the null.


5. to what extent does the age of the house affect house value? 
- As the house ages, the value of the home also decreases. There is a negative correlation between the house age and home value
- Null Hypothesis: Home value is independent of the age of house. Alt hypothesis: The home value is dependent on the age of the house. Result: We reject the null. 







---
## Overall Exploration and Testing Takeaways
---
* All features used for the questions proved to be statistically significant
* I will not be using overall size and instead stick to the finished square footage which has better correlation
* Two of the features have a negative correlation and those are bed bath ratio and house age
* Positive correlation features are the the square footage, pools, and garages
* ### The biggest takeaway is the amount of variance we see with all the features
--- 

# Summary
* The polynomial regression model used on the data beat the baseline prediction by almost 35,000
* The data has a lot of variance within it self causing for the large RMSE
* The top features to help predict the home value are: Square feet, Bed Bath Ratio, and House Age

---
# Recommendations
* Gain additional information from different states 
* Try to gain additional features about the house such as school district, if it was remolded, and appliance quality 
---
# Next Steps
* Try and break the data into groups in order to reduce variance
* Continue testing variables and feature engineering to gain better insight
* Proof of concecpt - can continue to build and work on the model. 