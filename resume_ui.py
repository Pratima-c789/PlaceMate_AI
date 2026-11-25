import hashlib
import streamlit as st
import pandas as pd
from resume_analyzer import analyze_resume, improve_section


def show_resume_analysis(resume_text):
    report = analyze_resume(resume_text)
    if report is None:
        st.warning('No readable resume content found.')
        return
    token = hashlib.sha256(resume_text.encode()).hexdigest()[:16]
    st.divider()
    st.header('📋 Smart Resume Quality Report')
    reviews = {section: improve_section(section, content) for section, content in report['section_contents'].items() if content}
    count = sum(len(r['changes']) for r in reviews.values())
    with st.container(border=True):
        a,b,c = st.columns(3)
        a.metric('Content Score', f"{report['score']}/100")
        b.metric('Word Count', report['word_count'])
        c.metric('Suggested Sentence Edits', count)
        st.progress(report['score']/100)
        if report['score'] >= 85: st.success('🌟 Strong foundation! Review the suggested edits below.')
        else: st.info('💪 Keep improving your resume one section at a time.')
        st.caption('Heuristic completeness score, not an ATS score or hiring prediction.')
    st.subheader('📑 Resume Section Analysis')
    st.dataframe(pd.DataFrame([{'Section': k, 'Status': 'Detected' if v else 'Not extracted — verify'} for k,v in report['sections'].items()]), hide_index=True, use_container_width=True)
    with st.expander('🌟 Strengths and contact checks'):
        for item in report['strengths']: st.success(item)
    with st.expander('📌 Missing details and placement guidance'):
        for item in report['improvements']: st.warning(item)
        st.write('Optional experience, certifications and achievements should only be included if genuine.')
    st.subheader('✨ Automatic Sentence-by-Sentence Review')
    st.caption('These edits use the actual extracted resume text. Review them for accuracy before using them.')
    if not count: st.info('No supported sentence patterns were flagged. This does not guarantee error-free content.')
    for section, review in reviews.items():
        if review['changes']:
            with st.expander(f"{section} — {len(review['changes'])} suggested edits", expanded=True):
                show_changes(review)
    st.subheader('✍️ Improve Your Resume Content')
    section = st.selectbox('Select a resume section', list(report['section_contents']), key=f'review_section_{token}')
    original = report['section_contents'][section]
    if not original: st.info('This section was not extracted. You can enter genuine content manually.')
    content = st.text_area('Automatically extracted content (editable)', value=original, height=180, key=f'review_content_{token}_{section}')
    if content.strip():
        review = improve_section(section, content)
        show_changes(review)
        st.markdown('**Complete improved section**')
        st.code(review['improved'], language=None, wrap_lines=True)
        st.download_button('📥 Download improved section', review['improved'], file_name='Improved_Resume_Section.txt', key=f'download_section_{token}_{section}')
        st.markdown('**What else to add and where**')
        for tip in review['tips']: st.info(tip)
    st.divider()
    report_text = f"PLACEMATE AI — RESUME REPORT\nContent score: {report['score']}/100\n\n"
    report_text += '\n'.join(report['strengths'] + report['improvements'])
    for name, review in reviews.items():
        report_text += f"\n\n{name}\n{review['improved']}\n"
        for change in review['changes']:
            report_text += f"Original: {change['original']}\nReplacement: {change['suggested']}\nReason: {change['reason']}\nWhere: {change['where']}\n"
        report_text += '\n'.join(review['tips'])
    st.download_button('📥 Download Resume Analysis Report', report_text, file_name='PlaceMate_Resume_Report.txt', key=f'download_report_{token}')
    st.caption('Rule-based editing, not a full grammar checker or generative AI rewrite. PDF extraction may miss headings or reading order.')


def show_changes(review):
    if not review['changes']:
        st.info('No automatic rewrite available for this wording. Review the suggestions below the improved section.')
    for i, item in enumerate(review['changes'], 1):
        with st.container(border=True):
            st.markdown(f'**Suggestion {i}**')
            st.markdown('**Original sentence**')
            st.warning(item['original'])
            st.markdown('**Why change it?**')
            st.write(item['reason'])
            st.markdown('**Suggested replacement**')
            st.success(item['suggested'])
            st.markdown('**Where to change**')
            st.write(item['where'])
