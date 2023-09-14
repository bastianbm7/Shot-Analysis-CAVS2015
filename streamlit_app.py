# Librerías de manejo de datos
import pandas as pd
import numpy as np
import statsmodels.api as sm

# Librerías de visualización
import plotly.express as px
import plotly.graph_objs as go
import plotly.offline as pyo
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
import seaborn as sns
from matplotlib.offsetbox import OffsetImage

# Librerías de acceso a datos externos
import urllib

import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.colored_header import colored_header
from streamlit_extras.grid import grid
from streamlit_option_menu import option_menu
from streamlit_toggle import st_toggle_switch



def fig1():
    # Group the data by team and calculate the conversion rate for each
    team_rates = df_grouped.groupby('Nombre equipo')['Tiro convertido'].mean().reset_index()
    
    # Round the conversion rates to 2 decimal places and convert to percentages
    team_rates['Tiro convertido'] = round(team_rates['Tiro convertido'], 4) * 100
    
    # Sort the DataFrame by the conversion rates in descending order
    team_rates = team_rates.sort_values('Tiro convertido', ascending=False)
    
    # Create a bar plot of the conversion rates for each team using Plotly
    fig = px.bar(team_rates, x='Nombre equipo', y='Tiro convertido', color='Nombre equipo')
    
    # Set the layout properties
    fig.update_layout(
        title=dict(text='Porcentaje de tiro por equipos de la NBA en la temporada 2015-16', font=dict(size=22)),
        xaxis=dict(title='Equipo', title_font=dict(size=18), tickfont=dict(size=14)),
        yaxis=dict(title='Probabilidad de encestar un tiro (%)', title_font=dict(size=18), tickfont=dict(size=14)),
        height=600,
        width=800
    )
    
    return fig


def fig2():
    team_rates = df_grouped.groupby(['Nombre equipo','Fecha'])['Tiro convertido'].mean().round(2).reset_index()

    # Round the conversion rates to 2 decimal places and convert to percentages
    team_rates['Tiro convertido'] = round(team_rates['Tiro convertido'], 4) * 100
    
    # Sort the DataFrame by the conversion rates in descending order
    team_rates = team_rates.sort_values('Tiro convertido', ascending=False)
    
    # Define a list of team names to match
    team_names = ['Golden State Warriors']
    
    # Find all the unique values in the 'Nombre equipo' column that match the list of team names
    team_rates_filter = team_rates.loc[team_rates['Nombre equipo'].isin(team_names)]
    
    # Sort the DataFrame by the conversion rates in descending order
    team_rates_filter = team_rates_filter.sort_values(['Fecha'], ascending=False)
    
    # Create a list to store traces for each team
    traces = []
    
    # Loop through the team names and create a trace for each team
    for team_name in team_names:
        team_data = team_rates_filter[team_rates_filter['Nombre equipo'] == team_name]
        trace = go.Scatter(x=team_data['Fecha'], 
                           y=team_data['Tiro convertido'], 
                           mode='lines', 
                           name=team_name, 
                          line=dict(
                                width=3,
                          color = 'orange'))
        traces.append(trace)
    
    # Graph Cavaliers data 
    df_cavs = team_rates.loc[team_rates['Nombre equipo'] == 'Cleveland Cavaliers']
    df_cavs = df_cavs.sort_values('Fecha', ascending=False)
    
    trace = go.Scatter(x=df_cavs['Fecha'], 
                       y=df_cavs['Tiro convertido'], 
                       mode='lines', 
                       name='Cleveland Cavaliers', 
                       line=dict(
                                width=3,
                                color = 'blue'))
    traces.append(trace)
    
    # Create the figure and add the traces
    fig = go.Figure(data=traces)
    
    # Set the layout properties
    fig.update_layout(
        title=dict(text='Porcentaje de tiro por periodo de los 2 finalistas <br>equipos de la temporada 2015-16', font=dict(size=22)),
        xaxis=dict(title='Fecha', title_font=dict(size=18), tickfont=dict(size=14)),
        yaxis=dict(title='Porcentaje de efectividad en tiros (%)', title_font=dict(size=18), tickfont=dict(size=14)),
        height=600,
        width=800
    )
    
    # Update the x-axis category order to match the sorted "Periodo" values
    fig.update_xaxes(categoryorder='trace')
    
    # Adjust legend position to be at the top
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=0.95, xanchor="right", x=0.7))
    
    
    # Show the figure
    return fig


