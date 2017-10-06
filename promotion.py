class Promotion:

    def __init__(self, name, promo_type, value, start_date, end_date, detail):
        self.id = id(self)
        self.name = name
        self.promo_type = promo_type
        self.value = value
        self.startdate = start_date
        self.enddate = end_date
        self.detail = detail
    
