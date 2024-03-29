import os
import pandas as pd
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from get_data import read_config
import numpy as np 
import joblib
import argparse
import json

def eval_metrices(actual,pred):
    rmse=np.sqrt(mean_squared_error(actual,pred))
    mae=mean_absolute_error(actual,pred)
    r2=r2_score(actual,pred)
    return rmse, mae,r2

def train_and_eval(config_path):
    config=read_config(config_path)
    test_data_path=config["split_data"]["test_path"]
    train_data_path=config["split_data"]["train_path"]
    random_state=config["base"]["randam_state"]
    model_dir=config["model_dir"]

    alpha=config["estimater"]["ElasticNet"]["params"]["alpha"]
    l1_ratio=config["estimater"]["ElasticNet"]["params"]["l1_ratio"]

    target=config["base"]["target_col"]

    train=pd.read_csv(train_data_path)
    test=pd.read_csv(test_data_path)

    train_x=train.drop(target,axis=1)
    test_x=test.drop(target,axis=1)

    train_y=train[target]
    test_y=test[target]


    lr=ElasticNet(alpha=alpha,l1_ratio=l1_ratio,random_state=random_state)

    lr.fit(train_x,train_y)
    pred=lr.predict(test_x)
    (rmse,mae,r2)=eval_metrices(test_y,pred)
    print("ElasticNet model (alpha=%f,l1_ratio=%f):" % (alpha,l1_ratio))
    print("Rmse: %s" %rmse)
    print("Mae: %s" %mae)
    print("R2: %s" %r2)

    ####
    score_file=config["reports"]["scores"]
    params_file=config["reports"]["params"]

    with open(score_file,"w") as f:
        score={
            "rmse": rmse,
            "mae":mae,
            "r2": r2
        }
        json.dump(score, f, indent=4)
    with open(params_file,"w")as p:
        param={
            "alpha":alpha,
            "l1_ratio":l1_ratio
        }
        json.dump(param,p,indent=4)
    ########
    os.makedirs(model_dir,exist_ok=True)
    model_path=os.path.join(model_dir,"model.joblib")
    joblib.dump(lr,model_path)

if __name__=="__main__":
    args=argparse.ArgumentParser() 
    args.add_argument("--config", default="params.yaml")
    parsed_args=args.parse_args()
    train_and_eval(config_path=parsed_args.config)