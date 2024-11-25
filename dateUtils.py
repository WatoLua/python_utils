import datetime
import pytz

## date ##

def subtractMonth(date, monthCount):
    if monthCount == date.month:
        return date.replace(month=12, year=date.year - 1)
    else:
        resultYear = date.year - int(monthCount / 12)
        monthCount -= int(monthCount / 12) * 12
        if resultYear != date.year:
            return subtractMonth(date.replace(year=resultYear), monthCount)
        else:
            resultMonth = (date.month - monthCount + 12) % 12
            if resultMonth >= date.month and monthCount != 0:
                resultYear -= 1
            return date.replace(month=resultMonth, year=resultYear)


def removeTimezoneAndParseDate(dateStr, outputFormat) -> str:
    date = datetime.datetime.fromisoformat(dateStr)
    date = date.astimezone(pytz.utc).replace(tzinfo=None)
    return date.strftime(outputFormat)


def getFormattedDateNow(format="%Y-%m-%dT%H:%M:%S.f"):
    return datetime.date.today().strftime(format)
