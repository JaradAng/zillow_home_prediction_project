import pandas as pd
import numpy as np
import os
from env import get_db_url

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, RobustScaler

def zillow_data():
    filename = 'zillow2.csv'

    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        zillow_df = pd.read_sql('''select bedroomcnt, 
                                        bathroomcnt,
                                         calculatedfinishedsquarefeet,
                                          taxvaluedollarcnt,
                                           yearbuilt,
                                            
                                             fips,
                                               lotsizesquarefeet,
                                                 poolcnt,
                                                  regionidcounty,
                                                   garagecarcnt
                                              from properties_2017
                                              join propertylandusetype as plut using (propertylandusetypeid) 
                                              join predictions_2017 using (parcelid)
                                              where plut.propertylandusedesc in ("Single Family Residential" , "Inferred Single Family Residential")
                                              and transactiondate like "2017%%";''', get_db_url('zillow'))
        zillow_df.to_csv(filename)

        return zillow_df


def clean_zillow(df):

    #Making pools boolean despite the amount of nulls, if a house has a pool it will be listed in the features becuase it is a high ticket item
    df['poolcnt'] = np.where((df['poolcnt'] == 1.0) , True , False)
    
    # Assigning the value of the car garage to the dataset if its above 1 and making the nulls to 0 doing this because garages are important enough to list and there are as many nulls with garage sq
    df['garagecarcnt'] = np.where((df['garagecarcnt'] >= 1.0) , df['garagecarcnt'] , 0)  


    #Drop the columns with null values because they only make up about 0.5% and would have less impact on model than imputing value
    df = df.dropna()
    
    # Rename Columns and assigning data type if needed
    df["fed_code"] = df["fips"].astype(int)
    df["year_built"] = df["yearbuilt"].astype(int)
    df["beds"] = df["bedroomcnt"].astype(int)    
    df["home_value"] = df["taxvaluedollarcnt"].astype(float)
    df["sq_ft"] = df["calculatedfinishedsquarefeet"].astype(float)
    df["baths"] = df["bathroomcnt"]
    df["lot_size"] = df["lotsizesquarefeet"]
    df["pools"] = df["poolcnt"]
    df["garages"] = df["garagecarcnt"]

    return df
  
def feature_engineering(df):
    #Feature engineering new variables to combat multicolinearty and test to see if new features help the model

    df['pool_encoded'] = df.pools.map({True:1, False:0})
  
    # Leaving in the two original columns and seeing if the overall sq ft might make a difference
    df['overall_size'] = df['sq_ft'] + df['lot_size']
    #dropping year built and turning it into house age which will then be scaled
    df['house_age'] = 2017 - df['year_built']
    
    # Making sure the house includes a bathroom
    df =df[df.baths > 0]

    # Making sure the house include a bedroom
    df =df[df.beds > 0]

    df['bed_bath_ratio'] = df['beds'] / df['baths']

    # Making sure the house include a bedroom
    df =df[df.home_value < 1_000_000]

    # making dummies and encoded values to help machine learning
    # dummy_df = pd.get_dummies(df[['garages']], dummy_na=False,drop_first=False)

    # df = pd.concat([df, dummy_df], axis=1)


    #Deleting duplicate rows
    df = df.drop(columns=['fips', 'yearbuilt', 'bedroomcnt', 'taxvaluedollarcnt', 'calculatedfinishedsquarefeet', 'bathroomcnt', 'poolcnt', 'lotsizesquarefeet', 'year_built', 'garagecarcnt'])
    
    return df







# def categorize_houses(df):
#     """Manually handle outliers that do not represent properties likely for 99% of buyers and zillow visitors"""
#     low_df = df[(df.baths <= 2) & (df.beds <=2) & (df.sq_ft <= 2_000) & (df.garages == 0) & (df.home_value <= 500_000)]

#     medium_df = df[(df.baths <= 4) & (df.beds <=5) & (df.sq_ft > 2_000) & (df.garages <= 3) & (df.home_value <= 1_000_000)]

#     high_df = df[(df.baths > 4) & (df.beds > 5) & (df.sq_ft > 7_000) & (df.garages > 3) & (df.home_value > 1_000_000)] 


    

#     return low_df, medium_df, high_df


def categorize_houses(df):
    """Manually handle outliers that do not represent properties likely for 99% of buyers and zillow visitors"""
    small_df = df[df.sq_ft <= 1_325]

    medium_df = df[(df.sq_ft > 1_325) & (df.sq_ft <= 2_250)]

    large_df = df[df.sq_ft > 2_250]


    

    return small_df, medium_df, large_df


def wrangle_zillow():

    df = zillow_data()

    df = clean_zillow(df)

 

    df = feature_engineering(df)

    df = categorize_houses(df)

    #df.to_csv("zillow.csv", index=False)

    return df

# split the data before fitting scalers 
def split_zillow(df):

    # split the data
    train_validate, test = train_test_split(df, test_size=.2, 
                                            random_state=123)
    train, validate = train_test_split(train_validate, test_size=.2, 
                                       random_state=123)
    return train, validate, test    

# cols_to_scale = ['sq_ft', 'overall_size', 'house_age', 'garages', 'lot_size']

def MinMax_scaler(x_train, x_validate, x_test):
 
    scaler = MinMaxScaler().fit(x_train)

    scaler.fit(x_train)
    
    x_train_scaled = pd.DataFrame(scaler.transform(x_train), index=x_train.index, columns=x_train.columns)
    x_validate_scaled = pd.DataFrame(scaler.transform(x_validate), index=x_validate.index, columns=x_validate.columns)
    x_test_scaled = pd.DataFrame(scaler.transform(x_test), index=x_test.index, columns = x_test.columns)
    
    return x_train_scaled, x_validate_scaled, x_test_scaled


def scale_data(train, validate, test):
    
    scale_columns = ['bedrooms', 'bathrooms', 'sq_ft']
    
    train_scaled = train.copy()
    validate_scaled = validate.copy()
    test_scaled = test.copy()
    
    mms = RobustScaler()
    
    mms.fit(train[scale_columns])
    
    train_scaled[scale_columns] = mms.transform(train[scale_columns])
    validate_scaled[scale_columns] = mms.transform(validate[scale_columns])
    test_scaled[scale_columns] = mms.transform(test[scale_columns])
    
    return train_scaled, validate_scaled, test_scaled
    