def fig3():
    df_cavs = df_grouped.loc[df_grouped['Nombre equipo'] == 'Cleveland Cavaliers']

    # Round the conversion rates to 2 decimal places and convert to percentages
    df_cavs['Tiro convertido'] = round(df_cavs['Tiro convertido'], 4) * 100
    
    fig = px.histogram(df_cavs, x='Tiro convertido', nbins = 30, marginal='box')
    
    # Set the layout properties
    fig.update_layout(
        title=dict(text='Distribución del porcentaje de efectividad en lanzamientos del equipo<br>de Cleveland Cavaliers en la temporada 2015-16', font=dict(size=22)),
        xaxis=dict(title='Porcentaje de efectividad en tiros', title_font=dict(size=18), tickfont=dict(size=14)),
        yaxis=dict(title='Cantidad de jugadores', title_font=dict(size=18), tickfont=dict(size=14)),
        height=600,
        width=800
    )
    return fig


def fig4():
    
    team_rates = df_grouped.groupby(['Nombre equipo','Fecha', 'Nombre jugador'])['Tiro convertido'].mean().round(2).reset_index()

    # Round the conversion rates to 2 decimal places and convert to percentages
    team_rates['Tiro convertido'] = round(team_rates['Tiro convertido'], 4) * 100
    
    # Sort the DataFrame by the conversion rates in descending order
    team_rates = team_rates.sort_values('Tiro convertido', ascending=False)
    
    # Crear QQ plot
    fig, ax = plt.subplots(figsize=(10, 8))  # Aumentar el tamaño (width=10, height=8)
    sm.qqplot(team_rates['Tiro convertido'], line='s', ax=ax)
    
    # Cambiar el título
    ax.set_title('QQ Plot de Porcentaje de tiros convertidos del equipo\nCleveland Cavaliers en la temporada 2015-16', fontsize=16)  # Cambiar el título y aumentar el tamaño de las letras
    
    # Cambiar el nombre del eje X
    ax.set_xlabel('Cuantiles teóricos', fontsize=14)  # Cambiar el nombre del eje X y aumentar el tamaño de las letras
    
    # Cambiar el nombre del eje Y
    ax.set_ylabel('Cuantiles observados', fontsize=14)  # Cambiar el nombre del eje Y y aumentar el tamaño de las letras
    
    return fig


def fig5():
    df_cavs = df_grouped.loc[df_grouped['Nombre equipo'] == 'Cleveland Cavaliers']

    team_rates = df_cavs.groupby(['Posicion', 'Nombre jugador', 'Fecha'])['Tiro convertido'].mean().reset_index()
    
    team_rates['Tiro convertido'] = round(team_rates['Tiro convertido'], 4)
    
    fig = px.box(team_rates, x='Nombre jugador', y='Tiro convertido', color='Posicion')
                  # Ajusta el ancho total del gráfico)
    # Set the layout properties
    fig.update_layout(
        title=dict(text='Porcentaje de efectividad en lanzamientos de todos los jugadores de<br>Cleveland Cavaliers en la temporada 2015-16', font=dict(size=22)),
        xaxis=dict(title='Nombre del jugador', title_font=dict(size=18), tickfont=dict(size=14)),
        yaxis=dict(title='Porcentaje de efectividad en lanzamientos', title_font=dict(size=18), tickfont=dict(size=14)),
        height=600,
        width=800
    )
    return fig


