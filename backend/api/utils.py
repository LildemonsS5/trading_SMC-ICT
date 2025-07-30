from datetime import datetime
import pytz

def is_valid_session(current_time: datetime, sessions: list) -> bool:
    ny_tz = pytz.timezone('America/New_York')
    current_time_ny = current_time.astimezone(ny_tz)
    hour = current_time_ny.hour
    minute = current_time_ny.minute

    if 'London' in sessions and 3 <= hour <= 11:  # London session: 3 AM - 11 AM NY time
        return True
    if 'New York' in sessions and 8 <= hour <= 16:  # NY session: 8 AM - 4 PM NY time
        return True
    return False
