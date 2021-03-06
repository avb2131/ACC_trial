import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt 


st.write("""
# Concussion Sub-type classification
""")

st.sidebar.header('Inventory Results')

def user_input_features():
    clientnumber = st.sidebar.text_input(label='Client Number',value='1872')
    experimentID = st.sidebar.text_input(label='Experiment ID',value='AC-0008'),

    #data = {'Experiment ID':experimentID,
            #'Client Number':clientnumber} 

    #features = pd.DataFrame(data, index=[0])
    return experimentID, clientnumber

df = user_input_features()

#st.write(df)
experimentid = df[0][0]
clientnumber = df[1]
#st.write(experimentid)

dataset = pd.read_csv('ACCdatabase2.csv')
experimentids = dataset['Experiment ID'].values
combined = dataset[['Experiment ID','Headache Hx (0/1)\nno=0\nyes=1','Migrain Hx (None 0; Personal 1; Family 2; Personal and Family 3)','Pain Interference Percentile','Pain Intensity','Physical Function and Mobility Percentile','Anxiety Percentile','Depression Percentile','DHI Total', 'DHI Functional','Visual Motor Speed Composite','Reaction Time Composite Score','Memory Composite (Verbal) Score','Sleep Disturbance Percentile','Ability to Participate in Social Roles Percentile','Cognitive Function Percentile','Fatigue Percentile']]
dfnew1 = combined.loc[combined['Experiment ID'] == experimentid]
dfnew = dfnew1.drop(columns = ['Experiment ID','Headache Hx (0/1)\nno=0\nyes=1','Migrain Hx (None 0; Personal 1; Family 2; Personal and Family 3)'])
#st.write(dfnew)
#iris = datasets.load_iris()
training_dataset = pd.read_csv('fulltraining.csv')
Y = training_dataset['cluster'] 
X = training_dataset.drop(columns = ['cluster'])
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.1, random_state = 50)
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors=11)
classifier.fit(X, Y)
import joblib 
model= open("randomforest_Classifier.pkl", "rb")
knn_clf=joblib.load(model)

#y_pred = classifier.predict(X_test)
#classifier = RandomForestClassifier(n_estimators = 1000, criterion = 'entropy', random_state = 50)
#classifier.fit(X_train, Y_train)
#Y_pred = classifier.predict(X_test)

from sklearn.metrics import confusion_matrix
#cm = confusion_matrix(Y_test, y_pred)
#s = np.trace(cm)

#st.write(s)
#st.write(len(y_pred))

pred = knn_clf.predict(dfnew)
#st.write(pred)

#st.write(training_dataset.shape) 
#st.write(Y.shape)
#st.write(X.shape)

#X = iris.data
#Y = iris.target

#clf = RandomForestClassifier()
#clf.fit(X, Y)

#pred = clf.predict(df)
prediction_proba = knn_clf.predict_proba(dfnew)

test1 = np.empty(int(round(prediction_proba[0][0] * 100.)))
test1.fill(0.)

test2 = np.empty(int(round(prediction_proba[0][1] * 100.)))
test2.fill(1.)

test3 = np.empty(int(round(prediction_proba[0][2] * 100.)))
test3.fill(2.)

test4 = np.empty(int(round(prediction_proba[0][3] * 100.)))
test4.fill(3.)

test5 = np.empty(int(round(prediction_proba[0][4] * 100.)))
test5.fill(4.)


#st.write(prediction_proba[0])
#st.write(prediction_proba[0][0] * 100.)

st.header('Your Critical Areas')
counter = 0 
if dfnew['Pain Interference Percentile'].values > 50: 
    st.write('Pain')
    counter = counter + 1 

#st.write(dfnew['Physical Function and Mobility Percentile'])

if dfnew['Physical Function and Mobility Percentile'].values < 51: 
    st.write('Mobility')
    counter = counter + 1 

if dfnew['Anxiety Percentile'].values > 48 or dfnew['Depression Percentile'].values > 46: 
    st.write('Mood')
    counter = counter + 1 

