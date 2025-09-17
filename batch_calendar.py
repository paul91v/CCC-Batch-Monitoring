# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 16:33:41 2025

@author: Paul
"""

import streamlit as st
from streamlit_calendar import calendar
import pandas as pd
import datetime as dt

st.set_page_config(layout="wide")

weekday_dict = {6:'Sunday',
             0:'Monday',
             1:'Tuesday',
             2:'Wednesday',
             3:'Thursday',
             4:'Friday',
             5:'Saturday'}

def get_time_duration(raw_time):
    raw_time = raw_time.replace('to','-')
    raw_time = raw_time.upper()
    raw_time = raw_time.replace(' ','')
    raw_time = raw_time.replace('.',':')
    processed_time = list(map(lambda x:x.strip(), raw_time.split('-')))
    processed_time = [dt.datetime.strptime(t, '%I%p').time() if ':' not in t else dt.datetime.strptime(t, '%I:%M%p').time() for t in processed_time]
    return processed_time

def create_ccc_sessions(current_date, batch_data):
    weekday = weekday_dict[current_date.weekday()].lower()
    current_day_data = batch_data[batch_data['Day'] == weekday]
    ccc_sessions = []
    for i, row in current_day_data.iterrows():
        ccc_session = {}
        ccc_session['title'] = row['Batch']
        ccc_session['start'] = current_date.strftime("%Y-%m-%d") + 'T' + row['Time'][0].strftime("%H:%M:%S")
        ccc_session['end'] = current_date.strftime("%Y-%m-%d") + 'T' + row['Time'][1].strftime("%H:%M:%S")
        ccc_session['resourceId'] = row['Batch Start Date'].strftime('%Y - %b') #"Batches started in " + row['Batch Start Date'].strftime('%b-%y')
        ccc_sessions.append(ccc_session)
    return ccc_sessions

t =    {
        "title": "Event 1",
        "start": "2025-08-12T08:30:00",
        "end": "2025-08-12T09:30:00",
        "resourceId": "a",
    }
performance_sheet_url = 'https://docs.google.com/spreadsheets/d/1jBECVkn6T62HMZIEO8sNiw8hJdA0EV7LT7UYwNjYX6k/export?format=csv&gid=1110936940'
coach_data = pd.read_csv("https://docs.google.com/spreadsheets/d/1xiHrVfM0sWgXr8PaXMHTh-yD-iCmyvUvC3HGQ-gEdh4/export?format=csv&gid=0")

batch_data_raw = pd.read_csv(performance_sheet_url, skiprows = 1)
batch_data_raw = batch_data_raw[batch_data_raw['Batch Name'].notnull()]
batch_data_raw = batch_data_raw[batch_data_raw['Batch close date'].isnull()]
batch_data_raw = batch_data_raw[~batch_data_raw['Batch Name'].str.contains('Summer')]
batch_data_raw = batch_data_raw[['Batch Name','Days', 'Time - Day 1', 'Time - Day 2', 'Batch start date']]
batch_data_raw['Batch Name'] = batch_data_raw['Batch Name'].str.upper()
batch_data_raw.dropna(inplace = True)
#melted_batch_data_raw = batch_data_raw.melt(id_vars = )
batch_data_raw['Time - Day 1'] = batch_data_raw['Time - Day 1'].apply(get_time_duration)
batch_data_raw['Time - Day 2'] = batch_data_raw['Time - Day 2'].apply(get_time_duration)
batch_data_raw['Day 1'] = batch_data_raw['Days'].str.split(',').str[0].apply(lambda x: x.strip())
batch_data_raw['Day 2'] = batch_data_raw['Days'].str.split(',').str[1].apply(lambda x: x.strip())

batch_data_1 = batch_data_raw[['Batch Name','Day 1','Time - Day 1','Batch start date']]
batch_data_1.columns = ['Batch','Day','Time','Batch Start Date']
batch_data_2 = batch_data_raw[['Batch Name','Day 2','Time - Day 2','Batch start date']]
batch_data_2.columns = ['Batch','Day','Time','Batch Start Date']
batch_data = pd.concat([batch_data_1, batch_data_2], ignore_index = True)
batch_data['Batch Start Date'] = pd.to_datetime(batch_data['Batch Start Date'], format = '%m/%d/%Y')
batch_data['Day'] = batch_data['Day'].str.lower()

time_now = dt.datetime.now()
batch_data = batch_data[batch_data['Batch Start Date'] <= time_now]
calendar_dates = [time_now.date() + dt.timedelta(days = i - 7) for i in range(14)]

ccc_calendar_events = [create_ccc_sessions(current_date, batch_data) for current_date in calendar_dates]
ccc_calendar_events = [ccc_session for ccc_sessions in ccc_calendar_events for ccc_session in ccc_sessions]
month_start_dates = sorted(batch_data['Batch Start Date'].apply(lambda x: x.replace(day = 1)).unique(), reverse = True)
batch_resource_ids = [pd.Timestamp(x).strftime('%Y - %b') for x in month_start_dates]

ccc_calendar_options = {
    "editable": True,
    "selectable": True,
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "" #"resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
    },
    "nowIndicator": True,
    "height": "640px",
    #'contentHeight': "auto",
    "aspectRatio": 1,
    "slotMinTime": "16:00:00",
    "slotMaxTime": "22:00:00",
    "initialView": "resourceTimelineDay",
    "resourceGroupField": "building",
    "resourceOrder": "order",
    "resources": [
        {"id": resource_id, "building": "Batches Started in", "title": resource_id, "order": i} for i, resource_id in enumerate(batch_resource_ids)
    ],
}

calendar_events = [
    {
        "title": "Event 1",
        "start": "2025-08-12T20:30:00",
        "end": "2025-08-12T21:30:00",
        "resourceId": "2025-08",
    },
    {
        "title": "Event 2",
        "start": "2025-08-12T19:30:00",
        "end": "2025-08-12T21:30:00",
        "resourceId": "2025-08",
    },
    {
        "title": "Event 3",
        "start": "2025-08-12T10:40:00",
        "end": "2025-08-12T12:30:00",
        "resourceId": "b",
    }
]

calendar_options = {
    "editable": True,
    "selectable": True,
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
    },
    "height": "640px",
    "aspectRatio": 1,
    "slotMinTime": "06:00:00",
    "slotMaxTime": "22:00:00",
    "initialView": "resourceTimelineDay",
    "resourceGroupField": "building",
    "resources": [
        {"id": "a", "building": "Building A", "title": "Sub Building A"},
        {"id": "b", "building": "Building A", "title": "Sub Building B"},
        {"id": "2025-08", "building": "Building B", "title": "Sub Building C"},
        {"id": "d", "building": "Building B", "title": "Sub Building D"},
        {"id": "e", "building": "Building C", "title": "Sub Building E"},
        {"id": "f", "building": "Building C", "title": "Sub Building F"},
    ],
}

custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
"""
st.markdown("<h2 style='text-align: center; font-weight: bold;'>Chennai Chess Club Batch Monitoring</h2>", unsafe_allow_html=True)

calendar = calendar(
    events = ccc_calendar_events,
    options = ccc_calendar_options,
    custom_css = custom_css,
    key='calendar', # Assign a widget key to prevent state loss
    )

# =============================================================================
# if calendar and "eventClick" in calendar:
#     clicked_event = calendar["eventClick"]["event"]
#     st.markdown("### Event Details")
#     st.write("**Title:**", clicked_event["title"])
#     st.write("**Start:**", clicked_event["start"])
#     st.write("**End:**", clicked_event["end"])
# 
#     props = clicked_event.get("extendedProps", {})
#     st.write("**Coach:**", props.get("coach"))
#     st.write("**Level:**", props.get("level"))
#     st.write("**Location:**", props.get("location"))
# else:
#     st.info("Click on an event to view details here.")
# =============================================================================

#st.write(calendar)
