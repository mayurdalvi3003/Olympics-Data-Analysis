import pandas as pd



def preprocess(df , region_df):
    # filtering for the summer olympics 
    df = df[df['Season'] =="Summer"]
    # merge with the region_df
    df = df.merge(region_df , on = "NOC" ,how = "left")

    # droping duplicates 
    df.drop_duplicates(inplace= True)

    # one hot encoding on medals 
    df = pd.concat([df  ,pd.get_dummies(df["Medal"])], axis = 1)
    return df 