if dfnew['DHI Total'].values > 17: 
    st.write('Dizziness')
    counter = counter + 1 

if dfnew['Visual Motor Speed Composite'].values < 36: 
    st.write('Visual Motor Speed')
    counter = counter + 1 

if dfnew['Reaction Time Composite Score'].values > 0.67: 
    st.write('Reaction Time')
    counter = counter + 1 

if dfnew['Sleep Disturbance Percentile'].values > 43: 
    st.write('Sleep')
    counter = counter + 1 

if dfnew['Cognitive Function Percentile'].values > 42: 
    st.write('Cognitive')
    counter = counter + 1 

if dfnew['Fatigue Percentile'].values > 48: 
    st.write('Fatigue')
    counter = counter + 1 

if dfnew['Memory Composite (Verbal) Score'].values < 80: 
    st.write('Memory')
    counter = counter + 1 
#st.write(iris.target_names)

st.header('Treatment Rx')
st.write('Based on the inventories completed and information provided, the ConcussionRx algorithm has determined you fall in the following concussion subtype:')
if pred == 0: 
    #st.write('Patient Classification: Concussion Sub-type 0')
    percentage = counter/10.0 * 100. 
    st.subheader('Severe Concussion')
    st.write('to a 96%'  + ' confidence interval.')


    st.write('This concussion type is characterized by having the following high, medium, and low critical areas')
    st.markdown(
    '''<span style="color:red">
    Highly Critical Areas: pain, mobility, mood, cognition, sleep, dizziness, fatigue 
    </span>
    ''',
    unsafe_allow_html=True
)
    st.markdown(
    '''
    <span style="color:blue">
    Medium Critical Areas: Memory,Visual Motor Speed, Reaction Time
    </span>
    ''',
    unsafe_allow_html=True
)

    st.header('Treatment recommended for this specific concussion sub-type includes:')
    st.write('Physiotherapy,occupational therapy,kinesiology, counseling, neurophysiology')
    st.write('Based on your ConcussionRX results, the following assessments are recommended:')
    st.subheader('Physiotherapy:')
    st.write('query cervical dysfunction, query occularmotor dysfunction, query vestibular dysfunction, query autonomic dysfunction')
    st.subheader('Neurophysiology:')
    st.write('query cognitive dysfunction')
    st.subheader('Counseling:')
    st.write('query emotional/mood dysfunction')
    st.subheader('Occupational therapy:')
    st.write('query ADLs function in school, work, home')
    
if pred == 1: 
    percentage = counter/10.0 * 100.
    st.subheader('Moderately Severe concussion')
    st.write('to a 96%'  + ' confidence interval.')

    st.write('This concussion type is characterized by having the following high, medium, and low critical areas')
    st.markdown(
    '''<span style="color:red">
    Highly Critical Areas: pain, mobility, sleep, memory,fatigue, dizziness 
    </span>
    ''',
    unsafe_allow_html=True
)
    st.markdown(
    '''
    <span style="color:blue">
    Medium Critical Areas: visual motor speed, reaction time, cognition, mood 
    </span>
    ''',
    unsafe_allow_html=True
)

    st.header('Treatment recommended for this specific concussion sub-type includes:')
    st.write('Physiotherapy,occupational therapy,kinesiology, counseling, neurophysiology')
    st.write('Based on your ConcussionRX results, the following assessments are recommended:')
    st.subheader('Physiotherapy:')
    st.write('query cervical dysfunction, query occularmotor dysfunction, query vestibular dysfunction, query autonomic dysfunction')
    st.subheader('Neurophysiology:')
    st.write('query cognitive dysfunction')
    st.subheader('counseling:')
    st.write('query emotional/mood dysfunction')
    st.subheader('Occupational therapy:')
    st.write('query ADLs function in school, work, home')

    