def fig6():
    df_cavs = df_grouped.loc[df_grouped['Nombre equipo'] == 'Cleveland Cavaliers']

    team_rates = df_cavs.groupby(['Posicion', 'Fecha'])['Distancia'].mean().reset_index()
    
    team_rates['Tiro convertido'] = round(team_rates['Distancia'], 4)
    
    fig = px.box(team_rates, x='Posicion', y='Distancia', color='Posicion')
    
    # Set the layout properties
    fig.update_layout(
        title=dict(text='Distancia media de los tiros realizados por posición de los jugadores de<br>Cleveland Cavaliers en la temporada 2015-16', font=dict(size=22)),
        xaxis=dict(title='Posicion', title_font=dict(size=18), tickfont=dict(size=14)),
        yaxis=dict(title='Distancia media (ft)', title_font=dict(size=18), tickfont=dict(size=14)),
        height=600,
        width=800
    )
    return fig




def fig7():
    def draw_court(outer_lines=False):
        # Create a Plotly figure
        fig = go.Figure()
    
        # Create the basketball hoop
        hoop = go.Scatter(
            x=[0],
            y=[0],
            mode='markers',
            marker=dict(size=15, color='black'),
            showlegend=False,
            hoverinfo='none'  # Disable hover details
        )
    
        # Create backboard
        backboard = go.Scatter(
            x=[-30, 30],
            y=[-7.5, -7.5],
            mode='lines',
            line=dict(color='black', width=2),
            showlegend=False,
            hoverinfo='none'  # Disable hover details
        )
    
        # The paint
    
    
        # Create the inner box of the paint
        box = go.Scatter(
            x=[-70, 70, 70, -70, -70],
            y=[-47.5, -47.5, 142.5, 142.5, -47.5],
            mode='lines',
            line=dict(color='black', width=2),
            showlegend=False,
            hoverinfo='none'  # Disable hover details
        )
    
        # Create free throw top arc
        top_free_throw = go.Scatter(
            x=[0],
            y=[142.5],
            mode='lines',
            line=dict(color='black', width=2),
            showlegend=False,
            hoverinfo='none'  # Disable hover details
        )
    
        # Create free throw bottom arc
        bottom_free_throw = go.Scatter(
            x=[0],
            y=[142.5],
            mode='lines',
            line=dict(color='black', width=2, dash='dash'),
            showlegend=False,
            hoverinfo='none'  # Disable hover details
        )
    
        # Restricted Zone
        restricted_zone = go.Scatter(
            x=[0],
            y=[0],
            mode='lines',
            line=dict(color='black', width=2),
            showlegend=False,
            hoverinfo='none'  # Disable hover details
        )
    
        # Three-point line
        corner_three_a = go.Scatter(
            x=[-220, -220],
            y=[-47.5, 92.5],
            mode='lines',
            line=dict(color='black', width=2),
            showlegend=False,
            hoverinfo='none'  # Disable hover details
        )
    
        corner_three_b = go.Scatter(
            x=[220, 220],
            y=[-47.5, 92.5],
            mode='lines',
            line=dict(color='black', width=2),
            showlegend=False,
            hoverinfo='none'  # Disable hover details
        )
    
        three_arc = go.Scatter(
            x=[-220, -70, 70, 220],
            y=[92.5, 300, 300, 92.5],
            mode='lines',
            line=dict(color='black', width=2),
            showlegend=False,
            hoverinfo='none'  # Disable hover details
        )
    
        # Center Court
        center_outer_arc = go.Scatter(
            x=[0],
            y=[422.5],
            mode='lines',
            line=dict(color='black', width=2),
            showlegend=False,
       #     hoverinfo='none'  # Disable hover details
        )
    
        center_inner_arc = go.Scatter(
            x=[0],
            y=[422.5],
            mode='lines',
            line=dict(color='black', width=2),
            showlegend=False,
            hoverinfo='none'  # Disable hover details
        )
    
        # Add the court elements to the figure
        fig.add_trace(hoop)
        fig.add_trace(backboard)
        fig.add_trace(box)
        fig.add_trace(top_free_throw)
        fig.add_trace(bottom_free_throw)
        fig.add_trace(restricted_zone)
        fig.add_trace(corner_three_a)
        fig.add_trace(corner_three_b)
        fig.add_trace(three_arc)
        fig.add_trace(center_outer_arc)
        fig.add_trace(center_inner_arc)
    
        if outer_lines:
            # Draw the half-court line, baseline, and side out-of-bounds lines
            outer_lines = go.Scatter(
                x=[-250, 250],
                y=[-47.5, -47.5],
                mode='lines',
                line=dict(color='black', width=2),
        #        showlegend=False,
            hoverinfo='none'  # Disable hover details
            )
            fig.add_trace(outer_lines)
    
        # Set the layout properties
        fig.update_layout(
            xaxis=dict(range=[-250, 250]),
            yaxis=dict(range=[-47.5, 422.5]),
            showlegend=False,
            height = 600,
            width = 800
        )
        return fig
    
    
    fig = draw_court()

    df_cavs = df.loc[(df['Nombre equipo'] == 'Cleveland Cavaliers') & (df['Tiro convertido'] == 1)]
    
    vars = ['X Posicion', 'Y Posicion', 'Distancia', 'Tiro convertido']
    #team_rates = df_cavs.groupby(['Nombre jugador', 'Posicion'])[vars].mean().reset_index()
    
    #team_rates['Tiro convertido'] = round(team_rates['Tiro convertido'], 4)
    
    
    scatter_fig = px.scatter(df_cavs, x="X Posicion", y="Y Posicion", color="Posicion")
    colors = {'Base': 'blue', 'Escolta': 'red', 'Posición3': 'green', 'Alero': 'yellow', 'Ala-Pívot': 'purple', 'Pívot': 'black'}
    
    for trace in scatter_fig.data:
        fig.add_trace(trace)
        
    for trace in scatter_fig.data:
        trace.marker.color = trace.marker.line.color = colors[trace.name]
    
    # Personalizar el diseño del gráfico
    fig.update_layout(
        title=dict(text="Posicion de los tiros convertidos por cada posición de los jugadores de <br>Cleveland Cavaliers en la temporada 2015-16", font=dict(size=22)),
        xaxis_title="",
        yaxis_title="",
        showlegend = True,
        legend_title="Posición",
        width=800,
        height=600,
            legend=dict(
            x=1.05,  # Ajusta la posición en el eje X para colocar la leyenda al costado derecho
            y=0.5,   # Ajusta la posición en el eje Y para centrar verticalmente la leyenda
        )
    )
    return fig


