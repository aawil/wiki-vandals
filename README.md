## Project 5: Exploration and detection of anonymous vandalism of Wikipedia

My fifth project at Metis. I started with around 730,000 anonymous edits to English Wikipedia extracted using WMF Quarry (query [here](https://quarry.wmflabs.org/query/36617)), and pulled in data from the ORES API, the Wikipedia API, and the MaxMind GeoLite2 IP geocoding database. I also added similar metadata to a 2015 list of human-labeled revisions used to train the ORES damage-probability model. 

I built my own version of a vandalism-probability scoring model, trained and validated on the 2019 machine-labeled data, and tested on the 2015 human-labeled data.

I also created a [web app](https://localvandals.herokuapp.com/) for exploring the May 2019 anonymous edits I collected.

A brief guide to the files in this directory:

* `get_damage_probs` is a script for gathering ORES damage probabilities in 50-revision batches, which are needed for the SQL data preparation.
* `p5utils.py` includes several utility functions used in the data preparation and modeling notebooks, including the ‘bad words’ regex lists partially swiped from [revscoring](https://github.com/wikimedia/revscoring/).
* `sql_data_prep_and_EDA.ipynb` prepares the data downloaded from the WMF Quarry SQL server for use in the web app and model building.
* `labeled_data_prep_and_EDA.ipynb` does the same thing for the 20k human-labeled revision set.
* `webapp_data_prep.ipynb` creates the dataframe pickles used in the [web app](https://localvandals.herokuapp.com/). 
* `vandal-app` is the bare bones of the app itself: just the `app.py`, the small `api.py`, and the `index.html` template.
* `vandal_model.ipynb` includes model building and visualization.
