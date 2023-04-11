import pandas as pd
import streamlit as st

import altair as alt
import duckdb

con = duckdb.connect(database='Job.db', read_only=True) 

# Countries
query="""
   SELECT * 
   FROM job
"""
Countries=list(con.execute(query).df().columns)[2:]


st.subheader('Investingation')

col1, col2 = st.columns(2)

with col1:
    query="""
            SELECT 
                 DISTINCT variable
            From job        
            ORDER BY variable       
          """

    kinds=con.execute(query).df()
    kind = st.selectbox('Kind of Statistics',kinds)
with col2: 
    country = st.multiselect('Country',Countries)


result_df = con.execute("""
    SELECT 
        *
    FROM Job 
    WHERE variable=?
    """, [kind]).df()

#chart = alt.Chart(result_df).mark_circle().encode(
#    x = 'date',
#    y = country,
#    #color = 'carrier'
#).interactive()
#st.altair_chart(chart, theme="streamlit", use_container_width=True)

# Create a new DataFrame containing only the selected countries
selected_data = result_df[['date'] + country]

# Melt the DataFrame to create a "long" format for plotting
melted_data = pd.melt(selected_data, id_vars=['date'], var_name='country', value_name='value')

# Plot the chart using the melted DataFrame
chart = alt.Chart(melted_data).mark_circle().encode(
    x = 'date',
    y = 'value',
    color = 'country'
).interactive()

st.altair_chart(chart, theme="streamlit", use_container_width=True)