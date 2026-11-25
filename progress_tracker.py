import streamlit as st
from datetime import date
import json

DEFAULT_AREAS = ['Quantitative Aptitude', 'Logical Reasoning', 'English and Verbal Ability', 'Programming and Coding', 'Computer Science Fundamentals', 'Technical Interview', 'HR Interview']

def show_progress():
    st.header('📈 Placement Progress Tracker')
    st.write('Track your preparation and celebrate every milestone.')
    areas = st.session_state.get('preparation_areas') or DEFAULT_AREAS
    areas = list(dict.fromkeys(str(a) for a in areas))
    completed = st.session_state.setdefault('tracker_completed', {})
    for area in areas:
        completed.setdefault(area, False)
    done = sum(bool(completed[a]) for a in areas)
    percent = round(100 * done / len(areas))
    a,b,c = st.columns(3)
    a.metric('Preparation Progress', f'{percent}%')
    b.metric('Completed Areas', done)
    c.metric('Remaining Areas', len(areas)-done)
    st.progress(percent/100)
    if percent == 100:
        st.success('🏆 Preparation Champion! You completed your checklist. Keep practising!')
    elif percent >= 50:
        st.success('🌟 Great progress! You are halfway there or beyond.')
    else:
        st.info('🚀 Every completed task brings you closer to your goal.')
    st.subheader('📚 Your Preparation Checklist')
    def update(area, key):
        completed[area] = st.session_state[key]
    for area in areas:
        key = 'tracker_check_' + area
        if key not in st.session_state:
            st.session_state[key] = completed[area]
        st.checkbox(area, key=key, on_change=update, args=(area,key))
    st.subheader('🎯 Practice Log')
    logs = st.session_state.setdefault('tracker_logs', [])
    with st.form('tracker_log_form', clear_on_submit=True):
        subject = st.selectbox('Practice area', areas)
        kind = st.selectbox('Activity', ['Mock Assessment','Interview Practice','Revision'])
        minutes = st.number_input('Minutes practised', min_value=1, max_value=600, value=30)
        score = st.number_input('Self-reported score (%)', min_value=0, max_value=100, value=0)
        scored = st.checkbox('Include score (if applicable)')
        if st.form_submit_button('Save Practice Activity'):
            logs.append({'Date': str(date.today()), 'Area': subject, 'Activity': kind, 'Minutes': int(minutes), 'Score': int(score) if scored else None})
            st.success('👏 Activity recorded! Keep up the effort.')
    if logs:
        a,b = st.columns(2)
        a.metric('Practice Sessions', len(logs))
        b.metric('Minutes Practised', sum(x['Minutes'] for x in logs))
        st.dataframe(logs, hide_index=True)
        scores = [x['Score'] for x in logs if x['Score'] is not None]
        if scores:
            st.line_chart({'Practice score (%)': scores})
    else:
        st.info('Record your first practice activity to see your progress.')
    report = {'completion_percent': percent, 'checklist': {a: completed[a] for a in areas}, 'practice_log': logs}
    st.download_button('📥 Download Progress Report', json.dumps(report, indent=2), file_name='PlaceMate_Progress.json', mime='application/json')
    st.caption('Checklist completion is self-reported, not a measure of job readiness. Practice records are manual and stored only in the current Streamlit session.')
