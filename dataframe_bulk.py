pip install elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import connections
import pandas as pd

#initialize the listof lists
data =[['tom',15,'NY'],['Nick',34,'YN'],['Ram',16,'IND'],['Sam',23,'AUS']]

df =pd.DataFrame(data,columns=['Name','Age','Country'])
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es_client =Elasticsearch(timeout=600, hosts="http://localhost:9200/",basic_auth=("elastic","XX0gNxxm4YFOnd2JlDgq"))


es_client.ping()

#Define maing structure based on Dataframe colums and their data types
def create_index_maping_from_dataframe(df,index_name):
    mapping={
        "mappings":{
            "properties":{}
        }
    }
    for column,dtype in df.dtypes.items():
        if dtype=='str':
            mapping['mappings']['properties'][column]={"type":"text"}
        elif dtype =='int':
             mapping['mappings']['properties'][column]={"type":"integer"}
            
    #create the index with the defined mapping
    response = es_client.indices.create(index=index_name , body =mapping)

    if response["acknowledged"]:
        print("success")

    else:
        print(f"Failed to create index '{index_name}'.")



def bulk_uload_dataframe(df,index_name):
    #convert Dataframe to a list of dictionaries
    data_to_index =df.to_dict(orient='records')
    #bulk index the data into elasticsearch
    success,failed = bulk(es_client , index_data(data_to_index,index_name))
    print(f"success indexed :{success}")
    print(f"failure indexed :{failed}")

def index_data(data,index_name):
    
    for doc in data:
        yield{
            "_index": index_name,
            "_source":doc
        }

index_name ="test2_dataframe"

#create index maping
create_index_maping_from_dataframe(df,index_name)
#upload dataframe to elasticsearch
bulk_uload_dataframe(df,index_name)

from elasticsearch_dsl import Search
s =Search(index="test2_dataframe").query("match",Name="Ram")

def search_documents(index_name,query):
    search_query={
        "query":{"match_all":{}
                }
    }
    if query:
        search_query={
            "query":{"match":{"Name":query}
                    }
        }

    response =es_client.search(index=index_name,body=search_query)
    a= response['hits']['hits']
    return a

         

query ="Ram"


search_documents(index_name,query)
