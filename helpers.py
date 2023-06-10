import datetime

def get_timeslots():
    today = datetime.date.today()
    current_weekday = today.weekday()

    days_ahead_tuesday = (1 - current_weekday + 7) % 7
    days_ahead_thursday = (3 - current_weekday + 7) % 7

    next_tuesday = today + datetime.timedelta(days=days_ahead_tuesday)
    next_thursday = today + datetime.timedelta(days=days_ahead_thursday)
    following_tuesday = next_tuesday + datetime.timedelta(days=7)
    following_thursday = next_thursday + datetime.timedelta(days=7)

    results = [
        {"label": f"Tuesday {next_tuesday.strftime('%Y.%m.%d')}", "value": next_tuesday},
        {"label": f"Thursday {next_thursday.strftime('%Y.%m.%d')}", "value": next_thursday},
        {"label": f"Tuesday {following_tuesday.strftime('%Y.%m.%d')}", "value": following_tuesday},
        {"label": f"Thursday {following_thursday.strftime('%Y.%m.%d')}", "value": following_thursday}
    ]

    results.sort(key=lambda x: x["value"])

    return results

