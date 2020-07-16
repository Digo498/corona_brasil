
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates 
import matplotlib.animation as animation 
import matplotlib.cm as cm
import matplotlib 
import numpy as np 
import pandas as pd
from datetime import datetime, timedelta, date
import csv
import sys
from requests import get
from pathlib import Path


####################### IMPORTING AND SETTING UP DATA #################

###### Import cities
print('Lendo as cidades no arquivo "brasil.in". Altere o arquivo, caso necessário.\nCidades que serão plotadas:\n')

inFile = sys.argv[1]
cities = []
states = []
with open(inFile, 'r') as file:
    csv_reader = csv.reader(file, delimiter=',')
    for line in csv_reader:
        print(f'{line[0]} - {line[1]}')
        
        city, state = line 
        cities.append(city)
        states.append(state)

Path("plots").mkdir(parents=True, exist_ok=True)


######## Import data
data_url = 'https://data.brasil.io/dataset/covid19/caso_full.csv.gz'
data_file = './caso_full.csv.gz'

print('\n\nBaixando os dados mais recentes de: https://data.brasil.io/dataset/covid19/caso_full.csv.gz ')

with open(data_file, 'wb' ) as file:
    response = get(data_url)

    file.write(response.content)



print('\nImportando dados...\n')

data = pd.read_csv(data_file)
data['date'] = pd.to_datetime(data.date, format='%Y-%m-%d')



############# Calculate city, week and country data gathered in weeks
print('\nCalculando dados agrupados em semanas...\n')


#city
mean_data_week = data.groupby(['city', 'state','epidemiological_week', 'place_type'], as_index=False).mean()
max_data_week = data.groupby(['city', 'state', 'epidemiological_week', 'place_type'], as_index=False).max() 
sum_data_week = data.groupby(['city', 'state', 'epidemiological_week', 'place_type'], as_index=False).sum()


#state
state_data = data[ (data['place_type'] == 'state')  ].groupby(['epidemiological_week', 'state'], as_index=False).max()
grouped = data[(data['place_type'] == 'state')].groupby(['epidemiological_week','state'], as_index=False ).sum()
state_data['new_confirmed'] = grouped['new_confirmed']
state_data['new_deaths'] = grouped['new_deaths']


#brasil
brasil_data = state_data.groupby(['epidemiological_week'], as_index=False).sum()
brasil_data['last_available_confirmed_per_100k_inhabitants'] = brasil_data['last_available_confirmed']/brasil_data['estimated_population_2019']
brasil_data['last_available_death_rate'] = brasil_data['last_available_deaths']/brasil_data['last_available_confirmed']






####### PLOT CITY DATA ################

dtype = ['last_available_confirmed', 'new_confirmed', 'last_available_confirmed_per_100k_inhabitants', 'last_available_death_rate', 'last_available_deaths', 'new_deaths']
dtype_name = ['Total de casos', 'Novos casos', 'Casos por 100 mil habitantes', 'Taxa de mortalidade', 'Total de mortes', 'Novas mortes']

def week_axes(ax, array, tipo, cidade, estado, name):
    ax.plot( array[(array.city  == cidade) & (array.state == estado)]['epidemiological_week'], array[(array.city  == cidade) & (array.state == estado)][ tipo ],  label=name, marker='o', linestyle='dashed'  )
    
    ax.legend()
    ax.grid()

    ax.set_ylim(bottom=0)



def plot_all_of_city_weekly(cidade, estado):
    fig, axs = plt.subplots(3,2, figsize=(12,6), sharex=True)


    week_axes(axs[0,0], max_data_week, dtype[0], cidade, estado, dtype_name[0])
    week_axes(axs[0,1], sum_data_week, dtype[1], cidade, estado, dtype_name[1])
    week_axes(axs[1,0], max_data_week, dtype[2], cidade, estado, dtype_name[2])
    week_axes(axs[1,1], mean_data_week, dtype[3], cidade, estado, dtype_name[3])
    week_axes(axs[2,0], max_data_week, dtype[4], cidade, estado, dtype_name[4])
    week_axes(axs[2,1], sum_data_week, dtype[5], cidade, estado, dtype_name[5])

    fig.suptitle(f'{cidade} - {estado}')

    plt.legend()
    axs[2,1].set_xlabel('Semana')
    axs[2,0].set_xlabel('Semana')

    plt.savefig(f'plots/{cidade}-{estado}.png')



for i in range(len(cities)):
    print(f'Fazendo gráfico de {cities[i]} - {states[i]}')
    plot_all_of_city_weekly( cities[i], states[i] )




######## PLOT BRASIL DATA
print('\nFazendo o gráfico do Brasil...')



def brasil_axes(ax, tipo, name):
    ax.plot( brasil_data['epidemiological_week'], brasil_data[ tipo ],  label=name , marker='o', linestyle='dashed' )
    
    ax.legend()
    ax.grid()

    ax.set_ylim(bottom=0)



def plot_brasil_weekly():
    fig, axs = plt.subplots(3,2, figsize=(12,6), sharex=True)


    brasil_axes(axs[0,0], dtype[0], dtype_name[0])
    brasil_axes(axs[0,1], dtype[1], dtype_name[1])
    brasil_axes(axs[1,0], dtype[2], dtype_name[2])
    brasil_axes(axs[1,1], dtype[3], dtype_name[3])
    brasil_axes(axs[2,0], dtype[4], dtype_name[4])
    brasil_axes(axs[2,1], dtype[5], dtype_name[5])

    fig.suptitle('Brasil')

    plt.legend()

    axs[2,1].set_xlabel('Semana')
    axs[2,0].set_xlabel('Semana')

    plt.savefig('plots/Brasil.png')


plot_brasil_weekly()


########## PLOT STATE DATA

print(f'\nFazendo o gráfico dos estados...')

unique_states = np.unique(states)


def state_axes(ax, tipo, name, state):
    ax.plot( state_data[state_data['state'] == state]['epidemiological_week'], state_data[state_data['state'] == state][ tipo ],  label=name , marker='o', linestyle='dashed'  )
    
    ax.legend()
    ax.grid()

    ax.set_ylim(bottom=0)



def plot_state_weekly(state):
    fig, axs = plt.subplots(3,2, figsize=(12,6), sharex=True )


    state_axes(axs[0,0], dtype[0], dtype_name[0], state)
    state_axes(axs[0,1], dtype[1], dtype_name[1], state)
    state_axes(axs[1,0], dtype[2], dtype_name[2], state)
    state_axes(axs[1,1], dtype[3], dtype_name[3], state)
    state_axes(axs[2,0], dtype[4], dtype_name[4], state)
    state_axes(axs[2,1], dtype[5], dtype_name[5], state)

    fig.suptitle(f'{state}')

    plt.legend()

    axs[2,1].set_xlabel('Semana')
    axs[2,0].set_xlabel('Semana')

    plt.savefig(f'plots/{state}.png')



for i in unique_states:
    plot_state_weekly(i)


print('\nPronto! Os gráfico estão na pasta "plots".')
