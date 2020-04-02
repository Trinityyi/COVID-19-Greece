# COVID-19-Greece

[![Preview](/splash.png)](https://trinityyi.github.io/COVID-19-Greece/)

A python-generated [website](https://trinityyi.github.io/COVID-19-Greece/) for visualizing the novel coronavirus (COVID-19) data for Greece.

## Data sources

Data provided by [Johns Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19/tree/a4ccce6f44b175d304ad18fb88fe479bc76b2584) and the [National Public Health Organization](https://eody.gov.gr/en/).

## Website generation

- The website is updated daily at 03:00 UTC, using GitHub actions.
- Data is pulled daily from the relevant data sources and/or updated manually.
- The `src/main.py` script combines the data in the CSV files and generates the [daily CSV report](/time_series_data_grc.csv).
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) then outputs the data and to the template and produces the [website](https://trinityyi.github.io/COVID-19-Greece/).
- [Google Charts](https://developers.google.com/chart/interactive/docs) is used for graph generation.
