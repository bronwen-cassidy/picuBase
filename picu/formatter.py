from datetime import datetime

from picu.models import Patient

def format_date(value):
	return datetime.strptime(value, '%d-%b-%y').strftime('%Y-%m-%d') if value else None


def format_gender(gender):
	return "F" if gender is "0" else "M"


def format_hiv(hiv):
	result = list((key for key,value in Patient.HIV_CHOICES if value.upper() == hiv.upper()))
	return "0" if not result else result[0]

def format_yes_no(value):
	return "1" if value is True else "0"

def format_boolean(value):
	return True if value is "1" else False