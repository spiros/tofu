"""
Collection of helper functions for working with UK Biobank
data dictionaries and generating fake values for synthetic
data.
"""

import numpy as np
import pandas as pd
import datetime

MIN_DATE = pd.to_datetime('1910-01-01')
MAX_DATE = pd.to_datetime('1990-12-31')

FILE_FIELDS = "lookups/df_lkp_fields.tsv.gz"
FILE_STATS = "lookups/df_showcase_desc_stats.csv.gz"
FILE_ENCODINGS = "lookups/df_lkp_encodings.csv.gz"

DF_ENCODINGS = pd.read_csv(FILE_ENCODINGS, encoding='latin-1')
DF_STATS = pd.read_csv(FILE_STATS)
DF_FIELDS = pd.read_csv(FILE_FIELDS, sep="\t", encoding='latin-1')


def get_field_ids() -> list:
    """
    Returns a list of all field id's.

    Output
    ------
        all valid field id numbers (list)

    """

    return DF_FIELDS.field_id.values


def get_field_metadata(field_id) -> dict:
    """
    Returns a dictonary of field metadata
    stored in the fields data dictionary.

    Arguments
    ---------
        field_id : field id number (int)

    Output
    ------
        metadata for field (dict)

    """

    df = DF_FIELDS[DF_FIELDS['field_id'] == field_id]
    if len(df) == 0:
        return None
    else:
        return df.to_dict(orient='records')[0]


def gen_fake_ids(n) -> list:
    """
    Return a list of fake identifiers.

    Arguments
    ---------
        n : number of identifiers to return (int)

    Output
    ------
        fake identifiers (list)

    """

    return ["fake%d" % x for x in np.arange(1, n+1, 1)]


def get_encoding_id_values(field_encoding_id) -> list:
    """
    Returns a list of all valid values for a field
    based on the UK Biobank encodings dictionary.
    Will only return values where "selectable" is true
    as defined in the lookup file supplied by the UK
    Biobank.

    Arguments
    ---------
        field_encoding_id : encoding id number (int)

    Output
    ------
        valid values (list)

    """

    # Get all values from the lookup_dictionary
    # but limit to selectable values.
    m = (DF_ENCODINGS['encoding_id'] == field_encoding_id)
    m = m & (DF_ENCODINGS['selectable'] != 0)

    df_value_lookup = DF_ENCODINGS[m]

    # Generate N fake values
    possible_field_values = df_value_lookup['value'].values
    return possible_field_values


def gen_dummy_data_for_field(field_id, n) -> list:

    """
    Generate and return a list of fake values for a
    UK Biobank field. The function supports date,
    categorical and continuous data type fields (and
    will return an empty array in other cases, such as
    for example for fields of polymoprhic value).

    Arguments
    ----------

        field_id = UK Biobank field identifider (int)
        n = number of fake fields to be generated (int)

    Output
    -------

        List of fake values (list)

    """

    field_metadata = get_field_metadata(field_id)
    field_encoding_id = field_metadata['encoding_id']
    field_data_type = field_metadata['value_type']

    # Date (51) and time (61)
    if field_data_type in (51, 61):
        d = (MAX_DATE - MIN_DATE).days + 1
        dummy_values = MIN_DATE + pd.to_timedelta(
                                    pd.np.random.randint(d, size=n),
                                    unit='d')
        dummy_values = dummy_values.tolist()

    # Categorical single choice (21) or multiple (22)
    elif field_data_type in (21, 22):

        # Get all values from the lookup_dictionary
        possible_field_values = get_encoding_id_values(field_encoding_id)
        dummy_values = np.random.choice(possible_field_values, n).tolist()

    # Float (31) or Integer (11)
    elif field_data_type in (31, 11):

        # Lookup mean and sd
        df_entry = DF_STATS[DF_STATS['field_id'] == field_id]
        mean = 0
        sd = 1

        if df_entry.empty is False:
            mean = df_entry['mean'].values[0]
            sd = df_entry['sd'].values[0]

        # Round all floats to four digits for
        # continious measurements and to no digits
        # for integer measurements.

        dec = 4
        if field_data_type == 11:
            dec = None

        dummy_values = [
            round(x, dec) for x in np.random.normal(loc=mean, scale=sd, size=n)
        ]

    # Everything else
    else:
        # Generate an empty array
        dummy_values = np.empty(n)

    return dummy_values


def gen_field_name(field_id, i, a) -> str:
    """
    Generate field column name composed of the field id
    the instance number and the array index.

    Arguments
    ----------

        field_id = UK Biobank field identifier (int)
        i = instance id (int)
        a = array index (int)

    Output
    -------

        Field name (string)

    """

    return "%d-%d.%d" % (field_id, i, a)


def get_now() -> str:
    """
    Return current timestamp in YYYYMMDDHHMMSS format.
    """

    return datetime.datetime.today().strftime('%Y%m%d%H%M%S')


def gen_output_filename() -> str:
    """
    Return timestamped output filename.
    """

    return "synthetic-%s.csv" % get_now()


def insert_missingness(a, perc) -> list:
    """
    Replaces a percentage of items from
    the list of values with np.nan.

    Arguments
    ----------
        a = values of data (list)
        perc = % of items to be removed (float)

    Output
    -------

        Values with missingness introduced (list)

    """

    total_values = len(a)

    howmany = int(total_values * perc / 100)

    random_ind_to_empty = np.random.randint(0,
                                            total_values,
                                            howmany)
    for i in random_ind_to_empty:
        a[i] = np.nan

    return a