if pred == 2: 
    percentage = counter/5.0 * 100.
    st.subheader('Mild concussion')
    st.write('to a 96'  + '%  confidence interval.')
   
    st.write('This concussion type is characterized by having the following high, medium, and low critical areas')
    st.markdown(
    '''<span style="color:red">
    Highly Critical Areas: pain
    </span>
    ''',
    unsafe_allow_html=True
)
    st.markdown(
    '''
    <span style="color:blue">
    Medium Critical Areas: mobility, mood, sleep, fatigue 
    </span>
    ''',
    unsafe_allow_html=True
)

    st.header('Treatment recommended for this specific concussion sub-type includes:')
    st.write('Physiotherapy,occupational therapy,kinesiology, counseling')
    st.write('Based on your ConcussionRX results, the following assessments are recommended:')
    st.subheader('Physiotherapy:')
    st.write('query cervical dysfunction, query autonomic dysfunction')
    st.subheader('counseling:')
    st.write('query emotional/mood dysfunction')
    st.subheader('Occupational therapy:')
    st.write('query ADLs function in school, work, home')

if pred == 3: 
    percentage = counter/7.0 * 100.
    st.subheader('Moderate concussion')
    st.write('to a 96'  + '%  confidence interval.')
 
    st.write('This concussion type is characterized by having the following high, medium, and low critical areas')
    st.markdown(
    '''<span style="color:red">
    Highly Critical Areas: pain, mobility, mood, sleep, fatigue 
    </span>
    ''',
    unsafe_allow_html=True
)
    st.markdown(
    '''
    <span style="color:blue">
    Medium Critical Areas: cognition, dizziness
    </span>
    ''',
    unsafe_allow_html=True
)

    st.header('Treatment recommended for this specific concussion sub-type includes:')
    st.write('Physiotherapy,occupational therapy,kinesiology, counseling, neurophysiology')
    st.write('Based on your ConcussionRX results, the following assessments are recommended:')
    st.subheader('Physiotherapy:')
    st.write('query cervical dysfunction, query vestibular dysfunction, query autonomic dysfunction')
    st.subheader('Neurophysiology:')
    st.write('query cognitive dysfunction')
    st.subheader('counseling:')
    st.write('query emotional/mood dysfunction')
    st.subheader('Occupational therapy:')
    st.write('query ADLs function in school, work, home')

if pred == 4: 
    percentage = counter/10.0 * 100.
    st.subheader('Very Severe concussion')
    st.write('to a 96'  + '%  confidence interval.')
   
    st.write('This concussion type is characterized by having the following high, medium, and low critical areas')
    st.markdown(
    '''<span style="color:red">
    Highly Critical Areas: pain, mobility, mood, cognition, sleep, memory, visual motor speed, reaction time, dizziness,fatigue 
    </span>
    ''',
    unsafe_allow_html=True
)

    st.header('Treatment recommended for this specific concussion sub-type includes:')
    st.write('Physiotherapy,occupational therapy,kinesiology, counseling, neurophysiology')
    st.write('Based on your ConcussionRX results, the following assessments are recommended:')
    st.subheader('Physiotherapy:')
    st.write('query cervical dysfunction, query occularmotor dysfunction, query vestibular dysfunction, query autonomic dysfunction')
    st.subheader('Neurophysiology:')
    st.write('query cognitive dysfunction')
    st.subheader('counseling:')
    st.write('query emotional/mood dysfunction')
    st.subheader('Occupational therapy:')
    st.write('query ADLs function in school, work, home')



#st.write(df)

#st.subheader('Prediction')
#st.write(iris.target_names[prediction])
#st.write(pred)


st.header('Patient Summary')
#st.write(df)

st.subheader('Visual and Movement')
fig = go.Figure()

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = dfnew['Reaction Time Composite Score'].values[0],
    domain = {'row': 0, 'column': 0}))

fig.add_trace(go.Indicator(
    mode = "number+gauge+delta",
    gauge = {'shape': "bullet"},
    delta = {'reference': 30},
    value = dfnew['Visual Motor Speed Composite'].values[0],
    #domain = {'x': [0.1, 1], 'y': [0.2, 0.9]},
    title = {'text': "Visual Motor Speed", 'font': {'size': 12}},domain = {'row': 0, 'column': 1}))