def fig8():
    def draw_court(ax=None, color='black', lw=2, outer_lines=False):
        if ax is None:
            ax = plt.gca()
    
        hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)
        backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)
        outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
        inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)
        top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
        bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color, linestyle='dashed')
        restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)
        corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
        corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
        three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)
        center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
        center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)
    
        court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw, bottom_free_throw, restricted,
                          corner_three_a, corner_three_b, three_arc, center_outer_arc, center_inner_arc]
    
        if outer_lines:
            outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw, color=color, fill=False)
            court_elements.append(outer_lines)
    
        for element in court_elements:
            ax.add_patch(element)
    
        ax.set_xlim(-250, 250)
        ax.set_ylim(-47.5, 422.5)
        ax.set_aspect('equal', adjustable='box')
        ax.axis('off')
    
        return ax
    
    df_cavs = df.loc[(df['Nombre equipo'] == 'Cleveland Cavaliers') & (df['Tiro convertido'] == 1)]

    # create our jointplot
    df_cavs = df_cavs.rename(columns={'X Posicion': 'LOC_X'})
    df_cavs = df_cavs.rename(columns={'Y Posicion': 'LOC_Y'})
    # get our colormap for the main kde plot
    # Note we can extract a color from cmap to use for 
    # the plots that lie on the side and top axes
    cmap=plt.cm.YlOrRd_r 
    
    # n_levels sets the number of contour lines for the main kde plot
    joint_shot_chart = sns.jointplot(data = df_cavs, x = 'LOC_X', y = 'LOC_Y', stat_func=None,
                                     kind='kde', space=0, color=cmap(0.1),
                                     cmap=cmap, n_levels=30)
    
    joint_shot_chart.fig.set_size_inches(10,8)
    
    # A joint plot has 3 Axes, the first one called ax_joint 
    # is the one we want to draw our court onto and adjust some other settings
    ax = joint_shot_chart.ax_joint
    draw_court(ax)
    
    # Adjust the axis limits and orientation of the plot in order
    # to plot half court, with the hoop by the top of the plot
    ax.set_xlim(-250,250)
    ax.set_ylim(422.5, -47.5)
    
    # Get rid of axis labels and tick marks
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params(labelbottom='off', labelleft='off')
    
    # Add a title
    ax.set_title('Posicion de los tiros convertidos de los jugadores de\nCleveland Cavaliers en la temporada 2015-16', 
                 y=1.2, fontsize=16)
    
    # Add Data Source and Author
    ax.text(-250,445,
            'Author: Savvas Tjortjoglou', fontsize=10)
    
    return joint_shot_chart






