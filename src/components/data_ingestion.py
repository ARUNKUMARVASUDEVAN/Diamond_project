import os ##to create file path
import sys ##gives access to some variable in interpreter
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation

@dataclass

class DataIngestionconfig:
    train_data_path:str=os.path.join('artifacts','train.csv')
    test_data_path:str=os.path.join('artifacts','test.csv')
    raw_data_path:str=os.path.join('artifacts','raw.csv')

##create a class for Data Ingestion

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionconfig()
    
    def initiate_data_ingestion(self):
        logging.info('Data Ingestion methods starts')
        try:
            df=pd.read_csv('notebooks/gemstone.csv')
            logging.info('Dataset read as pandas DataFrame')
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False)
            logging.info('Train test split')
            train_set,test_set=train_test_split(df,test_size=0.30)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Data ingestion is completed")
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            logging.info("Exception occured in data Ingestion stage")
            raise CustomException(e,sys)



if __name__=='__main__':
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()
    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)