fig.add_trace(go.Indicator(
    value = dfnew['DHI Total'].values[0],
    delta = {'reference': 0},
    title = {'text': "Dizziness", 'font': {'size': 12}},
    gauge = {
        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 15], 'color': 'green'},
            {'range': [15,25], 'color': 'orange'},
            {'range': [25,100], 'color': 'red'}]},
    domain = {'row': 1, 'column': 0}))

fig.add_trace(go.Indicator(
    value = dfnew['Physical Function and Mobility Percentile'].values[0],
    delta = {'reference': 0},
    title = {'text': "Physical Mobility", 'font': {'size': 12}},
    gauge = {
        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 40], 'color': 'red'},
            {'range': [40,60], 'color': 'orange'},
            {'range': [60,100], 'color': 'green'}]},
    domain = {'row': 1, 'column': 1}))



fig.update_layout(
    width = 760, 
    height = 500,
    grid = {'rows': 2, 'columns': 2, 'pattern': "independent"},
    template = {'data' : {'indicator': [{
        'title': {'text': "Reaction time "},
        'mode' : "number+delta+gauge",
        'delta' : {'reference': 0.67}}]
                         }})


st.plotly_chart(fig)

st.subheader('Pain and Sleep')
fig = go.Figure()

fig.add_trace(go.Indicator(
    value = dfnew['Pain Interference Percentile'].values[0],
    delta = {'reference': 0},
    title = {'text': "Pain", 'font': {'size': 12}},
    gauge = {
        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 40], 'color': 'green'},
            {'range': [40,60], 'color': 'orange'},
            {'range': [60,100], 'color': 'red'}]},
    domain = {'row': 0, 'column': 0}))


fig.add_trace(go.Indicator(
    value = dfnew['Sleep Disturbance Percentile'].values[0],
    delta = {'reference': 0},
    title = {'text': "Sleep Disturbance", 'font': {'size': 12}},
    gauge = {
        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 40], 'color': 'green'},
            {'range': [40,60], 'color': 'orange'},
            {'range': [60,100], 'color': 'red'}]},
    domain = {'row': 0, 'column': 1}))



fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = dfnew1['Headache Hx (0/1)\nno=0\nyes=1'].values[0],
    domain = {'row': 1, 'column': 0}))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    title = {'text': "Migraine"},
    value = dfnew1['Migrain Hx (None 0; Personal 1; Family 2; Personal and Family 3)'].values[0],
    domain = {'row': 1, 'column': 1}))




fig.update_layout(
    width = 700, 
    height = 500,
    grid = {'rows': 2, 'columns': 2, 'pattern': "independent"},
    template = {'data' : {'indicator': [{
        'title': {'text': "Headache"},
        'mode' : "number+delta+gauge",
        'delta' : {'reference': 0.0}}]
                         }})



st.plotly_chart(fig)

st.subheader('Cognitive and Memory')

fig = go.Figure()

fig.add_trace(go.Indicator(
    value = dfnew['Memory Composite (Verbal) Score'].values[0],
    delta = {'reference': 0},
    title = {'text': "Verbal Memory", 'font': {'size': 12}},
    gauge = {
        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 15], 'color': 'green'},
            {'range': [15,25], 'color': 'orange'},
            {'range': [25,100], 'color': 'red'}]},
    domain = {'row': 0, 'column': 0}))


fig.add_trace(go.Indicator(
    value = dfnew['Cognitive Function Percentile'].values[0],
    delta = {'reference': 0},
    title = {'text': "Cognitive Impairment", 'font': {'size': 14}},
    gauge = {
        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 40], 'color': 'green'},
            {'range': [40,60], 'color': 'orange'},
            {'range': [60,100], 'color': 'red'}]},
    domain = {'row': 0, 'column': 1}))


fig.update_layout(
    width = 700, 
    height = 400,
    grid = {'rows': 1, 'columns': 2, 'pattern': "independent"},
    template = {'data' : {'indicator': [{
        'title': {'text': "Speed"},
        'mode' : "number+delta+gauge",
        'delta' : {'reference': 90}}]
                         }})

