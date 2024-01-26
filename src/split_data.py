import os
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from get_data import read_config

def split_and_save(config_path):
    config = read_config(config_path)
    test_data_path=config["split_data"]["test_path"]
    train_data_path=config["split_data"]["train_path"]
    raw_data_path=config["load_data"]["raw_dataset"]
    split_ratio=config["split_data"]["test_size"]
    random_state=config["base"]["randam_state"]

    df=pd.read_csv(raw_data_path)
    train, test=train_test_split(df,train_size=split_ratio,random_state=random_state)

    train.to_csv(train_data_path, sep=",", index=False)
    test.to_csv(test_data_path,sep=",",index=False)

if __name__=="__main__":
    args=argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args=args.parse_args()
    split_and_save(config_path=parsed_args.config)
    
