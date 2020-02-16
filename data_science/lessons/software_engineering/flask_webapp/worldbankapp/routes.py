from worldbankapp import app
from wrangling_scripts.wrangling_simple import data_wrangling
from wrangling_scripts.wrangling_multi import return_figures
# Flask automatically looks for html files in the templates folder.
from flask import render_template
import plotly.graph_objs as go
import plotly
import json

# Load and pre-process data
data = data_wrangling()

# Prepare data for visualization. Note that data is returned by data_wrangling as a list of lists
country = data[0][0]
x_val = data[0][1]
y_val = data[0][2]

# Create a line chart of the data (single-country)
# graph_one = [go.Scatter(
#     x=x_val,
#     y=y_val,
#     mode="lines",
#     name=country
# )]

# Create a line chart per country
graph_one = []
for data_tuple in data:
    graph_one.append(go.Scatter(
        x=data_tuple[1],
        y=data_tuple[2],
        mode="lines",
        name=data_tuple[0]
    ))

layout_one = dict(title="Change in Hectares Arable Land <br> per Person 1990 to 2015",
                  xaxis=dict(title="Year", autotick=False, tick0=1990, dtick=25),
                  yaxis=dict(title="Hectares"))

figures_simple = [dict(data=graph_one, layout=layout_one)]

# Plot IDs for the HTML ID tag
ids_simple = ["figure-{}".format(i) for i, _ in enumerate(figures_simple)]

# Convert the plotly figures to JSON for javascript in HTML template
figuresJSON_simple = json.dumps(figures_simple, cls=plotly.utils.PlotlyJSONEncoder)

# Multiple Figures
figures_multi = return_figures()

# plot ids for the html id tag
ids_multi = ['figure-{}'.format(i) for i, _ in enumerate(figures_multi)]

# Convert the plotly figures to JSON for javascript in html template
figuresJSON_multi = json.dumps(figures_multi, cls=plotly.utils.PlotlyJSONEncoder)


@app.route("/")
@app.route("/index")
def index():
    # Specify the HTML file to be rendered when accessing this paths
    # Send data to the frontend template by adding named parameters to render_template (Jinja template)
    return render_template("index.html", ids=ids_multi, figuresJSON=figuresJSON_multi)


@app.route("/simple_plot")
def simple_plot():
    return render_template("simple_plot.html", ids=ids_simple, figuresJSON=figuresJSON_simple)


@app.route('/table_with_stuff')
def table_with_stuff():
    return render_template('table_with_stuff.html')


@app.route('/dataset_display')
def dataset_display():
    return render_template('dataset_display.html', data_set=data)
