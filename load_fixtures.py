from django.core.management import call_command
call_command('loaddata', 'selection_types.json', stdout=out, verbosity=0)
call_command('loaddata', 'selection_values.json', stdout=out, verbosity=0)
call_command('loaddata', 'diagnostic_codes_anszic.json', stdout=out, verbosity=0)
call_command('loaddata', 'diagnostic_codes_icd10.json', stdout=out, verbosity=0)
call_command('loaddata', 'diagnostic_codes_icd10_2.json', stdout=out, verbosity=0)