import datetime
import random
import time
from datetime import datetime
import os

import numpy as np
import pandas as pd
import requests

from holidays import countries_independence_day, international_holidays, list_of_countries
from send_email import SendEmail

testing = SendEmail()


class Messaging:
    """
    A class representing a messaging program that goes through contact information saved in a csv file and
    checks for each contact's birthday , country's independence day and other possible holidays they
    celebrates then send them messages accordingly
    """

    def __init__(self):
        self.today = datetime.today().date()
        self.df = pd.read_csv("myFilenow.csv")
        self.df['Date of Birth'] = pd.to_datetime(
            self.df['Date of Birth'], infer_datetime_format=True)
        self.df['age'] = self.df['Date of Birth'].apply(self.age)
        self.df['age_group'] = self.df['Date of Birth'].apply(self.age_group)
        self.df['title'] = self.df.apply(self.title_add, axis=1)
        self.clean_data()
        self.df['month_and_day'] = self.df['Date of Birth'].apply(
            self.month_day)
        self.df['month'] = self.df['Date of Birth'].apply(self.month)
        self.df['Nationality'] = self.df['Nationality'].apply(
            self.change_country)
        self.df['independence_day'] = self.df['Nationality'].apply(
            self.independence_day_setter)
        self.df['continent'] = self.df['Nationality'].apply(
            self.apply_continent)
        self.df.to_csv('testing.csv')

    ############################# BIRTHDAY SECTION ##############################

    def month_day(self, new):
        current_month = new.month
        day = new.day
        month_and_day = (current_month, day)
        return month_and_day

    def age(self, dob):
        this_year = datetime.today().year
        return int(this_year - dob.year)

    @staticmethod
    def month(new):
        current_month = new.month

        return current_month

    def age_group(self, new):
        this_year = datetime.today().year
        age = this_year - new.year
        if age <= 12:
            return 'Children'
        elif 12 < age <= 17:
            return 'Teen'
        elif 17 < age <= 45:
            return 'Youth'
        elif 45 < age <= 70:
            return 'Adult'
        else:
            return "Elder"

    def title_add(self, new):

        if new.age_group == 'Children' and new.Gender == 'Male':
            return 'Master'
        elif new.age_group == 'Children' and new.Gender == 'Female':
            return 'Ms'
        elif new.age_group == 'Teen' and new.Gender == 'Male':
            return 'Master'
        elif new.age_group == 'Teen' and new.Gender == 'Female':
            return 'Miss'
        elif new.age_group == 'Youth' and new.Gender == 'Female':
            return 'Ms'
        elif new.age_group == 'Youth' and new.Gender == 'Male':
            return 'Mr'
        elif new.age_group == 'Adult' and new.Gender == 'Female':
            return 'Ms'
        elif new.age_group == 'Elder' and new.Gender == 'Female':
            return 'Ms'

        else:
            return "Mr"

    def get_continent(self):
        list_of_countries = self.df['Nationality'].unique()
        lst = []
        for country in list_of_countries:
            try:
                result = requests.get(
                    f'https://restcountries.com/v3.1/name/{country}').json()[0]['continents'][0]
                lst.append({'country': country, 'continents': result})
                time.sleep(1)
            except Exception:
                continue
        return lst

    def apply_continent(self, country):
        try:
            continent = next(
                item for item in list_of_countries if item["country"] == country)
            return continent['continents']
        except Exception:
            continent = 'unknown continent'
            return continent

    def today_birthday(self):
        '''for birthday'''

        today = datetime.today().date()
        # today = self.today
        month = today.month
        day = today.day
        celebrant_email = self.df[self.df.month_and_day == (month, day)].email
        celebrant_name = self.df[self.df.month_and_day == (
            month, day)].firstname
        celebrant_title = self.df[self.df.month_and_day == (month, day)].title
        result = list(zip(celebrant_title, celebrant_name, celebrant_email))
        return [{"title": i[0], 'firstname': i[1], 'email': i[2]} for i in result]

    ################################### INDEPENDENCE DAY SECTION ################################

    def change_country(self, country):
        '''
        Takes a country from the nationality column and changes every occurrence that can be found in the
        independence_day.py file to Nigeria
        '''

        list_of_countries = [i['Country'] for i in countries_independence_day
                             ]
        if country not in list_of_countries:
            return 'Nigeria'
        else:
            return country

    def independence_day_setter(self, nationals):

        for country in countries_independence_day:
            if country['Country'] == nationals:
                date = country['Independence Day'].split('/')
                try:
                    return (int(date[0]), int(date[1]))
                except Exception:
                    continue

    def todays_independence_day(self):

        month = self.today.month
        day = self.today.day
        celebrant_email = self.df[self.df.independence_day == (
            month, day)].email
        celebrant_name = self.df[self.df.independence_day == (
            month, day)].firstname
        celebrant_title = self.df[self.df.independence_day == (
            month, day)].title
        celebrant_country = self.df[self.df.independence_day == (
            month, day)].Nationality
        result = list(zip(celebrant_title, celebrant_name,
                          celebrant_email, celebrant_country))
        return [{"title": i[0], 'firstname': i[1], 'email': i[2], 'celebrant_country': i[3]} for i in result]

    def clean_data(self):

        self.df["profession"] = np.where(
            self.df["age_group"] == "Children", 'Student', self.df["profession"])
        self.df["profession"] = np.where(
            self.df["age_group"] == "Teen", 'Student', self.df["profession"])
        self.df["Marital_status"] = np.where(
            self.df["age_group"] == "Children", 'Single', self.df["Marital_status"])
        self.df["Marital_status"] = np.where(
            self.df["age_group"] == "Teen", 'Single', self.df["Marital_status"])
        self.df["Gender"] = np.where(
            self.df["Gender"] == "XX", random.randint(0, 1), self.df["Gender"])

    ####################################### INTERNATIONAL HOLIDAYS #################################

    def women_international_days(self):

        womens_day = next(
            item for item in international_holidays if item["Occasion"] == "International Women's Day")
        date_str = datetime.strptime(womens_day['date'], '%d/%m/%Y').date()

        if date_str == self.today:
            is_woman = self.df[self.df.eval(" Gender== 'Female'")]
            # return womens_day['date']
            celebrant_title = is_woman['title']
            firstname = is_woman['firstname']
            lastname = is_woman['lastname']
            email = is_woman['email']
            result = list(zip(celebrant_title, firstname, email))
            return [{"title": i[0], 'firstname': i[1], 'email': i[2]} for i in result]

    def Mothers_day(self):

        mothers_day = [
            item for item in international_holidays if item["Occasion"] == "Mother's Day"]

        for item in mothers_day:
            if datetime.strptime(item['date'], '%d/%m/%Y').date() == datetime.today().date():
                is_mother = self.df[self.df.eval(
                    "age >= 18 & Gender== 'Female'")]
                celebrant_title = is_mother['title']
                firstname = is_mother['firstname']
                lastname = is_mother['lastname']
                email = is_mother['email']
                result = list(zip(celebrant_title, firstname, email))
                return [{"title": i[0], 'firstname': i[1], 'email': i[2]} for i in result]

    def Fathers_day(self):

        fathers_day = [
            item for item in international_holidays if item["Occasion"] == "Father's Day"]
        for item in fathers_day:
            if datetime.strptime(item['date'], '%d/%m/%Y').date() == datetime.today().date():
                # if date_str == datetime.today().date():
                is_father = self.df[self.df.eval(
                    "age >= 18 & Gender== 'Male'")]
                celebrant_title = is_father['title']
                firstname = is_father['firstname']
                lastname = is_father['lastname']
                email = is_father['email']

                result = list(zip(celebrant_title, firstname, email))
                return [{"title": i[0], 'firstname': i[1], 'email': i[2]} for i in result]

    def men_international_days(self):
        men_day = next(
            item for item in international_holidays if item["Occasion"] == "International Men's Day")
        date_str = datetime.strptime(men_day['date'], '%d/%m/%Y').date()
        # today = datetime.datetime(2020, 4, 9)

        if date_str == datetime.today().date():
            is_man = self.df[self.df.eval("Gender== 'Male'")]
            # return womens_day['date']
            celebrant_title = is_man['title']
            firstname = is_man['firstname']
            lastname = is_man['lastname']
            email = is_man['email']
            result = list(zip(celebrant_title, firstname, email))
            return [{"title": i[0], 'firstname': i[1], 'email': i[2]} for i in result]

    def global_family_day(self):
        family_day = next(
            item for item in international_holidays if item["Occasion"] == "Global Family Day")
        today = datetime.today().date()
        date_str = datetime.strptime(family_day['date'], '%d/%m/%Y').date()
        if date_str == datetime.today().date():
            is_df = self.df[self.df.eval(
                "Gender== 'Male' | Gender== 'Female'")]

            celebrant_title = is_df["title"]
            firstname = is_df["firstname"]
            lastname = is_df["lastname"]
            email = is_df["email"]
            result = list(zip(celebrant_title, firstname, email))

            return [{"title": i[0], 'firstname': i[1], 'email': i[2]} for i in result]

    def world_engineering_day(self):
        engineering_day = next(
            item for item in international_holidays if item["Occasion"] == "IEEE Global Engineering Day")
        today = datetime.today().date()
        # today = datetime(2023, 5, 13).date()
        date_str = datetime.strptime(
            engineering_day['date'], '%d/%m/%Y').date()
        if date_str == datetime.today().date():
            is_engineer = self.df[self.df.eval("profession=='engineer'")]
            celebrant_title = is_engineer['title']
            firstname = is_engineer['firstname']
            lastname = is_engineer['lastname']
            email = is_engineer['email']
            result = list(zip(celebrant_title, firstname, email))
            return [{"title": i[0], 'firstname': i[1], 'email': i[2]} for i in result]

    def world_teachers_day(self):
        teachers_day = next(
            item for item in international_holidays if item["Occasion"] == "World Teacher's Day")
        # today = datetime(2023, 10, 5).date()
        today = datetime.today().date()
        date_str = datetime.strptime(teachers_day['date'], '%d/%m/%Y').date()

        if date_str == datetime.today().date():
            is_teacher = self.df[self.df.eval(
                "profession=='teacher' | profession=='professor'")]
            celebrant_title = is_teacher['title']
            firstname = is_teacher['firstname']
            lastname = is_teacher['lastname']
            email = is_teacher["email"]
            result = list(zip(celebrant_title, firstname, email))
            return [{"title": i[0], 'firstname': i[1], 'email': i[2]} for i in result]

    def world_computer_security_day(self):
        comp_sec_day = next(
            item for item in international_holidays if item["Occasion"] == "International Computer Security Day")
        today = datetime.today().date()
        date_str = datetime.strptime(comp_sec_day['date'], '%d/%m/%Y').date()
        if date_str == datetime.today().date():
            celebrant_title = self.df.title
            firstname = self.df.firstname
            lastname = self.df.lastname
            email = self.df.email
            result = list(zip(celebrant_title, firstname, email))
            return [{"title": i[0], 'firstname': i[1], 'email': i[2]} for i in result]

    def world_friendship_day(self):
        friendship_day = next(
            item for item in international_holidays if item["Occasion"] == "International Friendship Day")
        today = datetime.today().date()
        # today = datetime(2023, 8, 7).date()
        date_str = datetime.strptime(friendship_day['date'], '%d/%m/%Y').date()
        if date_str == datetime.today().date():
            celebrant_title = self.df.title
            firstname = self.df.firstname
            lastname = self.df.lastname
            email = self.df.email
            result = list(zip(celebrant_title, firstname, email))
            return [{"title": i[0], 'firstname': i[1], 'email': i[2]} for i in result]

    def world_african_child(self):
        african_child = next(
            item for item in international_holidays if item["Occasion"] == "International Day of the African Child")
        today = datetime(2023, 6, 19).date()
        # today = datetime.today().date()
        date_str = datetime.strptime(african_child['date'], '%d/%m/%Y').date()
        if date_str == datetime.today().date():
            is_african_child = self.df[self.df.eval(
                "continent=='Africa'")]
            celebrant_title = is_african_child.title
            firstname = is_african_child.firstname
            lastname = is_african_child.lastname
            email = self.df.email
            result = list(zip(celebrant_title, firstname, email))
            return [{"title": i[0], 'firstname': i[1], 'email': i[2]} for i in result]

    def world_human_right_day(self):
        human_right_day = next(
            item for item in international_holidays if item["Occasion"] == "Human Rights Day")
        today = datetime.today().date()
        # today = datetime(2023, 12, 10).date()
        date_str = datetime.strptime(
            human_right_day['date'], '%d/%m/%Y').date()
        if date_str == datetime.today().date():
            celebrant_title = self.df.title
            firstname = self.df.firstname
            lastname = self.df.lastname
            email = self.df.email
            result = list(zip(celebrant_title, firstname, email))
            return [{"title": i[0], 'firstname': i[1], 'email': i[2]} for i in result]

    def world_mother_language_day(self):
        mother_language_day = next(
            item for item in international_holidays if item["Occasion"] == "International Mother Language Day")
        today = datetime.today().date()
        # today = datetime(2023, 2, 21).date()
        date_str = datetime.strptime(
            mother_language_day['date'], '%d/%m/%Y').date()

        if date_str == datetime.today().date():
            celebrant_title = self.df.title
            firstname = self.df.firstname
            email = self.df.email
            result = list(zip(celebrant_title, firstname, email))
            return [{"title": i[0], 'firstname': i[1], 'email': i[2]} for i in result]

    def world_violence_elimination_against_women(self):
        women_violence_elimination_day = next(
            item for item in international_holidays if
            item["Occasion"] == "International Day for the Elimination of Violence Against Women")
        today = datetime.today().date()
        # today = datetime(2023, 11, 25).date()
        date_str = datetime.strptime(
            women_violence_elimination_day['date'], '%d/%m/%Y').date()
        if date_str == datetime.today().date():
            celebrant_title = self.df.title
            firstname = self.df.firstname
            lastname = self.df.lastname
            email = self.df.email
            result = list(zip(celebrant_title, firstname, email))
            return [{"title": i[0], 'firstname': i[1], 'email': i[2]} for i in result]

    def need_to_send(self):
        # for birthday
        todays_birthday = self.today_birthday()
        if todays_birthday is not None:
            for i in todays_birthday:
                testing.send_email(subject="Happy Birthday", obj=i,
                                   types="personal", celebration="birthday")
        # # for independence day
        independence_day = self.todays_independence_day()
        if independence_day is not None:
            for i in independence_day:
                testing.send_email(subject="Happy independence", obj=i,
                                   types="personal", celebration="independence_day")

        # for international women day
        todays_international_women = self.women_international_days()
        if todays_international_women is not None:
            emails = [i['email'] for i in todays_international_women]
            testing.send_email(subject="Happy International Women's Day", obj=emails,
                               types="general", celebration="international_women_day")
        # for international men day
        todays_international_men = self.men_international_days()
        if todays_international_men is not None:
            emails = [i['email'] for i in todays_international_women]
            testing.send_email(subject="Happy International Men's Day", obj=emails,
                               types="general", celebration="international_men_day")

        # for mothers day
        today_is_mothers_day = self.Mothers_day()
        if today_is_mothers_day is not None:
            emails = [i['email'] for i in today_is_mothers_day]
            testing.send_email(subject="Happy Mother's Day", obj=emails,
                               types="general", celebration="mothers_day")
        # for fathers day
        today_is_fathers_day = self.Fathers_day()
        if today_is_fathers_day is not None:
            emails = [i['email'] for i in today_is_fathers_day]
            testing.send_email(subject="Happy Father's Day", obj=emails,
                               types="general", celebration="fathers_day")

        today_is_global_family_day = self.global_family_day()
        if today_is_global_family_day is not None:
            emails = [i['email'] for i in today_is_global_family_day]

            testing.send_email(subject="Happy Global Family Day", obj=emails,
                               types="general", celebration="global_family_day")

        today_is_world_engineering_day = self.world_engineering_day()
        if today_is_world_engineering_day is not None:
            emails = [(i['email']) for i in today_is_world_engineering_day]
            print(emails)
            testing.send_email(subject="Happy World Engineering Day", obj=emails,
                               types="general", celebration="engineering_day")

        today_is_world_teachers_day = self.world_teachers_day()
        if today_is_world_teachers_day is not None:
            emails = [i['email'] for i in today_is_world_teachers_day]
            testing.send_email(subject="Happy World Teacher's Day", obj=emails,
                               types="general", celebration="teachers_day")

        today_is_world_computer_security_day = self.world_computer_security_day()
        if today_is_world_computer_security_day is not None:
            emails = [i['email'] for i in today_is_world_computer_security_day]
            testing.send_email(subject="Happy World Computer Security Day", obj=emails,
                               types="general", celebration="computer_security_day")

        today_is_world_friendship_day = self.world_friendship_day()
        if today_is_world_friendship_day is not None:
            emails = [i['email'] for i in today_is_world_friendship_day]
            testing.send_email(subject="Happy World Friendship Day", obj=emails,
                               types="general", celebration="world_friendship_day")

        today_is_world_african_child_day = self.world_african_child()
        if today_is_world_african_child_day is not None:
            emails = [i['email'] for i in today_is_world_african_child_day]
            testing.send_email(subject="Happy World African Child Day", obj=emails,
                               types="general", celebration="world_african_child_day")

        today_is_world_human_right_day = self.world_human_right_day()
        if today_is_world_human_right_day is not None:
            emails = [i['email'] for i in today_is_world_african_child_day]
            testing.send_email(subject="Happy World Human Rights Day", obj=emails,
                               types="general", celebration="world_human_right_day")

        today_is_world_mother_language_day = self.world_mother_language_day()
        if today_is_world_mother_language_day is not None:
            emails = [i['email'] for i in today_is_world_mother_language_day]
            testing.send_email(subject="Happy World Mother Language Day", obj=emails,
                               types="general", celebration="world_mother_language_day")

        today_is_world_violence_elimination_against_women_day = self.world_violence_elimination_against_women()
        if today_is_world_violence_elimination_against_women_day is not None:
            emails = [i['email']
                      for i in today_is_world_violence_elimination_against_women_day]
            testing.send_email(subject="Happy World Violence Elimination Against Women Day", obj=emails,
                               types="general", celebration="world_violence_elimination_against_women_day")


print(Messaging().need_to_send())
# print(requests.get(
#     'https://restcountries.com/v3.1/name/nigeria').json()[0]['flags']['png'])
