import csv
from datetime import datetime
from flask import render_template
import flask

csv_files = [
  'data/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
  'data/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',
  'data/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv',
  'static_data/covid19_greece_critical_cases.csv'
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

def write_to_csv(csv_file, rows, fieldnames):
  with open(csv_file, 'w', newline='') as csv_out:
    writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
      writer.writerow(row)

def combine_csvs(csv_filenames, selected_key, selection_key, ignore_keys, common_key, output_keys, csv_out_filename):
  csv_files = [
    transpose_row(
      read_csv(csv_filename, selected_key, selection_key, ignore_keys),
      common_key,output_keys[i]
    ) for i, csv_filename in enumerate(csv_filenames)
  ]
  csv_rows=[]
  for row in csv_files[0]:
    csv_row ={'{}'.format(common_key): row[common_key]}
    for k,csv_file in enumerate(csv_files):
      csv_row.update(next(
        (v for v in csv_file if v[common_key] == row[common_key]),
        { '{}'.format(output_keys[k]): '-1' }
      ))
    csv_rows.append(csv_row)
  csv_rows.sort(key=lambda row: datetime.strptime(row[common_key], '%m/%d/%y'))
  write_to_csv(csv_out_filename, csv_rows, [common_key] + output_keys)

def build_page():
  app = flask.Flask('my app')

  # Load case data
  case_data = []
  age_data = []
  gender_data = []

  total_cases = 0
  active_cases = 0
  recovered = 0
  critical = 0
  dead = 0

  total_cases_diff = 0
  active_cases_diff = 0
  recovered_diff = 0
  critical_diff = 0
  dead_diff = 0
  with open ('time_series_data_grc.csv', newline ='') as csv_data:
    reader = csv.DictReader(csv_data)
    for row in reader:
      if int(row['Confirmed Cases']) == 0 and total_cases == 0:
        continue
      r = {
        'DATE': row['Date'],
        'ACTIVE CASES': int(row['Confirmed Cases']) - int(row['Deceased Cases']) - int(row['Recovered Cases']),
        'REPORTED': int(row['Confirmed Cases']) - total_cases,
        'CRITICAL': int(row['Critical Cases']) if int(row['Critical Cases']) != -1 else critical,
        'RECOVERED': int(row['Recovered Cases']) - recovered,
        'DECEASED': int(row['Deceased Cases']) - dead
      }

      if total_cases != 0:
        total_cases_diff = int(row['Confirmed Cases']) / total_cases - 1

      if active_cases != 0:
        active_cases_diff = (int(row['Confirmed Cases']) - int(row['Deceased Cases']) - int(row['Recovered Cases'])) / active_cases - 1

      if dead != 0:
        dead_diff = int(row['Deceased Cases']) / dead - 1

      if critical != 0:
        critical_diff = int(row['Critical Cases']) / critical - 1

      if recovered != 0:
        recovered_diff = int(row['Recovered Cases']) / recovered - 1

      total_cases = int(row['Confirmed Cases'])
      active_cases = int(row['Confirmed Cases'])-int(row['Deceased Cases']) - int(row['Recovered Cases'])
      recovered = int(row['Recovered Cases'])
      critical = int(row['Critical Cases']) if int(row['Critical Cases']) != -1 else critical
      dead = int(row['Deceased Cases'])
      case_data.append(r)

  # Load age data
  with open ('static_data/covid19_greece_age_distribution.csv', newline ='') as csv_data:
    reader = csv.DictReader(csv_data)
    for row in reader:
      age_data.append(row)

  # Load gender data
  with open ('static_data/covid19_greece_cases_by_gender.csv', newline ='') as csv_data:
    reader = csv.DictReader(csv_data)
    for row in reader:
      gender_data.append({
        'Gender': row['Gender'],
        'Cases by Gender': int(float(row['Cases by Gender']) * total_cases)
      })

  with app.app_context():
    rendered = render_template('stats.html', \
      total_cases = total_cases, \
      total_cases_diff = "{:.2f}".format(total_cases_diff * 100),\
      active_cases = active_cases, \
      active_cases_diff = "{:.2f}".format(active_cases_diff * 100), \
      deceased_cases = dead, \
      deceased_cases_diff= "{:.2f}".format(dead_diff * 100), \
      recovered_cases = recovered, \
      recovered_cases_diff = "{:.2f}".format(recovered_diff * 100), \
      gender_data = gender_data, \
      age_data = age_data, \
      case_data = case_data)
    print(rendered)

combine_csvs(
  csv_files,
  'Greece',
  'Country/Region',
  ['Province/State','Country/Region','Lat','Long'],
  'Date',
  ['Confirmed Cases', 'Deceased Cases', 'Recovered Cases','Critical Cases'],
  'time_series_data_grc.csv'
)

build_page()
