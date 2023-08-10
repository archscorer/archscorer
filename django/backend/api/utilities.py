from re import search

# Constants
# https://www.ifaa-archery.org/documents/rule-book/book-of-rules/  2021 page 61-62
LEVELS = {
    'FS-R': {'A': 450, 'B': 350},
    'FS-C': {'A': 450, 'B': 350},
    'FU': {'A': 500, 'B': 400},
    'BB-R': {'A': 400, 'B': 300},
    'BB-C': {'A': 400, 'B': 300},
    'BL': {'A': 450, 'B': 300},
    'BU': {'A': 475, 'B': 325},
    'BH-C': {'A': 375, 'B': 225},
    'BH-R': {'A': 375, 'B': 225},
    'LB': {'A': 250, 'B': 150},
    'TR': {'A': 375, 'B': 225}
}

def update_classification(classif, p_age_style, level, date_end, score):
    if level in classif[p_age_style] and (date_end - classif[p_age_style][level][-1]['date']).days <= 365:
        classif[p_age_style][level].append({'date': date_end, 'score': score})
    else:
       classif[p_age_style][level] = [{'date': date_end, 'score': score}]

def get_archer_class(archer=None, eval_date=None):
    """
    Get the classification class of an archer based on their events and scores.

    Parameters:
    - archer: The archer object containing event details.
    - eval_date: The date for evaluation.

    Returns:
    - A dictionary of classification classes.
    """
    if not eval_date:
        return None
    classification = {}
    last_event_date = None
    units = []
    for event_participation in archer.events.order_by('event__date_end'):
        # Filter out certain age groups and styles
        if event_participation.age_group in ['S', 'V', 'C']:
            continue
        if event_participation.style not in LEVELS:
            continue
        p_age_style = event_participation.age_group + '|' + event_participation.style
        if p_age_style not in classification:
            classification[p_age_style] = {}
        for scorecard in event_participation.scorecards.all():
            course_round = scorecard.round
            course = course_round.course
            score = scorecard.score
            # Filters for score validity
            if course.type == 's' or not score or not search('IFAA (Field|Hunter)', course.name) or not event_participation.event.records:
                continue
            # Update units for 'u' type courses
            if course.type == 'u':
                unit_indices = [i for i, unit in enumerate(units) if 'id' in unit and unit['id'] == course.id]
                if unit_indices:
                    index = unit_indices[0]
                    units[index]['score'] += score
                    units.pop(index)
                else:
                    units.append({'id': course.id, 'score': score})
                    continue
            # Update classification
            # see # https://www.ifaa-archery.org/documents/rule-book/book-of-rules/  2021 pages 62-63 for details
            if last_event_date and (eval_date - last_event_date).days < 730:
                if score >= LEVELS[event_participation.style]['A']:
                    update_classification(classification, p_age_style, 'A', event_participation.event.date_end, score)
                if LEVELS[event_participation.style]['A'] > score >= LEVELS[event_participation.style]['B']:
                    update_classification(classification, p_age_style, 'B', event_participation.event.date_end, score)
                if LEVELS[event_participation.style]['B'] > score > 0:
                    update_classification(classification, p_age_style, 'C', event_participation.event.date_end, score)
            last_event_date = event_participation.event.date_end
    classfication_classes = []
    for style, levels in classification.items():
        for level in ['A', 'B', 'C']:
            if level in levels and len(levels[level]) > 1:
                classfication_classes.append({'age_group': style.split('|')[0],
                                              'style': style.split('|')[1],
                                              'level': level, 
                                              'date': levels[level][-1]['date']})
                break
    return classfication_classes
