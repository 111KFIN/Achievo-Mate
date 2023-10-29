import streamlit as st
import sqlite3
import pandas as pd
import time
#st.set_page_config(layout="centered")
conn = sqlite3.connect("user.db")
cursor = conn.cursor()


def insert_user(username, password):
    query = "INSERT INTO users (name, pass) VALUES ( ? , ? );"
    values = (username, password)
    cursor.execute(query, values)
    conn.commit()
    return cursor.lastrowid
def task(user_id):
    query = """ CREATE TABLE IF NOT EXISTS """+"a"+str(user_id)+""" (
    TaskID INTEGER,
	TaskName	TEXT NOT NULL,
	TaskStatus	TEXT NOT NULL,
	DateLimit TEXT,
    PRIMARY KEY(TaskID AUTOINCREMENT)
    ); """
    cursor.execute(query)
def authenticate_user(username, password):
    query = "SELECT id FROM users WHERE name = ? AND pass = ?"
    values = (username, password)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result:
        return result[0]
    return None

def get_tasks(user_id):
    query = "SELECT * FROM "+"a"+str(user_id)
    cursor.execute(query)
    return cursor.fetchall()

def add_task(user_id,taskname,date):
    query = "INSERT INTO "+"a"+str(user_id)+" (TaskName,TaskStatus,DateLimit) VALUES (?,'Not Done',?)"
    values = (taskname,date)
    cursor.execute(query, values)
    conn.commit()
def u_task(user_id,tid,taskstatus):
    query = "UPDATE "+"a"+str(user_id)+" SET TaskStatus = ? WHERE TaskID = ?"
    values = (taskstatus,tid)
    cursor.execute(query, values)
    conn.commit()
def progress_s(user_id):
    query="SELECT count(TaskStatus) from "+"a"+str(user_id)+""" WHERE TaskStatus="Done" """
    cursor.execute(query)
    var1=cursor.fetchone()
    query="SELECT count(TaskStatus) from "+"a"+str(user_id)
    cursor.execute(query)
    var2=cursor.fetchone()
    if var2[0]:
        return int((var1[0]/var2[0])*100)
    return 100

st.title("Achievomate")

st.sidebar.header("User Authentication")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
if st.sidebar.button("Sign Up"):
    if username and password:
        insert_user(username, password)
        st.sidebar.success("User created successfully!")
    else:
        st.sidebar.error("Please enter a username and password.")
elif st.sidebar.button("Login"):
    user_id = authenticate_user(username, password)
    if user_id:
        st.sidebar.success("Login successful!")
        st.session_state.user_id = user_id
    else:
        st.sidebar.error("Invalid username or password.")
if "user_id" in st.session_state:
        st.subheader("Dashboard")
        selected_operation = st.selectbox("Select an operation", ("Progress", "Tasklist","Productivity" ))

        if selected_operation == "Progress":
            st.subheader("Progress")
            task(st.session_state.user_id)
            var = progress_s(st.session_state.user_id)
            st.header(str(var)+"%")
            st.progress(var)
            if var<50:
                st.subheader("Plant the seeds of today, for a harvest of success tomorrow. Your future is created by what you do today, not tomorrow.")
            st.write('''Progress is the lifeblood of our journey towards success and fulfillment. It's the force that propels us forward, pushing boundaries and unlocking our true potential. Without progress, we remain stagnant, confined to the familiar and never experiencing the exhilaration of breaking new ground. ''')



        elif selected_operation == "Tasklist":
            st.subheader("Tasklist")
            task(st.session_state.user_id)
            taska = st.text_input("Taskname")
            user_date = st.date_input("Select Deadline")
            if st.button("Add"):
                add_task(st.session_state.user_id,taska,user_date)
            tid= st.text_input("Task ID")
            status= st.selectbox("Status",("Done","Not Done"),index=None)
            if status :
                u_task(st.session_state.user_id,tid,status)
            ch=get_tasks(st.session_state.user_id)
            for i in ch:
                st.write(f"#{i[0]} - Task Name: {i[1]}, Task Status: {i[2]}, Deadline : {i[3]}")
        elif selected_operation == "Productivity":
            st.subheader("Are you productive Enough??")
            st.write('''Productivity is the cornerstone of efficiency and progress in both personal and professional realms. It encompasses the ability to prioritize tasks, manage time effectively, and achieve desired outcomes with the least amount of resources. A productive individual or team can accomplish more in a given timeframe, leading to a greater sense of accomplishment and, often, improved quality of work. Employing effective organizational strategies, harnessing motivation, and leveraging appropriate tools and technology are key components in enhancing productivity.

In the modern workplace, productivity is a critical factor in achieving success and maintaining a competitive edge. It's not merely about working harder, but also about working smarter. This involves employing strategies like setting clear goals, utilizing time management techniques, and leveraging technology to automate repetitive tasks. Additionally, fostering a positive work environment, providing opportunities for skill development, and recognizing and rewarding employees' efforts can significantly boost overall productivity within an organization.''')
            st.header("Get to Work Now")
            st.subheader("ELON MUSK")
            st.write('''Elon Musk's success can be attributed to a combination of visionary thinking, relentless determination, and a keen ability to disrupt traditional industries. Musk co-founded PayPal, which revolutionized online payments, and later founded companies like SpaceX, Tesla, Neuralink, and The Boring Company, each addressing different frontiers of technology and innovation.

SpaceX, for instance, aimed to reduce space transportation costs and eventually colonize Mars. Tesla focused on accelerating the world's transition to sustainable energy with electric vehicles. These ventures were risky, capital-intensive, and required a level of audacity that few entrepreneurs possess. However, Musk's unwavering belief in the potential of these technologies and his willingness to invest his own resources paid off.''')
            st.subheader("MARK ZUKERBERG")
            st.write