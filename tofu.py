#!/usr/bin/env python

"""
Script used to generate synthetic data for UK Biobank.
"""

import pandas as pd
from tqdm import tqdm
import numpy as np
import argparse
import helpers


def jitter_type(x):
    x = int(x)
    if x < 0 or x >= 100:
        raise argparse.ArgumentTypeError("Jitter value must be >0 and <100")
    return x


parser = argparse.ArgumentParser(
    description='Generate synthetic UK Biobank baseline data.')

parser.add_argument('-f', '--field', type=int, nargs='*',
                    help="specify one or more field ids to use")

parser.add_argument('-n', type=int, default=10,
                    help="specify numbet of patients to generate")

parser.add_argument('-v', '--verbose', action='store_true',
                    help="be verbose")

parser.add_argument('-j', '--jitter', type=jitter_type, default=0,
                    help="jitter percentage for missingness")

parser.add_argument('-o', '--out', type=str,
                    default=helpers.gen_output_filename(),
                    help="specify output file, defaults to timestamped file.")

parser.add_argument('-H', '--human', action='store_true',
                    help="decode values into human readable format")

args = parser.parse_args()

if args.verbose:
    print(args)

TOTAL_PATIENTS = args.n

if __name__ == '__main__':

    df_output = pd.DataFrame()
    df_output['eid'] = helpers.gen_fake_ids(TOTAL_PATIENTS)

    # User has supplied field list
    if args.field is not None:
        all_field_ids = helpers.get_field_ids()
        fields_to_process = set(all_field_ids).intersection(set(args.field))
        assert len(fields_to_process) > 0, "Fields not found in lookup file."
    else:
        fields_to_process = helpers.get_field_ids()

    for field_id in tqdm(fields_to_process):
        r = helpers.get_field_metadata(field_id)

        if args.verbose is True:
            print(r)

        field_title = r['title']
        field_data_type = r['value_type']
        field_encoding_id = r['encoding_id']

        # Check if a field is instanced
        # i.e. it has been collected at different
        # recruitment instances.
        field_instance_max = r.get('instance_max')
        if field_instance_max == 0:
            field_instance_max = 1

        # Check if a field is arrayed
        # i.e. there can be multiple values
        # selected for it.
        field_array_max = r.get('array_max')
        if field_array_max == 0:
            field_array_max = 1

        for i in range(field_instance_max):
            for a in range(field_array_max):

                field_canonical_name = helpers.gen_field_name(field_id, i, a, args.human)

                dummy_values = helpers.gen_dummy_data_for_field(
                                                        field_id,
                                                        TOTAL_PATIENTS)
                if args.human:
                    dummy_values = helpers.decode_values(dummy_values, field_id)

                if args.jitter > 0:
                    dummy_values = helpers.insert_missingness(
                                                            dummy_values,
                                                            args.jitter)

                df_output[field_canonical_name] = dummy_values

    df_output.to_csv(args.out, index=False)
    print("Wrote %s shape (%d,%d)." % (
                                        args.out,
                                        df_output.shape[0],
                                        df_output.shape[1]))
