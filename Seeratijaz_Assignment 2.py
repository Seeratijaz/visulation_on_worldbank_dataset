import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib.ticker import MaxNLocator

def lineplot(x, y, xlabel, ylabel, title, labels):
    """ Funtion to Create Lineplot. Arguments:
        list of values for xaxis
        list of values for yaxis
        xlabel, ylabel and titel value
        color name
        label value
    """
    plt.style.use('tableau-colorblind10')
    plt.figure(figsize=(7, 5))
    for index in range(len(y)):
        plt.plot(x, y[index], label=labels[index])
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=6))
    plt.xticks(rotation=90)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.savefig('Line_plot.jpg', dpi=500)
    plt.show()
    return


def bar_plot(dataframe,xlabel,ylabel,title):
    dataframe.plot(kind='bar', figsize=(10, 6))
    # Set plot labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig('Bar_plot.jpg', dpi=500)
    plt.show()


def data_for_countries(dataframe,countries,Year_to_start,Year_to_end):
    dataframe = dataframe.T
    dataframe = dataframe.drop(['Country Code','Indicator Name','Indicator Code'])
    dataframe.columns = dataframe.iloc[0]
    dataframe = dataframe.drop(['Country Name'])
    dataframe= dataframe.reset_index()
    dataframe['Years']= dataframe['index']
    dataframe = dataframe.drop('index',axis=1)
    dataframe= dataframe[(dataframe['Years']>=Year_to_start)&(dataframe['Years']<=Year_to_end)]
    selected_data = dataframe[countries]
    selected_data = selected_data.fillna(selected_data.iloc[:,:-1].mean())
    return selected_data

def make_corr_heat_map(df,title,cmap='viridis'):

    # Calculate the correlation matrix
    correlation_matrix = df.corr()

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(8, 6))

    # Create a heatmap using Matplotlib's pcolormesh, focusing on positive correlations
    heatmap = ax.pcolormesh(correlation_matrix, cmap=cmap)

    # Add colorbar
    cbar = plt.colorbar(heatmap)
    for i in range(len(correlation_matrix.columns)):
        for j in range(len(correlation_matrix.columns)):
            ax.text(j + 0.5, i + 0.5, f'{correlation_matrix.iloc[i, j]:.2f}',
                    ha='center', va='center', color='white')

    # Set axis labels and title
    ax.set_xticks(range(len(correlation_matrix.columns)))
    ax.set_yticks(range(len(correlation_matrix.columns)))
    ax.set_xticklabels(correlation_matrix.columns, rotation=90)
    ax.set_yticklabels(correlation_matrix.columns)
    plt.title(title)
    plt.savefig('Heatmap_plot.jpg', dpi=500)
    # Display the plot
    plt.show()


def get_data_for_specific_country(data_frames,country_name,names,start_year,end_year):
    country_data = []
    for i, data in enumerate(data_frames):
        data = data_for_countries(data,country_name,start_year,end_year)
        data = data.rename(columns={country_name[0]:names[i]})
        country_data.append(data)
    country_data = pd.concat(country_data, axis= 1)
    country_data = country_data.T.drop_duplicates().T
    country_data = country_data.drop('Years',axis=1)
    return country_data


def convert_to_lists(df,cols):
    column_lists = [df[col].tolist() for col in cols[:-1]]
    return column_lists


def get_data_for_bar(df,years):
    df = df[df['Years'].isin(years)]
    df = df.set_index('Years')
    return df

CO2_emission_ = pd.read_csv('CO2_emissions.csv', skiprows=4)
GDP_Data_ = pd.read_csv('GDP_of_Agriculture_forestry_and_fishing_value_added.csv', skiprows=4)
Population_growth_ = pd.read_csv('Population_growth.csv', skiprows=4)
Arable_land = pd.read_csv('Arable_land.csv', skiprows=4)
Agricultural_irrigated_land = pd.read_csv('Agricultural_irrigated_land.csv', skiprows=4)
Electric_power_consumption = pd.read_csv('Electric_power_consumption.csv', skiprows=4)
Nitrous_oxide_emissions = pd.read_csv('Nitrous_oxide_emissions.csv', skiprows=4)
cols = ['Pakistan','India','Sri Lanka','Maldives','Bangladesh','Bhutan','Nepal','Afghanistan','Years']
start_year = '1970'
end_year   = '2021'
lineplot(list(data_for_countries(Arable_land, cols, start_year, end_year)['Years']),convert_to_lists(data_for_countries(Arable_land, cols, start_year, end_year),cols), 'Years', 'Arable land Percentage', 'Arable land Percentage comparision in South Asia', cols[:-1])
lineplot(list(data_for_countries(Population_growth_, cols, start_year, end_year)['Years']),convert_to_lists(data_for_countries(Population_growth_, cols, start_year, end_year),cols), 'Years', 'Population Growth Rate', 'Population Growth Rate comparision in South Asia', cols[:-1])
years = ['2012','2014','2016','2018']
bar_plot(get_data_for_bar(data_for_countries(Nitrous_oxide_emissions,cols,start_year, end_year),years),'Years','Nitrous oxide emissions (thousand metric tons of CO2 equivalent)','Nitrous oxide emissions Comparision of South Asian Countries')
bar_plot(get_data_for_bar(data_for_countries(CO2_emission_,cols,start_year, end_year),years),'Years',"Emission of CO2 (Metric tons per capita)",'Emission of CO2 for South Asian Countries')
names = ['Arable_land','Population_growth_','GDP_Data_','CO2_emission_','Agricultural_irrigated_land','Electric_power_consumption','Nitrous_oxide_emissions']
data_frames = [Arable_land,Population_growth_,GDP_Data_,CO2_emission_,Agricultural_irrigated_land,Electric_power_consumption,Nitrous_oxide_emissions]
country_name = ['Pakistan','Years']
make_corr_heat_map(get_data_for_specific_country(data_frames,country_name,names,start_year,end_year),'Pakistan','tab10')
country_name = ['India','Years']
make_corr_heat_map(get_data_for_specific_country(data_frames,country_name,names,start_year,end_year),'India','Paired')
country_name = ['Bangladesh','Years']
make_corr_heat_map(get_data_for_specific_country(data_frames,country_name,names,start_year,end_year),'Bangladesh','tab20c')
table_data = data_for_countries(GDP_Data_,cols,'1970','2021')
table_data = get_data_for_bar(table_data,['1970','1980','1990','2000','2010','2020'])
table_data = table_data.T
table_data = table_data.round(1)
table_data.head(7)
