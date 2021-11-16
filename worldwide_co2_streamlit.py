import streamlit as st
import pandas as pd
import altair as alt

st.write("""
### Worldwide CO2 Emissions
Feel free to click on the chart and the filters!
""")

#Upload data
def load_data(dataset):
    data = pd.read_csv(dataset)
    return data

co_df = load_data('owid-co2-data.csv')
#st.write(co_df)

#Deal with Nulls
co_df['co2'] = co_df['co2'].fillna(0)
co_df['consumption_co2'] = co_df['consumption_co2'].fillna(0)
co_df = co_df.dropna(subset=['iso_code', 'country'])

#Create Worldwide Filter
co_df['Filter Worldwide'] = ['Worldwide View' if list(co_df['country'])[i] == 'World' else 'Country View' for i in range(len(co_df))]


#Filtering to years divisible by 5 and after 1900 for less granular data
year_div_5s = co_df[co_df['year']%5 == 0]
years_19s = year_div_5s[year_div_5s['year'] >= 1900]

#Filter by top 10 co2 producting/consuming countries
top_co2_countries = list(co_df.groupby('country').sum().sort_values('co2', ascending = False).head(11).index)

#Define dataset to use
top_co2_countries_data = years_19s[years_19s['country'].isin(top_co2_countries)]


#FINAL GRAPH
#Production-based CO2 Interactive Graph

#COLOR ASSIGNMENTS
domain = ['United States', 'China', 'Russia', 'India','Japan', 'Germany','Canada', 'United Kingdom','France','Ukraine', 'World']
range_ = [ '#4EB550','#FFAF64', '#FCEA73', '#A3EC77', '#73B3FC','#FF6B6B',  '#73F1FC', '#FFB0D8','#345cfa', '#B273FC','#5E3499']

#COLOR FILTER
color_filter_dropdown = alt.binding_select(options=list(top_co2_countries_data['country'].unique()))
color_filter_select = alt.selection_single(fields=['country'], bind=color_filter_dropdown, name="__Filter")
color = alt.condition(color_filter_select,
                    alt.Color('country:N', legend=None, scale=alt.Scale(domain=domain, range=range_)),
                    alt.value('lightgray'))

#Worldwide Filter
worldwide_dropdown = alt.binding_select(options=['Worldwide View', 'Country View'])
selection = alt.selection_single(fields=['Filter Worldwide'], bind=worldwide_dropdown, name= ' ')

#Plot Chart
def plot_chart(top_co2_countries_data):
    co2_chart = alt.Chart(top_co2_countries_data, title = 'CO2 Production-Based Emissions from Top 10 Countries Worldwide').mark_line().encode(
        x=alt.X('year:O', title = 'Year'),
        y=alt.Y('co2:Q', title = 'CO2 Emissions (mil tonnes)'),
        color=color,
        tooltip=['iso_code', 'country', 'co2']
    ).add_selection(color_filter_select
    ).add_selection(selection
    ).transform_filter(selection
    ).properties(
        width=600,
        height=700)
    return co2_chart

st.write(plot_chart(top_co2_countries_data))
