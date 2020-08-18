#Description: This is a plotter using streamlit

import streamlit as st
import pandas as pd
from PIL import Image
import datetime
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go

def select_block_container_style():
    """Add selection section for setting setting the max-width and padding
    of the main block container"""

    max_width = 1200
    max_width_str = f"max-width: 100%;"

    st.markdown(
    f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
        padding-top: {1}rem;
        padding-right: {1}rem;
        padding-left: {3}rem;
        padding-bottom: {1}rem;
    }}
    .reportview-container .main {{
        color: {COLOR};
        background-color: {BACKGROUND_COLOR};
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )

#Create a function to get the users Input

def get_input():

    #if st.sidebar.checkbox('Default Date: ',False):
    #    start_date = st.sidebar.text_input("Start Date",earlier_str)
    #    end_date = st.sidebar.text_input("End Date",current_str)
    #else:
    start_date = st.sidebar.text_input("Start Date","2020-08-10")
    end_date = st.sidebar.text_input("End Date","2020-08-14")

    return start_date,end_date

#Create a function to get the proper data from timeframe range
#@st.cache
def get_data(start,end):

    # Collects user input features into dataframe
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])

    if uploaded_file is not None:
        warning_func()

        df = pd.read_csv(uploaded_file)
        df['Date'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

        #Get the date range
        start = pd.to_datetime(start)
        end = pd.to_datetime(end)

        for i in range(0, len(df)):
            if start <= pd.to_datetime(df['Date'][i]):
                start_row = i
                break
        for j in range(0, len(df)):
            if end >= pd.to_datetime(df['Date'][len(df)-1-j]):
                end_row = len(df) -1 -j
                break
        df = df.set_index(pd.DatetimeIndex(df['Date'].values))

        return df.iloc[start_row:end_row,:]


    else:
        df = pd.DataFrame(columns = ['Date','Time'])

def warning_func():

    global state
    if st.sidebar.checkbox("Display Charts",False):
        st.success("VIEWING CHART ENABLED")
        state = True
    else:
        st.warning("VIEW CHART DISABLED")
        state = False

#-----PLOTLY PLOTS (trace and layout)

def plotter_func():

    if state is True:
        #date time
        date_data =  df['Date']

        #ram usage
        used_mem =  df['Used_RAM(%)']
        temp_mem = df['Used plus Temporarily Used RAM(%)']
        evtc_mem =  df['evtc_MEM']
        eimproc_mem =  df['eimproc_MEM']
        tpa_mem =  df['tpa_server_sparc_MEM']

        #pc load averages
        load_cpu_ave1 = df['Load_Average(1min)']
        load_cpu_ave5 = df['Load_Average(5min)']
        load_cpu_ave15 = df['Load_Average(15min)']
        cpu_ave = df['CPU LOAD AVERAGE(%)']

        # apps cpu average
        evtc_cpu_ave = df['evtc_CPU_AVE']
        tpa_cpu_ave = df['tpa_server_sparc_CPU_AVE']
        eimproc_cpu_ave = df['eimproc_CPU_AVE']

        # apps cpu instantaneous
        evtc_cpu = df['evtc_CPU']
        tpa_cpu = df['tpa_server_sparc_CPU']
        eimproc_cpu = df['eimproc_CPU']

        # remote connections
        vnc_con = df['VNC_viewer_sessions']
        ssh_con = df['SSH_Connections']
        telnet_con = df['Telnet_Connections']

        #Top1_Cpu_Usage,Top2_Cpu_Usage,Top3_Cpu_Usage,Top4_Cpu_Usage,Top5_Cpu_Usage
        #Top1_RAM_Usage,Top2_RAM_Usage,Top3_RAM_Usage,Top4_RAM_Usage,Top5_RAM_Usage


        trace1 = go.Scatter(x = date_data,y = cpu_ave,mode = 'lines',name = 'Cpu Ave',fill='tozeroy')
        trace2 = go.Scatter(x = date_data,y = load_cpu_ave1,mode = 'lines',name = '1 min  ',fill='tozeroy')
        trace3 = go.Scatter(x = date_data,y = load_cpu_ave5,mode = 'lines',name = '5 min  ',fill='tozeroy')
        trace4 = go.Scatter(x = date_data,y = load_cpu_ave15,mode = 'lines',name = '15 min ',fill='tozeroy')
        trace5 = go.Scatter(x = date_data,y = temp_mem,mode = 'lines',name = 'Temp RAM',stackgroup = 'one')
        trace6 = go.Scatter(x = date_data,y = used_mem,mode = 'lines',name = 'Used RAM',stackgroup = 'one')

        trace7 = go.Scatter(x = date_data,y = evtc_cpu_ave,mode = 'lines',name = 'Evtc CPU',stackgroup = 'one')
        trace8 = go.Scatter(x = date_data,y = tpa_cpu_ave,mode = 'lines',name = 'Tpa CPU ',stackgroup = 'one')
        trace9 = go.Scatter(x = date_data,y = eimproc_cpu_ave,mode = 'lines',name = 'Eim CPU',stackgroup = 'one')

        trace10 = go.Scatter(x = date_data,y = evtc_mem,mode = 'lines',name = 'Evtc MEM',stackgroup = 'one')
        trace11 = go.Scatter(x = date_data,y = tpa_mem,mode = 'lines',name = 'Tpa MEM ',stackgroup = 'one')
        trace12 = go.Scatter(x = date_data,y = eimproc_mem,mode = 'lines',name = 'Eim MEM',stackgroup = 'one')

        trace13 = go.Scatter(x = date_data,y = vnc_con,mode = 'lines',name = 'VNC User',stackgroup = 'one')
        trace14 = go.Scatter(x = date_data,y = ssh_con,mode = 'lines',name = 'SSH User  ',stackgroup = 'one')
        trace15 = go.Scatter(x = date_data,y = telnet_con,mode = 'lines',name = 'TELNET',stackgroup = 'one')


        layout1 = go.Layout(
            #title = "CPU Usage Monitoring",
            xaxis = {'showgrid':False},yaxis = {'showgrid':False},
            xaxis2 = {'showgrid':False},yaxis2 = {'showgrid':False},
            xaxis3 = {'showgrid':False},yaxis3 = {'showgrid':False},

            width = 1450,height = 450,
            plot_bgcolor = "rgb(255, 255, 255)",
            paper_bgcolor = "rgb(0,0,0)",
            margin = {'b':8,'l':8,'r':20,'t':40,'pad':1 },
            #font=dict(family="Arial",size=12,color="White"),
            font=dict(color="White",size=10),
            legend=dict(orientation="h",bgcolor="rgb(18, 51, 52)",bordercolor='silver',borderwidth=2,xanchor='center',y=-0.1,x=0.5)
            )

        layout2 = go.Layout(
            xaxis = {'showgrid':False},yaxis = {'showgrid':False},
            xaxis2 = {'showgrid':False},yaxis2 = {'showgrid':False},

            plot_bgcolor = "rgb(255, 255, 255)",
            paper_bgcolor = "rgb(0,0,0)",
            margin = {'b':8,'l':8,'r':20,'t':40,'pad':1 },
            font=dict(color="White",size=10),
            width = 1450,height = 450,
            legend=dict(orientation="h",bgcolor="rgb(18, 51, 52)",bordercolor='silver',borderwidth=2,xanchor='center',y=-0.1,x=0.5)
            )

        layout3 = go.Layout(
            xaxis = {'showgrid':False},yaxis = {'showgrid':False},
            xaxis2 = {'showgrid':False},yaxis2 = {'showgrid':False},
            xaxis3 = {'showgrid':False},yaxis3 = {'showgrid':False},
            xaxis4 = {'showgrid':False},yaxis4 = {'showgrid':False},

            plot_bgcolor = "rgb(255, 255, 255)",
            paper_bgcolor = "rgb(0,0,0)",
            margin = {'b':8,'l':8,'r':20,'t':40,'pad':1 },
            font=dict(color="White",size=10),
            width = 1450,height = 600,
            legend=dict(orientation="h",bgcolor="rgb(18, 51, 52)",bordercolor='silver',borderwidth=2,xanchor='center',y=-0.1,x=0.5)

            )

        layout4 = go.Layout(
            xaxis = {'showgrid':False},yaxis = {'showgrid':False},

            plot_bgcolor = "rgb(255, 255, 255)",
            paper_bgcolor = "rgb(0,0,0)",
            margin = {'b':8,'l':8,'r':20,'t':40,'pad':1 },
            font=dict(color="White",size=10),
            width = 1450,height = 400,
            legend=dict(orientation="h",bgcolor="rgb(18, 51, 52)",bordercolor='silver',borderwidth=2,xanchor='center',y=-0.1,x=0.5)

            )

        #fig1 = go.Figure(data=[trace1,trace2], layout=layout1)

        fig1 = make_subplots(rows=3, cols=1)
        fig1.append_trace(trace1,row=1,col=1)
        fig1.append_trace(trace2,row=2,col=1)
        fig1.append_trace(trace3,row=2,col=1)
        fig1.append_trace(trace4,row=2,col=1)
        fig1.append_trace(trace5,row=3,col=1)
        fig1.append_trace(trace6,row=3,col=1)
        fig1.update_layout(layout1)

        fig2 = make_subplots(rows=2, cols=1)
        fig2.append_trace(trace7,row=1,col=1)
        fig2.append_trace(trace8,row=1,col=1)
        fig2.append_trace(trace9,row=1,col=1)
        fig2.append_trace(trace10,row=2,col=1)
        fig2.append_trace(trace11,row=2,col=1)
        fig2.append_trace(trace12,row=2,col=1)
        fig2.update_layout(layout2)

        fig3 = make_subplots(rows=4, cols=1)
        fig3.append_trace(trace1,row=1,col=1)
        fig3.append_trace(trace5,row=2,col=1)
        fig3.append_trace(trace6,row=3,col=1)
        fig3.append_trace(trace7,row=4,col=1)
        fig3.update_layout(layout3)

        fig4 = make_subplots(rows=1, cols=1)
        fig4.append_trace(trace13,row=1,col=1)
        fig4.append_trace(trace14,row=1,col=1)
        fig4.append_trace(trace15,row=1,col=1)
        fig4.update_layout(layout4)

        #if st.checkbox('View Cpu Usage Plots'):
        st.header("CPU and Memory Usage\n")
        st.plotly_chart(fig1)

        st.header("Application CPU and Mem Usage\n")
        st.plotly_chart(fig2)

        #if st.checkbox('View Mem Usage Plots'):
        st.header("Standard Monitoring Patterns\n")
        st.plotly_chart(fig3)

        st.header("Remote Connections\n")
        st.plotly_chart(fig4)

        #Get statistics on the Data
        if st.sidebar.checkbox("Data Statistics",False):
            st.header('Data Statistics')
            stat = df.drop(columns=['dummy28','dummy29','dummy30','dummy31','dummy32','dummy33','dummy34','dummy35','dummy36','dummy42','dummy43','dummy44','dummy45','dummy46','dummy47','dummy48','dummy49','dummy50','dummy51','dummy52','dummy53'])
            st.write(stat.describe())
    else:
        return
##---MAIN-----

global COLOR
global BACKGROUND_COLOR

state = False
#Set the start and end index rows both to 0
start_row = 0
end_row = 0

BACKGROUND_COLOR = "rgb(18, 51, 52)"
COLOR = "#fff"

#Add a title and an Image
st.write("""
# Machine Learning Web Application
Learning Streamlit, Plotly, CSS Grid
""")

st.set_option('deprecation.showfileUploaderEncoding', False)

# Get the start and end date display
now = datetime.datetime.now()
interval = datetime.timedelta(hours=12)
earlier_date = now - interval

current_str = now.strftime("%Y-%m-%d %H:%M:%S")
earlier_str = earlier_date.strftime("%Y-%m-%d %H:%M:%S")

image = Image.open("ml.jpeg")
st.image(image, width=300, height=1200)

#layout
select_block_container_style()

#Create a sidebar header
st.sidebar.header('User Inputs')

#Get the Users Input
start, end = get_input()
#Get the DataFrame
df = get_data(start, end)

plotter_func()
