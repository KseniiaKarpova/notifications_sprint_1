import datetime
offset = datetime.timedelta(hours=3)

def check_now_is_valid_cron(cron: str):
    if cron == '* * * * *':
        return False

    now = datetime.datetime.now(datetime.timezone(offset, name='МСК'))
    cron = [x if x == '*' else int(x) for x in cron.split()]

    if cron[4] != '*' and now.minute % cron[4] != 0:
        return False
    elif cron[4] == '*' and now.minute != 0:
        return False
    if cron[3] != '*' and now.hour % cron[3] != 0:
        return False
    if cron[2] != '*' and now.day % cron[2] != 0:
        return False
    if cron[1] != '*' and now.month % cron[1] != 0:
        return False
    if cron[0] != '*' and now.weekday() % cron[0] != 0:
        return False

    return True
