import re

SECTION_PATTERNS = {
    'Professional Summary': r'professional summary|summary|profile|career objective|about me|objective',
    'Education': r'education|academic qualifications|academic background',
    'Technical Skills': r'technical skills|skills|technical expertise',
    'Projects': r'projects|academic projects|personal projects|project experience',
    'Experience': r'experience|internships?|work experience|professional experience',
    'Certifications': r'certifications?|certificates|courses|training and certifications',
    'Achievements': r'achievements|awards|honors|honours|publications|research\s*(?:&|and)\s*publications|research publications',
}

def extract_sections(text):
    result = {name: '' for name in SECTION_PATTERNS}
    current = None
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        heading = next((name for name, pattern in SECTION_PATTERNS.items() if re.fullmatch(pattern + r'\s*:?', line, re.I)), None)
        if heading:
            current = heading
        elif re.fullmatch(r'languages|interests|hobbies|references|personal details|declaration', line.rstrip(':'), re.I):
            current = None
        elif current:
            result[current] += line + '\n'
    return {k: v.strip() for k, v in result.items()}

RULES = [
    (r'^I am (?:a |an )?(.+)$', lambda m: m[1][0].upper()+m[1][1:], 'Remove first-person phrasing for a concise resume style.'),
    (r'^(?:I have |I )?worked on (.+)$', lambda m: 'Contributed to '+m[1], 'The phrase is vague; state your actual contribution if you can.'),
    (r'^(?:I am a |I am |a )?hard[ -]?working (?:person|individual) and interested in learning new technologies\.?$', lambda m: 'Interested in learning new technologies and developing professional skills.', 'Replace generic self-praise with a clear learning interest.'),
    (r'^(?:I have |I )?helped (?:with|in) (.+)$', lambda m: 'Assisted with '+m[1], 'Use concise contribution-focused wording.'),
    (r'^(?:I was |was )?responsible for (.+)$', lambda m: 'Responsibilities included '+m[1], 'Remove unnecessary first-person wording; specify your actual tasks.'),
    (r'^I have knowledge (?:of|in) (.+)$', lambda m: 'Knowledge of '+m[1], 'Use concise skill-focused wording.'),
    (r'^I (developed|implemented|designed|built|created|tested|trained|evaluated|presented|completed) (.+)$', lambda m: m[1].capitalize()+' '+m[2], 'Start directly with the action verb.'),
]

def improve_section(section, content):
    changes, output, tips = [], [], []
    # Keep skill lists and factual entries intact; avoid splitting decimal numbers or URLs.
    lines = [' '.join(content.split())] if section == 'Professional Summary' else content.splitlines()
    for line in lines:
        if not line.strip():
            continue
        units = re.split(r'(?<=[.!?])\s+(?=[A-Z])', line.strip()) if section in ('Professional Summary','Projects','Experience','Achievements') else [line.strip()]
        revised = []
        for original in units:
            new = original
            if section in ('Professional Summary','Projects','Experience','Achievements'):
                for pattern, replacement, reason in [RULES[2]] + RULES[:2] + RULES[3:]:
                    match = re.fullmatch(pattern, original, re.I)
                    if match:
                        new = replacement(match)
                        if original.endswith('.') and not new.endswith('.'):
                            new += '.'
                        changes.append(dict(original=original, suggested=new, reason=reason, where=f'In {section}, replace the quoted sentence or bullet.'))
                        break
            revised.append(new)
        output.append(' '.join(revised))
    if section == 'Professional Summary':
        tips.append('Mention your target role if known. Add a real project or experience that demonstrates your skills.')
    elif section in ('Projects','Experience'):
        tips.append('Under each relevant title, specify your individual contribution, technologies used and verified results or testing methods.')
    elif section == 'Technical Skills':
        tips.append('Group existing skills by category and retain only skills you can explain in an interview.')
    elif section == 'Certifications':
        tips.append('Include the actual certificate title, issuer and completion date.')
    elif section == 'Education':
        tips.append('Verify degree, institution, graduation year and CGPA if included.')
    else:
        tips.append('Include the actual achievement, event and date where applicable.')
    return dict(changes=changes, improved='\n'.join(output), tips=tips)

def analyze_resume(text):
    if not text.strip(): return None
    contents = extract_sections(text)
    sections = {k: bool(v) for k,v in contents.items()}
    strengths, improvements = [], []
    score = 0
    contacts = {
        'email_detected': bool(re.search(r'[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}', text)),
        'phone_detected': bool(re.search(r'(?<!\d)(?:\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}(?!\d)', text)),
        'github_detected': 'github.com' in text.lower(),
        'linkedin_detected': 'linkedin.com' in text.lower(),
    }
    for (key, found), weight in zip(contacts.items(), [8,7,5,5]):
        label = key.replace('_detected','').capitalize()
        if found: score += weight; strengths.append(label+' detected.')
        else: improvements.append('Verify or add '+label+' in the contact header, if applicable.')
    for section, weight in {'Professional Summary':10,'Education':15,'Technical Skills':15,'Projects':20}.items():
        if sections[section]: score += weight; strengths.append(section+' detected.')
        else: improvements.append('Verify or clearly label '+section+'.')
    project = contents['Projects']
    actions = re.findall(r'\b(?:developed|implemented|designed|built|created|trained|evaluated|tested|deployed|optimized|integrated)\b', project, re.I)
    metrics = re.findall(r'\b\d+(?:\.\d+)?\s*%|\b\d+\s+(?:users|samples|records|images|documents|seconds|milliseconds)\b', project, re.I)
    if actions: score += 5; strengths.append('Project action verbs detected.')
    elif project: improvements.append('Clarify individual project contributions.')
    if metrics: score += 5; strengths.append('Possible numeric project outcomes detected.')
    elif project: improvements.append('Add verified project outcomes or testing methods where available.')
    for section in ('Experience','Certifications','Achievements'):
        if sections[section]: strengths.append(section+' detected.')
    count = len(text.split())
    if count < 150: improvements.append('Check whether important details are missing.')
    elif count > 1000: improvements.append('Review repetitive or less relevant content.')
    # Original weights total 95; normalize to a 100-point checklist.
    score = round(score / 95 * 100)
    rating = 'Strong content foundation' if score >= 85 else 'Good foundation - can be improved' if score >= 65 else 'Needs content improvement'
    return dict(score=score,rating=rating,sections=sections,strengths=strengths,improvements=improvements,word_count=count,action_words=list(dict.fromkeys(actions)),measurable_results=metrics,project_text=project,section_contents=contents,**contacts)
