import csv

csv_files = [
  'data/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
  'data/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',
  'data/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
]

def read_csv(csv_file, selected_key, selection_key, ignore_keys=[]):
  with open (csv_file, newline ='') as csv_data:
    reader = csv.DictReader(csv_data)
    keys = [fieldname for fieldname in reader.fieldnames if fieldname not in ignore_keys]
    values = next(v for v in reader if v[selection_key] == selected_key)
  return { k: v for k, v in values.items() if k in keys }

def transpose_row(row_dict, key_colname, value_colname):
  return [
    { '{}'.format(key_colname): k, '{}'.format(value_colname): v }
    for k, v in row_dict.items()
  ]