# Specify the path to the CSV file you want to read
file_path = r'C:\Users\Bastian Barraza M\OneDrive\Documentos\Visualización de datos\Prueba 1\dataComplete.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Specify the path to the CSV file you want to read
file_path = r'C:\Users\Bastian Barraza M\OneDrive\Documentos\Visualización de datos\Prueba 1\dataGrouped.csv'

# Read the CSV file into a DataFrame
df_grouped = pd.read_csv(file_path)




colored_header(
    label=("Eficacia en tiros de los jugadores de Cleveland Cavaliers primer periodo de la temporada 2015-16: Análisis comparativo "),
    description='',
            color_name="red-70")
with st.sidebar:
    st.markdown('##### IECD421: Visualización de datos ')
    st.markdown('##### Alumno: Bastian Barraza Morales')
    st.markdown('##### Profesor: Javier Contreras Reyes')
    st.divider()
selected = option_menu("Preguntas", ["Pregunta 1", 'Pregunta 2', 'Pregunta 3', 'Pregunta 4', 'Pregunta 5'], 
    icons=['one', 'two', 'three', 'four', 'five'], menu_icon="cast", orientation = 'horizontal', default_index=0)

if selected == 'Pregunta 1':
    with st.sidebar:
        colored_header(
            label=("¿Cuál fue el porcentaje de tiros encestados por los equipos de la NBA en el año 2016 en general? "),
            description='',
            color_name="blue-green-70")
    
    
    fig1 = fig1()
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)


if selected == 'Pregunta 2':
    with st.sidebar:
        colored_header(
            label=("¿Cómo varió la efectividad de los tiros de Cleveland Cavaliers a lo largo del año 2015-16?"),
            description='',
            color_name="blue-green-70")

    fig2 = fig2()
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

    
if selected == 'Pregunta 3':
    with st.sidebar:
        colored_header(
            label=("¿Cuáles fueron los jugadores más efectivos en términos de tiros convertidos?"),
            description='',
            color_name="blue-green-70")
    
    options = ["Histograma", "QQ-Plot", "Boxplot"]
    # Create tabs
    tab1, tab2, tab3 = st.tabs(options)
    with tab1:
        fig3 = fig3()
        st.plotly_chart(fig3, theme="streamlit", use_container_width=True)
    
    with tab2:
        fig4 = fig4()
        st.pyplot(fig4)
    with tab3:
        fig5 = fig5()
        st.plotly_chart(fig5, theme="streamlit", use_container_width=True)


if selected == 'Pregunta 4':
    with st.sidebar:
        colored_header(
            label=("¿Cuál es la distancia adecuada para lanzar en cada posición en términos de tiros convertidos?"),
            description='',
            color_name="blue-green-70")

    fig6 = fig6()
    st.plotly_chart(fig6, theme="streamlit", use_container_width=True)

if selected == 'Pregunta 5':
    with st.sidebar:
        colored_header(
            label=("¿Existen áreas específicas del campo desde las cuales el equipo tuvo una mayor cantidad de tiros anotados?"),
            description='',
            color_name="blue-green-70")

    options = ["Scatterplot", "Heatmap"]
    # Create tabs
    tab1, tab2 = st.tabs(options)
    with tab1:
        fig7 = fig7()
        st.plotly_chart(fig7, theme="streamlit", use_container_width=True)
    
    with tab2:
        fig8 = fig8()
        st.pyplot(fig8)