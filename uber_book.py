import sys
import random
from text_to_speech import speak
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

greet = 'Welcome To Uber'                          #greeting
print (greet.center(60,'*'))
speak("welcome to uber","en",save=True,file="greet.mp3")

speak("input your details for proceed further","en",save=True,file="greeting.mp3")

class User :
    """
    This is simple user class for taking user details
    """
    user_name : str = ""
    user_mobile_no : str = ""
    user_email : str = ""
    #constructor 
    def __init__(self,name:str,mob_no:str,email:str):
        self.user_name = name
        self.user_mobile_no = mob_no
        self.user_email = email
    
    def showUserDetails(self):
        print(f"Name of User = {self.user_name} \n \
                Contact No of user = {self.user_mobile_no} \n \
                Email ID of user = {self.user_email} \n \
                ")

name = input("Enter your name = ")
mob_no = input("Enter your mobile no. = ")
email = input("Enter your email address = ")

user = User(name,mob_no,email)
user.showUserDetails()

speak(f"ok {name}, these are available rotes please select your route ")

_routes = {'deccan-karvenagar':'4.2','deccan-swargate':'4.4','deccan-hadpsar':'8.7',
'deccan-nda':'7.5','swargate-katraj':'4.5','deccan-shivajinagar':'4'}

print("****Available Routes****")
list_routes = _routes.keys()
for r in list_routes:
    print(r)

speak("please enter your source and destination to proceed further")

_source = input ("Enter your pick up point = ")
_source = _source.lower()
_destination = input ("Enter dropping point = ")
_destination = _destination.lower()

route_to_find = _source + "-" + _destination

if route_to_find in _routes:
    print('--'*60)
    print(f"***entered source {_source}-{_destination}={_routes[route_to_find]} kms ***\n")
    print('--'*60)
    speak(f"selected route is {_source}-{_destination}={_routes[route_to_find]} kilometer ")
else:
    print('--'*60)
    print(f"entered route {_source}-{_destination} is not available in routes list.....plz try it with available routes.")
    print('--'*60)
    speak(f"entered route {_source}-{_destination} is not available....try with available routes")
    sys.exit()

speak("Do you want to proceed further")
choice = input('Yes/No : ')
print('--'*60)

while choice.casefold()=='yes':
    _txt = ('Select Your Ride')
    print(_txt.center(50,'*'))
    speak("select your ride from available options")

    class Ride :
        """
        This is simple class for Ride availability
        """
        def __init__(self,type,capacity,bags,rate):
            self.type = type
            self.capacity = capacity
            self.bags = bags
            self.rate = rate

        def ShowRide(self):
             print(f"You are selected {self.type} \n \
                It's passenger carrying capacity is {self.capacity} \n \
                It Has luggage carrying capacity is upto {self.bags} \n \
                Charges per kilometer will be {self.rate}")
    
   
    class UberPrime(Ride):
        pass
    class Uber(Ride):
        pass
    class Auto (Ride):
        pass
    class Bike(Ride):
        pass

    _uberPr = UberPrime('UBER PRIME','6','4','30 Rs.')
    _uberPr.ShowRide()

    _uber = Uber('UBER','4','3','25 Rs.')
    _uber.ShowRide()

    _auto = Auto('AUTO','3','2','15 Rs.')
    _auto.ShowRide()

    _bike = Bike('BIKE','1','1','10 Rs')
    _bike.ShowRide()

    print('--'*50)
    _sel_ride=input('Enter selected ride:')
    _sel_ride=_sel_ride.upper()

    rate = { 'UBER PRIME': 30,'UBER': 25,'AUTO': 15,'BIKE': 10 }

    if _sel_ride in rate:
        _base_amt = float(_routes[route_to_find]) * float(rate[_sel_ride])
        print(f'Base fare for ride will be {_base_amt} Rs. ')
        speak(f"Base fare for ride will be {int(_base_amt)} INR")
        speak("Do you want to book ride with us ....")
        chc = input('Yes/No : ')
        print('--'*50)
        print('--'*50)
        if chc.casefold() == 'yes':
            _alpha= ['MY', 'AS','RN','GH']
            i= random.randint(0,3)
            _state=(_alpha[i])
            _time = random.randint(10,40)
            _veh_num = 'MH12 ' + _state +' ' + str(random.randint(9999,9999) )
            print(f'Ride booked successfully!\n \
                Vehicle Type = {_sel_ride} \n \
                Vehicle Number = {_veh_num}\n \
                time to reach= {_time} mins')

            _cgst = _base_amt * 0.09
            _sgst = _base_amt * 0.09
            _total_fare = _base_amt + _cgst + _sgst
            print('--'*50)
            txt_2=( ' **** BILL OF RIDE***')
            print(txt_2)
            print(_total_fare)

            data = (('Customer','fare'),(name , str(_base_amt) ),(mob_no, str(_cgst )),(email ,str(_sgst) ) ,
                     ('total_amt',str(_total_fare)))
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Times", size=10)
            line_height = pdf.font_size * 3
            col_width = pdf.epw /5
            for row in data:
                for datum in row:
                    pdf.multi_cell(col_width, line_height, datum, border=1,
                            new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
                pdf.ln(line_height)
            pdf.output('uber_bill.pdf')

            fromaddr = "suryavanshibhakti743@gmail.com"
            toaddr = "bhakti9552@gmail.com"
            msg = MIMEMultipart() 
            msg['From'] = fromaddr 
            msg['To'] = toaddr
            msg['Subject'] = "Regarding bill for the ride"
            body = "Body_of_the_mail"
            msg.attach(MIMEText(body, 'plain'))
            filename = "uber_bill.pdf"
            attachment = open("D:/python_assignment/uber_bill.pdf", "rb")

            # instance of MIMEBase and named as p
            p = MIMEBase('application', 'octet-stream')

            # To change the payload into encoded form
            p.set_payload((attachment).read()) 
            encoders.encode_base64(p)   
            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(p)
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("suryavanshibhakti743@gmail.com", "dirglashpvphmvrf")
            text = msg.as_string()
            s.sendmail("suryavanshibhakti743@gmail.com", "bhakti9552@gmail.com", text)
            s.quit()
            print(f"Ride booked successfully.total bill of ride including cgst and sgst will be {int(_total_fare)}")
            speak(f"Ride booked successfully.total bill of ride including cgst and sgst will be {int(_total_fare)} \n \
            copy of the bill is sent to your registerd email ....driver will arrive shortly \n \
            THANK YOU for choosing Your ride with UBER")
            break

        elif chc.casefold()== 'No':
            print("Try available routes")
            speak("entered details are not correct.... please check details once ..")
        print('Exit from uber')
        speak('EXIT')
        break

            





