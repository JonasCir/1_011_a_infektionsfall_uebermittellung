import argparse
import json
import os
import pathlib
import string
from random import randint, randrange, choice, sample, getrandbits, seed

# introduce determinism
seed(42)

last_names = ['Peters', 'Müller', 'Schulz', 'Schulze', 'Weber', 'Wagner', 'Richter', 'Klein', 'Bauer', 'Schröder',
			  'Lange', 'Winkler', 'Winter', 'Sommer', 'Schmitt', 'Schmidt', 'Berger']

male_first_names = ['Peter', 'Daniel', 'Hans', 'Franz', 'Karl', 'Tim', 'Jan', 'Jens', 'Kai', 'Ben', 'Fin', 'Matthias',
					'Christopher', 'Cornelius', 'Konrad']

female_fist_names = ['Jana', 'Lisa', 'Anna', 'Annika', 'Petra', 'Marie', 'Susanne', 'Daniela', 'Petra', 'Martina',
					 'Emma', 'Hanna', 'Olivia', 'Isabella']

genders = ['male', 'female']

# email_providers = ['t-online', 'posteo', 'gmail', 'gmx', 'web']
email_providers = ['example']

streets = [
	"Aarhusweg",
	"Im Kramersfeld"
	"Aaröstraße",
	"Haidthöhe"
	"Aarweg",
	"Schernerweg",
	"Aastwiete",
	"Abbachstraße",
	"Niekampsweg",
	"Abbendiekshof",
	"Sonnenweg",
	"Wintergasse",
	"Südweg",
	"Hauptstraße",
	"Zähringerstraße",
	"Kaiserstraße",
	"Waldstraße",
	"Steinstraße",
	"Hafenstraße",
	"Poststraße",
	"Hohenzollerstraße",
	"Eisenbahnstraße",
	"Kronenstraße",
	"Bismarckstraße",
	"Rosenstraße",
	"Tulpenweg",
	"Bückerheide",
	"Nordstraße",
	"Nordtstraße",
	"Nordufer"]

# temporarily replace possible cities for simulation
# cities = ['Berlin', 'München', 'Hamburg', 'Köln', 'Düsseldorf', 'Kiel', 'Freiburg', 'Bochum', 'Frankfurt', 'Saarbrücken']
cities = ['Saarbrücken', 'Sulzbach', 'Dudweiler', 'St. Ingbert', 'Saarlouis', 'Völklingen', 'Bous', 'Neunkirchen',
		  'Homburg', 'Kirkel', 'Heusweiler', 'Riegelsberg', 'Püttlingen', 'St. Wendel', 'Merzig']

insurance_companies = ['AOK', 'Barmer', 'Techniker Krankenkasse', 'IKK Nord', 'KNAPPSCHAFT', 'DAK Gesundheit']

symptoms = [
	'LOSS_OF_APPETITE',
	'DIFFICULTY_BREATHING',
	'SHORTNESS_OF_BREATH',
	'FEVER',
	'WEIGHT_LOSS',
	'COUGH',
	'HEADACHE',
	'MUSCLE_PAIN',
	'BACK_PAIN',
	'COLD',
	'NAUSEA',
	'LOSS_OF_SENSE_OF_SMELL_TASTE'
]

days_in_month = {
	"01": 31, "02": 28,
	"03": 31, "04": 30,
	"05": 31, "06": 30,
	"07": 31, "08": 31,
	"09": 30, "10": 31,
	"11": 30, "12": 31
}


def gen_date_of_birth():
	year = 2020 - randint(15, 95)
	m = "{:02}".format(randrange(12) + 1)

	day = randrange(days_in_month[m]) + 1
	d = "{:02}".format(day)

	return f'{year}-{m}-{d}'


def rand_num_str(len=10):
	return ''.join([str(randint(0, 10)) for _ in range(len)])


exposures = [
	'MEDICAL_HEALTH_PROFESSION',
	'MEDICAL_LABORATORY',
	'STAY_IN_MEDICAL_FACILITY',
	'CONTACT_WITH_CORONA_CASE',
	'CONTACT_WITH_CORONA_CASE_MEDICAL_FACILITY',
	'CONTACT_WITH_CORONA_CASE_PRIVATE',
	'CONTACT_WITH_CORONA_CASE_WORK',
	'CONTACT_WITH_CORONA_CASE_OTHER',
	'COMMUNITY_FACILITY',
	'COMMUNITY_FACILITY_MINORS',
]

