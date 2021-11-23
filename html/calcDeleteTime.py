from datetime import datetime, timedelta


def seconds_until_end_of_day():
    dt = datetime.utcnow()
    tomorrow = dt + timedelta(days=1)
    midnight = datetime(year=tomorrow.year, month=tomorrow.month,
                        day=tomorrow.day, hour=0, minute=0, second=0)

    return (midnight - datetime.utcnow()).seconds
