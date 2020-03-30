# COVID-19-tools
A python tool for parsing novel coronavirus (COVID-19) data into a more usable CSV format

## API

#### `combine_csvs(csv_filenames, selected_key, selection_key, ignore_keys, common_key, output_keys, csv_out_filename)`

Combines the data from multiple CSV files into one, selecting a specific row, filtering out specific keys and transposing columns.

- `csv_filenames`: A list of CSV files to be combined.
- `selected_key`: The value of the key of the row to be selected.
- `selection_key`: The key use for row selection ().
- `ignore_keys`: Keys to be ignored (filtered out - e.g. 'long', 'lat' etc.).
- `common_key`: Name of the common key (columns transpose - e.g. 'date').
- `output_keys`: List of output keys (must correspond 1-to-1 to the list of filenames).
- `csv_out_filename`: The name of the output file.

As an example, we use [`main.py`](./src/main.py) to extract data for Greece.

Data sources provided by [Johns Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19/tree/a4ccce6f44b175d304ad18fb88fe479bc76b2584).
