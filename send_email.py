
import ssl
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from message import message
import requests


class SendEmail:

    def __init__(self):
        self.password = "yagnrbonocvwyzbu"
        self.sender = "zoebiggerman@gmail.com"

    def anniversary_items(self, lst, yrs=None):
        string = ''

        for item in lst:
            string += f'<li>{item[0]} {item[1]} {item[2]}<br>Phone Number:{item[3]}<br>Email:{item[4]}<br></li>'

        return string

    def body_maker(self, celebration, obj):
        # obj.get('title', None)
        celebrant = f"{obj['title']} {obj['firstname']}" if type(
            obj) != list else ''
        body = ''
        if celebration == 'birthday':
            body = f'''

         <body class="bg-black bg-gradient">
        <div class="row mt-5 p-5">
            <div class="row">
                <div class="col-sm-12">
    
                    <h1 >
                        Happy Birthday {celebrant}
                    </h1>
                </div>
            </div>
<div class="row ">
    <div class="col-sm-6 justify-content-center">

        <img src="https://media.giphy.com/media/g5R9dok94mrIvplmZd/giphy.gif" alt="" style="height: 400; width: 400;">
    </div>
    <div class="col-sm-6">
        <h3>{message['birthday']}</h3>
        
    </div>
</div>
        </div>
    </body>
        '''

        elif celebration == 'independence_day':
            country = f"{obj['celebrant_country']}"
            country_flag = requests.get(
                f'https://restcountries.com/v3.1/name/{country}').json()[0]['flags']['png']
            body = f'''

         <body class="bg-black bg-gradient">
        <div class="row mt-5 p-5">
            <div class="row">
                <div class="col-sm-12">
    
                    <h1 >
                        Happy Independence Day to {country}
                    </h1>
                </div>
            </div>
<div class="row ">
    <div class="col-sm-6 justify-content-center">

        <img src="{country_flag}" alt="" style="height: 400; width: 400;">
    </div>
    <div class="col-sm-6">
        <h3>{message['independence'][0]}</h3>
        
    </div>
</div>
        </div>
    </body>
        '''
        elif celebration == 'international_women_day':
            body = f'''

         <body class="bg-black bg-gradient">
        <div class="row mt-5 p-5">
            <div class="row">
                <div class="col-sm-12">
    
                    <h1 >
                        Happy international women's day
                    </h1>
                </div>
            </div>
<div class="row ">
    <div class="col-sm-6 justify-content-center">

        <img src="https://internationalwomensday.s3-us-west-2.amazonaws.com/images/2022/IWD-relationships.png" alt="" style="height: 400; width: 400;">
    </div>
    <div class="col-sm-6">
        <h3>{message['international_women_day']}</h3>
        
    </div>
</div>
        </div>
    </body>
        '''
        elif celebration == 'international_men_day':
            body = f'''

         <body class="bg-black bg-gradient">
        <div class="row mt-5 p-5">
            <div class="row">
                <div class="col-sm-12">
    
                    <h1 >
                        Happy international men's day
                    </h1>
                </div>
            </div>
<div class="row ">
    <div class="col-sm-6 justify-content-center">

        <img src="https://epa.com.ng/wp-content/uploads/2020/11/938433-international-men-s-day-735x400.jpg" alt="" style="height: 400; width: 400;">
    </div>
    <div class="col-sm-6">
        <h3>{message['international_men_day']}</h3>
        
    </div>
</div>
        </div>
    </body>
        '''
        elif celebration == 'mothers_day':
            body = f'''

         <body class="bg-black bg-gradient">
        <div class="row mt-5 p-5">
            <div class="row">
                <div class="col-sm-12">
    
                    <h1 >
                        Happy Mothers day
                    </h1>
                </div>
            </div>
<div class="row ">
    <div class="col-sm-6 justify-content-center">

        <img src="https://www.almanac.com/sites/default/files/styles/or/public/image_nodes/mothers-day-shutterstock_609887015.jpg" alt="" style="height: 400px; width: 400px;">
    </div>
    <div class="col-sm-6">
        <h3>{message['fathers_day']}</h3>
        
    </div>
</div>
        </div>
    </body>
        '''
        elif celebration == 'fathers_day':
            body = f'''

         <body class="bg-black bg-gradient">
        <div class="row mt-5 p-5">
            <div class="row">
                <div class="col-sm-12">
    
                    <h1 >
                        Happy Fathers day
                    </h1>
                </div>
            </div>
<div class="row ">
    <div class="col-sm-6 justify-content-center">

        <img src="https://wesleychoice.org/content/uploads/2020/06/fathersDay.jpg" alt="" style="height: 400px; width: 400px;">
    </div>
    <div class="col-sm-6">
        <h3>{message['fathers_day']}</h3>
        
    </div>
</div>
        </div>
    </body>
        '''
        elif celebration == 'global_family_day':
            body = f'''

         <body class="bg-black bg-gradient">
        <div class="row mt-5 p-5">
            <div class="row">
                <div class="col-sm-12">
    
                    <h1 >
                        Happy Global Family Day
                    </h1>
                </div>
            </div>
<div class="row ">
    <div class="col-sm-6 justify-content-center">

        <img src="https://img.republicworld.com/republic-prod/stories/promolarge/xhdpi/jck7dvqussz6clpr_1641021317.jpeg" alt="" style="height: 400px; width: 400px;">
    </div>
    <div class="col-sm-6">
        <h3>{message['global_family_day']}</h3>
        
    </div>
</div>
        </div>
    </body>
        '''
        elif celebration == 'engineering_day':
            body = f'''

         <body class="bg-black bg-gradient">
        <div class="row mt-5 p-5">
            <div class="row">
                <div class="col-sm-12">
    
                    <h1 >
                        Happy World Engineering Day
                    </h1>
                </div>
            </div>
<div class="row ">
    <div class="col-sm-6 justify-content-center">

        <img src="https://region8today.ieeer8.org/wp-content/uploads/sites/114/2020/03/World-Engineering-Day_Logo_CMYK-01-1200x675.png" alt="" style="height: 400px; width: 400px;">
    </div>
    <div class="col-sm-6">
        <h3>{message['engineering_day']}</h3>
        
    </div>
</div>
        </div>
    </body>
        '''
        elif celebration == 'teachers_day':
            body = f'''

         <body class="bg-black bg-gradient">
        <div class="row mt-5 p-5">
            <div class="row">
                <div class="col-sm-12">
    
                    <h1 >
                        Happy World Teacher's Day
                    </h1>
                </div>
            </div>
<div class="row ">
    <div class="col-sm-6 justify-content-center">

        <img src="https://i0.wp.com/brandspurng.com/wp-content/uploads/2021/10/teachers-day-1.jpg" alt="" style="height: 400px; width: 400px;">
    </div>
    <div class="col-sm-6">
        <h3>{message['teachers_day']}</h3>
        
    </div>
</div>
        </div>
    </body>
        '''
        elif celebration == 'computer_security_day':
            body = f'''

         <body class="bg-black bg-gradient">
        <div class="row mt-5 p-5">
            <div class="row">
                <div class="col-sm-12">
    
                    <h1 >
                        Happy World Computer Security Day
                    </h1>
                </div>
            </div>
<div class="row ">
    <div class="col-sm-6 justify-content-center">

        <img src="https://cdn.vectorstock.com/i/1000x1000/71/26/computer-security-day-vector-27267126.webp" alt="" style="height: 400px; width: 400px;">
    </div>
    <div class="col-sm-6">
        <h3>{message['computer_security_day']}</h3>
        
    </div>
</div>
        </div>
    </body>
        '''
        elif celebration == 'world_friendship_day':
            body = f'''

         <body class="bg-black bg-gradient">
        <div class="row mt-5 p-5">
            <div class="row">
                <div class="col-sm-12">
    
                    <h1 >
                        Happy World Friendship Day
                    </h1>
                </div>
            </div>
<div class="row ">
    <div class="col-sm-6 justify-content-center">

        <img src="https://calendar.wincalendar.net/img/holiday/international-friendship-day.png" alt="" style="height: 400px; width: 400px;">
    </div>
    <div class="col-sm-6">
        <h3>{message['world_friendship_day']}</h3>
        
    </div>
</div>
        </div>
    </body>
        '''
        elif celebration == 'world_african_child_day':
            body = f'''

         <body class="bg-black bg-gradient">
        <div class="row mt-5 p-5">
            <div class="row">
                <div class="col-sm-12">
    
                    <h1 >
                        Its World African Child Day
                    </h1>
                </div>
            </div>
<div class="row ">
    <div class="col-sm-6 justify-content-center">

        <img src="https://i0.wp.com/nationaldayreview.com/wp-content/uploads/2021/06/International-Day-of-African-Child.jpg" alt="" style="height: 400px; width: 400px;">
    </div>
    <div class="col-sm-6">
        <h3>{message['world_african_child_day']}</h3>
        
    </div>
</div>
        </div>
    </body>
        '''
        elif celebration == 'world_violence_elimination_against_women_day':
            body = f'''

         <body class="bg-black bg-gradient">
        <div class="row mt-5 p-5">
            <div class="row">
                <div class="col-sm-12">
    
                    <h1 >
                        Its World Human Right Day
                    </h1>
                </div>
            </div>
<div class="row ">
    <div class="col-sm-6 justify-content-center">

        <img src="https://d2v9ipibika81v.cloudfront.net/uploads/sites/256/stop-f.jpg" alt="" style="height: 400px; width: 400px;">
    </div>
    <div class="col-sm-6">
        <h3>{message['world_human_right_day']}</h3>
        
    </div>
</div>
        </div>
    </body>
        '''
        elif celebration == 'world_mother_language_day':
            body = f'''

         <body class="bg-black bg-gradient">
        <div class="row mt-5 p-5">
            <div class="row">
                <div class="col-sm-12">
    
                    <h1 >
                        Happy World Mother Language Day
                    </h1>
                </div>
            </div>
<div class="row ">
    <div class="col-sm-6 justify-content-center">

        <img src="https://blog.pearsoninternationalschools.com/wp-content/uploads/2020/01/International-Mother-Language-Day-Blog-Post-Image-1200-x-600-px-1132x600.jpg" alt="" style="height: 400px; width: 400px;">
    </div>
    <div class="col-sm-6">
        <h3>{message['world_mother_language_day']}</h3>
        
    </div>
</div>
        </div>
    </body>
        '''

        html = f'''
        <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
      </head>
      <style>h1,p,h3 {" color: white;" }</style>
        {body}
      </html>
        '''
        return html

    def send_email(self, subject, obj, types, celebration):
        html = self.body_maker(celebration, obj)
        recipient = ','.join(
            [i for i in obj]) if types == 'general' else obj['email']

        email_message = MIMEMultipart()
        email_message['From'] = self.sender
        email_message['To'] = recipient
        email_message['Subject'] = subject
        email_message.attach(MIMEText(html, "html"))
        email_string = email_message.as_string()
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender, self.password)
            server.sendmail(self.sender, recipient, email_string)


# SendEmail().send_email(
#     "to@example.com", "gafyojorda@gufum.com", "gafyojorda@gufum.com")