preIllnesses = [
	'ARDS',
	'RESPIRATORY_DISEASE',
	'CHRONIC_LUNG_DISEASE',
	'DIABETES',
	'ADIPOSITAS',
	'CARDIOVASCULAR_DISEASE',
	'IMMUNODEFICIENCY',
	'CANCER',
	'LIVER_DISEASE',
	'NEUROLOGICAL_DISEASE',
	'KIDNEY_DISEASE',
	'SMOKING',
	'PREGNANCY',
	'Alzheimer',  # Custom pre illness
]


def insurance_number():
	upper_alphabet = string.ascii_uppercase
	random_letter = choice(upper_alphabet)
	number = randint(100000000, 999999999)
	return f'{random_letter}{number}'


def replace_umlauts(inp):
	return inp.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')


########################################################################################################################

def gen_person():
	gender = choice(genders)
	first_name = choice(male_first_names) if gender == 'male' else choice(female_fist_names)
	last_name = choice(last_names)

	_email = f'{first_name[0].lower()}.{last_name.lower()}@{choice(email_providers)}.de'
	email = replace_umlauts(_email)

	return {
		'lastName': last_name,
		'firstName': first_name,
		'gender': gender,
		'dateOfBirth': gen_date_of_birth(),
		'email': email,
		'phoneNumber': rand_num_str(),
		# include house number within street field
		'street': '{} {}'.format(choice(streets), randint(0, 100)),
		#		'houseNumber': randint(0, 100),
		# temporarily filter zip codes to saarland region (approximately)
		#		'zip': rand_num_str(5),
		'zip': '66{}'.format(rand_num_str(3)),
		'city': choice(cities),
		'country': 'DE',
		'insuranceCompany': choice(insurance_companies),
		'insuranceMembershipNumber': insurance_number(),
		'fluImmunization': bool(getrandbits(1)),
		'speedOfSymptomsOutbreak': choice(['Langsam', 'Mittel', 'Schnell']),
		'symptoms': sample(symptoms, randint(0, len(symptoms))),
		'coronaContacts': bool(getrandbits(1)),
		'riskAreas': [choice(exposures)] if randint(0, 4) > 1 else [],
		'weakenedImmuneSystem': bool(getrandbits(1)),
		'preIllnesses': [choice(preIllnesses)] if randint(0, 4) > 1 else [],
		'nationality': 'deutsch'
	}


def main():
	argparser = argparse.ArgumentParser(description='Generate test patients for IMIS.')
	argparser.add_argument('-u', '--update', action='store_true',
		help='Only overwrite files if this script changed since last generation')
	argparser.add_argument('amount', nargs='?', type=int, default=250,
		help='Amount of patients to generate')

	args = argparser.parse_args()
	pathlib.Path('persons').mkdir(parents=True, exist_ok=True)


	# Check time of last update of this script
	script_last_modified = os.stat(__file__).st_mtime

	skipped_count = 0
	for i in range(args.amount):
		filename = f'persons/person{i}.json'

		# Check whether the file needs to be created / overwritten
		write_file = not args.update
		try:
			write_file = write_file or os.stat(filename).st_mtime < script_last_modified
		except FileNotFoundError as e:
			write_file = True

		# Always generate patient so that determinism is preserved
		patient = gen_person()

		if write_file:
			print(f'Writing patient data to file `{filename}`')
			with open(filename, 'w+') as f:
				f.write(json.dumps(patient, sort_keys=True, indent=2))
		else:
			skipped_count += 1

	print()
	print('=================================================')
	print()

	if skipped_count == 0:
		print(f'{args.amount} patient files written, none skipped')
	elif skipped_count == args.amount:
		print(f'All patient files already up-to-date')
	else:
		print(f'{args.amount - skipped_count} patient files written, {skipped_count} skipped')


if __name__ == '__main__':
	main()
