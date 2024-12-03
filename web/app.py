import numpy as np
import pandas as pd
import streamlit as st
import requests
#from st_aggrid import AgGrid
from sqlalchemy import create_engine, func, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from datetime import datetime


st.set_page_config(layout="wide")

engine = create_engine('postgresql://admin:password@postgres_container_bis/job_market')
Session = sessionmaker(bind=engine)
session = Session()

# Reflect the existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

metadata_obj = MetaData()

job_table = Table("job_offers_tech", metadata_obj, autoload_with=engine)
columns = [c.name for c in job_table.columns]
st.write(columns)

# Assuming you have a table named 'your_table' and a column named 'your_column'
max_value = session.query(func.max(job_table.columns.date_creation)).scalar()

st.write(max_value)

# Convert datetime to string
#max_value_str = max_value.strftime("%Y-%m-%dT%H:%M:%S")
st.write(f"The maximum value in the column as string is: {max_value}")

if st.button("Get data from API"):
    response = requests.post("http://api:5000/collect", json={"begin_datetime": max_value})
    print(response)
    st.write(response.json())




session.close()