st.plotly_chart(fig)

st.subheader('Mood and Activies of Daily Living')

fig = go.Figure()



fig.add_trace(go.Indicator(
    value = dfnew['Fatigue Percentile'].values[0],
    delta = {'reference': 0},
    title = {'text': "Fatigue", 'font': {'size': 12}},
    gauge = {
        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 40], 'color': 'green'},
            {'range': [40,60], 'color': 'orange'},
            {'range': [60,100], 'color': 'red'}]},
    domain = {'row': 0, 'column': 0}))



fig.add_trace(go.Indicator(
    value = dfnew['Anxiety Percentile'].values[0],
    delta = {'reference': 0},
    title = {'text': "Anxiety", 'font': {'size': 14}},
    gauge = {
        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 40], 'color': 'green'},
            {'range': [40,60], 'color': 'orange'},
            {'range': [60,100], 'color': 'red'}]},
    domain = {'row': 0, 'column': 1}))

fig.add_trace(go.Indicator(
    value = dfnew['Depression Percentile'].values[0],
    delta = {'reference': 0},
    title = {'text': "Depression", 'font': {'size': 14}},
    gauge = {
        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 40], 'color': 'green'},
            {'range': [40,60], 'color': 'orange'},
            {'range': [60,100], 'color': 'red'}]},
    domain = {'row': 1, 'column': 0}))

fig.add_trace(go.Indicator(
    value = dfnew['Ability to Participate in Social Roles Percentile'].values[0],
    delta = {'reference': 0},
    title = {'text': "Social Life", 'font': {'size': 14}},
    gauge = {
        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 40], 'color': 'red'},
            {'range': [40,60], 'color': 'orange'},
            {'range': [60,100], 'color': 'green'}]},
    domain = {'row': 1, 'column': 1}))


fig.update_layout(
    width = 700, 
    height = 600,
    grid = {'rows': 2, 'columns': 2, 'pattern': "independent"},
    template = {'data' : {'indicator': [{
        'title': {'text': "Speed"},
        'mode' : "number+delta+gauge",
        'delta' : {'reference': 90}}]
                         }})

st.plotly_chart(fig)

st.header('Patient Progress')

outcomes = pd.read_csv('OutcomeMeasures.csv')
dataset_client = outcomes.loc[outcomes['Client Number'] == clientnumber]
s = np.arange(len(dataset_client['Anxiety'].values))
newlist = dataset_client['timestamp'].values
dates = [] 
for item in newlist: 
    dates.append(item.split()[0])

mood = [] 
anxiety = dataset_client['Anxiety'].values 
depression = dataset_client['Depression'].values 

if len(anxiety) == len(depression):
    i = 0 
    while i < len(anxiety): 
        mood.append(max(anxiety[i],depression[i]))
        i = i + 1 
else: 
    print "not enough data"


sns.set()
fig, ax = plt.subplots(4,1,sharex='col',figsize=(10,10))

ax[0].scatter(s,mood)
ax[0].plot(s,mood)
ax[0].set_title('Client Number ' + clientnumber)
#ax[0].set_title('Mood')
ax[3].set_xticks(s)
ax[3].set_xticklabels(dates)
ax[3].set_xlabel('date')

ax[0].set_ylabel('Mood')

ax[1].scatter(s,dataset_client['Cognitive Function'].values)
ax[1].plot(s,dataset_client['Cognitive Function'].values)
#ax[0].set_title('Mood')
ax[1].set_ylabel('Cognitive Impairment')

ax[2].scatter(s,dataset_client['Pain Interferance'].values)
ax[2].plot(s,dataset_client['Pain Interferance'].values)
#ax[0].set_title('Mood')
ax[2].set_ylabel('Pain')

ax[3].scatter(s,dataset_client['Physical Function'].values)
ax[3].plot(s,dataset_client['Physical Function'].values)
#ax[0].set_title('Mood')
ax[3].set_ylabel('Movement')


st.write(fig)







