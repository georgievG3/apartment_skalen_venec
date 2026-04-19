from django.conf import settings

def get_price_for_date(date):
    quarter = (date.month - 1) // 3 + 1
    return settings.SEASONAL_PRICES[quarter]
