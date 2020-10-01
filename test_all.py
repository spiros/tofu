
import helpers
import numpy as np
from pathlib import Path
import pytest


def test_fake_ids():

    n = 10
    fake_ids = helpers.gen_fake_ids(n)
    assert len(fake_ids) == 10

    for x in fake_ids:
        assert(x.startswith('fake'))


def test_field_metadata():

    expected = {'field_id': 3,
                'title': 'Verbal interview duration',
                'availability': 0,
                'stability': 0,
                'private': 0,
                'value_type': 11,
                'base_type': 0,
                'item_type': 0,
                'strata': 2,
                'instanced': 1,
                'arrayed': 0,
                'sexed': 0,
                'units': 'seconds',
                'main_category': 152,
                'encoding_id': 0,
                'instance_id': 2,
                'instance_min': 0,
                'instance_max': 3,
                'array_min': 0,
                'array_max': 0,
                'notes': 'Time taken for interview',
                'debut': '2012-01-05',
                'version': '2019-09-05',
                'num_participants': 501673,
                'item_count': 561869,
                'showcase_order': 0.0}

    assert helpers.get_field_metadata(3) == expected
    assert helpers.get_field_metadata(999999) is None


def test_get_field_ids():
    assert len(helpers.get_field_ids()) > 0


def test_dummy_data():
    diseases = helpers.gen_dummy_data_for_field(20002, 100)
    allowed_values = helpers.get_encoding_id_values(6)
    assert len(diseases) == 100

    for x in diseases:
        assert str(x) in allowed_values

    ages = helpers.gen_dummy_data_for_field(21022, 100)
    assert len(ages) == 100
    assert pytest.approx(np.median(ages), 2) == 55


def test_missing():
    a = np.random.randint(0, 100, 100).tolist()
    new_a = helpers.insert_missingness(a, 10)
    assert pytest.approx(new_a.count(np.nan), 2) == 10


def test_decoding_fields():
    diseases_encoded = ['1545', '1164', '1446']
    diseases_decoded_expected = ['neck problem/injury', 'pancreatic disease', 'anaemia']

    diseases_decoded = helpers.decode_values(diseases_encoded, 20002)
    assert diseases_decoded_expected == diseases_decoded

def test_fields_from_file():
    fields = set([31,34,21000])
    assert fields == helpers.get_fields_from_file('test/test_fields.txt')
