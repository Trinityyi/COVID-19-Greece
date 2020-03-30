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
    for csv_file in csv_files:
      csv_row.update(next(v for v in csv_file if v[common_key] == row[common_key]))
    csv_rows.append(csv_row)
  write_to_csv(csv_out_filename, csv_rows, [common_key] + output_keys)
  