#Name: Terry Felice
# Date: 01/25/2026

from time import strftime # used for current date and time

class Call:
    def __init__(self, client_id=0, customer_name="unknown", customer_phone="unknown"):
        self.client_id = client_id
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.call_date = strftime("%m/%d/%Y")
        self.call_time = strftime("%H:%M")

        #__str__ is automatically called when printing the object
    def __str__(self):
        return str(self.client_id) +", "+self.customer_name + \
        "\n\tPhone: "+ self.customer_phone + "\tDate/Time:"+ \
            self.call_date +" @ "+self.call_time