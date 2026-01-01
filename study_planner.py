# Simple adaptive study planner

def generate_study_plan(topics, hours):
    # topics: list of dicts with keys:
    # name, priority (1-5), difficulty (1-5), proficiency (1-5), exam_date (YYYY-MM-DD), min_hours, max_hours
    import datetime
    plan = {}
    if not topics or hours <= 0:
        return plan
    today = datetime.date.today()
    norm_topics = []
    for t in topics:
        if isinstance(t, dict):
            name = t.get('name', str(t))
            priority = int(t.get('priority', 1))
            difficulty = int(t.get('difficulty', 1))
            proficiency = int(t.get('proficiency', 3)) # 1=weak, 5=strong
            exam_date_str = t.get('exam_date', None)
            min_hours = float(t.get('min_hours', 0))
            max_hours = float(t.get('max_hours', hours))
            # Days until exam
            if exam_date_str:
                try:
                    exam_date = datetime.datetime.strptime(exam_date_str, '%Y-%m-%d').date()
                    days_until_exam = max((exam_date - today).days, 1)
                except:
                    days_until_exam = 30
            else:
                days_until_exam = 30
        else:
            name = str(t)
            priority = 1
            difficulty = 1
            proficiency = 3
            days_until_exam = 30
            min_hours = 0
            max_hours = hours
        norm_topics.append({
            'name': name,
            'priority': priority,
            'difficulty': difficulty,
            'proficiency': proficiency,
            'days_until_exam': days_until_exam,
            'min_hours': min_hours,
            'max_hours': max_hours
        })
    # Calculate weight for each topic
    weights = []
    for t in norm_topics:
        # More hours for higher priority, higher difficulty, lower proficiency, and sooner exam
        weight = (
            t['priority'] * 1.5 +
            t['difficulty'] * 1.2 +
            (6 - t['proficiency']) * 1.2 +
            (1 / max(t['days_until_exam'], 1)) * 20
        )
        weights.append(weight)
    total_weight = sum(weights)
    for i, t in enumerate(norm_topics):
        raw_hours = hours * (weights[i] / total_weight) if total_weight > 0 else hours / len(norm_topics)
        # Apply min/max constraints
        allocated = max(t['min_hours'], min(t['max_hours'], round(raw_hours, 2)))
        plan[t['name']] = allocated
    return plan
