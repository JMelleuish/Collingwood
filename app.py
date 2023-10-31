from shiny import App, Inputs, Outputs, Session, render, ui
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import numpy as np

app_ui = ui.page_fluid(
    ui.input_select("x", "Select Team", 
                    {'Adelaide':'Adelaide',
                     'Brisbane Lions':'Brisbane Lions',
                     'Carlton':'Carlton',
                     'Collingwood': 'Collingwood',
                     'Essendon':'Essendon',
                     'Fremantle':'Fremantle',
                     'Geelong': 'Geelong',
                     'Gold Coast': 'Gold Coast',
                     'Greater Western Sydney':'Greater Western Sydney',
                     'Hawthorn':'Hawthorn',
                     'Melbourne':'Melbourne',
                     'North Melbourne':'North Melbourne',
                     'Port Adelaide':'Port Adelaide',
                     'Richmond':'Richmond',
                     'St Kilda':'St Kilda',
                     'Sydney':'Sydney',
                     'West Coast':'West Coast',
                     'Western Bulldogs':'Western Bulldogs'}),
    ui.output_plot("DayOfWeek"),
    ui.output_plot("Opposition"),
    ui.input_select("y", "Select Year", {'2011':'2011', '2012':'2012', '2013':'2013', '2014':'2014', '2015':'2015', '2016':'2016', '2017':'2017', '2018':'2018', '2019':'2019', '2020':'2020', '2021':'2021', '2022':'2022', '2023':'2023'}),
    ui.output_plot("Margin"),
    ui.output_plot("Crowd")   
)


def server(input, output, session):
    df = pd.read_csv(Path(__file__).parent / "AFL.csv")
    colour_codes = {'Geelong': '#002B5C', 'Sydney':'#E1251B' , 'Hawthorn':'#4D2004', 'Collingwood': '#000000', 'Richmond':'#FFD200', 'West Coast':'#F2A900','Adelaide':'#E21937','Fremantle':'#2A0D54','Port Adelaide':'#008AAB', 'Western Bulldogs':'#20539D', 'Essendon':'#CC2031', 'Greater Western Sydney':'#F47920', 'North Melbourne':'#1A3B8E', 'St Kilda':'#ED1B2F', 'Melbourne':'#0F1131', 'Brisbane Lions':'#FDBE57', 'Carlton':'#031A29', 'Gold Coast': '#FFDD00' }
        
    @output
    @render.plot(alt="A histogram")
    def DayOfWeek():
        WinPercent = df[df['Team'] == input.x()]
        WinPercent = WinPercent.groupby(['Day', 'WinLoss']).size().reset_index(name='count')
        WinPercent['percentage'] = round((WinPercent['count'] / WinPercent.groupby('Day')['count'].transform('sum'))*100)
        WinPercent = WinPercent.iloc[1::2]
        WinPercent = WinPercent.sort_values(by = 'percentage', ascending=False)

        fig, ax = plt.subplots(figsize=(18,5))
        bar = ax.bar(WinPercent['Day'], WinPercent['percentage'], color = colour_codes[input.x()])
        plt.xticks(rotation = 25)
        plt.title(f'{input.x()}s win percentage per each day of the week since 2011')
        plt.xlabel("Team")
        plt.ylabel("Percentage")
        ax.bar_label(bar)
        plt.show()
        return fig

    @output
    @render.plot(alt="A histogram")
    def Opposition():
        WinPercent = df[df['Team'] == input.x()]
        WinPercent = WinPercent.groupby(['Opposition', 'WinLoss']).size().reset_index(name='count')
        WinPercent['percentage'] = round((WinPercent['count'] / WinPercent.groupby('Opposition')['count'].transform('sum'))*100)
        WinPercent = WinPercent.iloc[1::2]
        WinPercent = WinPercent.sort_values(by = 'percentage', ascending=False)
        
        fig, ax = plt.subplots(figsize=(18,5))
        bar = ax.bar(WinPercent['Opposition'], WinPercent['percentage'], color = colour_codes[input.x()])
        plt.xticks(rotation = 90)
        plt.title(f'{input.x()}s win percentage against each team since 2011')
        plt.xlabel("Team")
        plt.ylabel("Percentage")
        ax.bar_label(bar)
        return fig

    @output
    @render.plot(alt="A line plot")
    def Margin():
        Team = df[df['Team'] == input.x()]
        Season = Team[Team['Season'] == int(input.y())]
        Season['zero'] = 0

        fig, ax = plt.subplots(figsize=(18,5))
        plt.plot(Season['Round'], Season['Margin'], color = colour_codes[input.x()], label = 'Margin')
        plt.plot(Season['Round'], Season['zero'], color = 'green', label= 'Draw')
        plt.xticks(Season['Round'])
        plt.title(f'{input.x()}s margin per round in season {input.y()}')
        plt.xlabel("Round (Bye rounds omitted)")
        plt.ylabel("Margin")
        plt.legend()
        return fig

    @output
    @render.plot(alt="A line plot")
    def Crowd():  
        Team = df[df['Team'] == input.x()]
        Season = Team[Team['Season'] == int(input.y())]
        Wins = Season[Season['WinLoss'] == 'Win']
        Loss = Season[Season['WinLoss'] == 'Loss']
        Season['MCG'] = 100024
        Season['Optus'] = 61266
        Season['SCG'] = 48000


        fig, ax = plt.subplots(figsize=(18,5))
        plt.scatter(Wins['Round'], Wins['ActualCrowd'], c = 'lightgreen', label = 'Win')
        plt.scatter(Loss['Round'], Loss['ActualCrowd'], c = 'red', label = 'Loss')
        plt.plot(Season['Round'], Season['MCG'], color = 'green', label='MCG')
        plt.plot(Season['Round'], Season['Optus'], color = '#F2A900', label="Optus")
        plt.plot(Season['Round'], Season['SCG'], color = 'red', label='SCG')
        plt.xticks(Season['Round'])
        plt.title(f'{input.x()}s crowd attendance per round in season {input.y()}')
        plt.xlabel("Round (Bye rounds omitted)")
        plt.ylabel("Crowd Attendance")
        plt.legend(loc='upper right')
        return fig

app = App(app_ui, server, debug=True)