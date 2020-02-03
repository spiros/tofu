# Tofu

[![DOI](https://zenodo.org/badge/236825382.svg)](https://zenodo.org/badge/latestdoi/236825382)

<a><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Japanese_SilkyTofu_%28Kinugoshi_Tofu%29.JPG/1920px-Japanese_SilkyTofu_%28Kinugoshi_Tofu%29.JPG" 
title="tofu" alt="tofu" width="20%" height="20%"></a>

Tofu is a Python library for generating synthetic UK Biobank data.

The [UK Biobank](https://www.ukbiobank.ac.uk/) is a large open-access prospective research cohort study 
of 500,000 middle aged participants recruited in England, Scotland and Wales. The study has collected and continues to collect extensive phenotypic and genotypic detail about its participants, including data from questionnaires, physical measures, sample assays, accelerometry, multimodal imaging, genome-wide genotyping and longitudinal follow-up for a wide range of health-related outcomes. 

Tofu will generate synthetic data which conform to the structure of the baseline data UK Biobank sends researchers by generating random values:
* For categorical variables (single or multiple choices), a random value will be picked from the UK Biobank data dictionary for that field.
* For continous variables, a random value will be generated based on the distribution of values reported for that field on the UK Biobank showcase.
* For date and date/time fields, a random date will be generated.
* For all other fields, such as polymorphic fields, no data will be generated.

Some general observations:
* The ```lookups``` directory contains lookups downloaded from the UK Biobank showcase - they might need to be updated when new fields become available.
* Data conform to the _structure_ and _schema_ of the baseline file but are otherwise nonsensical: no checks have been implemented across fields.
* All eid's (patient identifiers) generated from this tool are prefaced with 'fake' in order to avoid confusion with legitimate datasets.
* Dates randomly generated are between 1910 and 1990 again to avoid confusion with real data.

You can find more information on the UK Biobank here:

* The protocol paper in [PLOS Medicine](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1001779)
* Presentations from the [UK Biobank Scientific Conference](https://www.youtube.com/watch?v=_OG9aXf-Pd0&list=PLretMgaKD12883K_GZPWzQUwDBVz5dCfM) contain a lot of information on various aspects of the dataset.
* The [UK Biobank Showcase](http://biobank.ctsu.ox.ac.uk/crystal/) contains information for each field.
* The [data dictionaries](https://biobank.ctsu.ox.ac.uk/crystal/exinfo.cgi?src=DataDictionary) contain machine-readable metadata for each field.

## Usage

Generate synthetic data for 100 patients across all baseline fields (not advised unless you really have the entire dataset):

```bash
python tofu.py -n 100
Wrote synthetic-20200128181342.csv shape (100,21946).
```

Generate synthetic data for 100 patients for fields _3_ and _20002_ 

*Note*: you do not have to specify the eid in the list of fields since all generated datasets include it by default.

```bash
python tofu.py -n 100 --field 3 20002
Wrote synthetic-20200128171143.csv shape (10,103).
```

Generate synthetic data for 100 patients for fields _3_ and _20002_ 
and make 10% of values missing.

```bash
python tofu.py -n 100 --field 3 20002 -j 10
Wrote synthetic-20200128191124.csv shape (100,103).
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Cite as

> Spiros Denaxas. (2020). spiros/tofu: Updated release for DOI (Version v1.1). Zenodo. http://doi.org/10.5281/zenodo.3634604

## License
[MIT](https://choosealicense.com/licenses/mit/)


# 

