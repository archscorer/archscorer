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

def update_classification(eval_date, classif, p_age_style, level, date_end, score):
    classif[p_age_style]['count'] += 1
    if classif[p_age_style]['count'] > 3 and (eval_date - date_end).days > 365:
        return
    # this list of events could potentially be passed with the return value
    # print(p_age_style, classif[p_age_style]['count'], level, date_end, score)
    if level in classif[p_age_style] and (classif[p_age_style][level][-1]['date'] - date_end).days <= 365:
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
    for event_participation in archer.events.order_by('-event__date_end'):
        # Filter out events that are too old, or newer than eval_date
        date_delta = (eval_date - event_participation.event.date_end).days
        if date_delta < 0 or date_delta > 730:
            continue
        # Filter out certain age groups and styles
        if event_participation.age_group in ['S', 'V', 'C']:
            continue
        if event_participation.style not in LEVELS:
            continue
        p_age_style = event_participation.age_group + '|' + event_participation.style
        if p_age_style not in classification:
            classification[p_age_style] = {'count': 0}
        event_round_scores = []
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
            event_round_scores.append(score)
        for score in event_round_scores[::-1]:
            # Update classification
            # see # https://www.ifaa-archery.org/documents/rule-book/book-of-rules/  2021 pages 62-63 for details
            if score >= LEVELS[event_participation.style]['A']:
                update_classification(eval_date, classification, p_age_style, 'A', event_participation.event.date_end, score)
            elif LEVELS[event_participation.style]['A'] > score >= LEVELS[event_participation.style]['B']:
                update_classification(eval_date, classification, p_age_style, 'B', event_participation.event.date_end, score)
            elif LEVELS[event_participation.style]['B'] > score > 0:
                update_classification(eval_date, classification, p_age_style, 'C', event_participation.event.date_end, score)
    classfication_classes = []
    for style, levels in classification.items():
        not_within_365 = {}
        for level in ['A', 'B', 'C']:
            if level in levels and len(levels[level]) > 1:
                valid_for = 730 - (eval_date - levels[level][1]['date']).days
                # if levels[level][-2]['date'] is within 365 days of eval_date, then use as current level
                # if not, then store if not already stored and use as current level if not defined otherwise
                if (eval_date - levels[level][1]['date']).days <= 365:
                    classfication_classes.append({'age_group': style.split('|')[0],
                                                  'style': style.split('|')[1],
                                                  'level': level, 
                                                  'date': levels[level][0]['date'],
                                                  'valid_for': valid_for})
                    break
                elif not not_within_365:
                    not_within_365 = {'age_group': style.split('|')[0],
                                  'style': style.split('|')[1],
                                  'level': level, 
                                  'date': levels[level][0]['date'],
                                  'valid_for': valid_for}
        else:
            if not_within_365:
                classfication_classes.append(not_within_365)
    return classfication_classes
