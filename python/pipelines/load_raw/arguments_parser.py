"""argument parser for the load raw pipeline"""

import argparse


def arg_parse():
    """
    Parse input parameter

    When a dataflow flex template is called, the caller pass two types of parameters:
    - custom code parameters: These are parameters needed by the custom code of the template
     (ex. source-tables)
    - apache beam parameter: These parameters are needed by apache beam to create the pipeline
     graph and run it on Dataflow

    When a job launcher is called this method will parse the custom arguments (known_args)
    and the rest of arguments will be passed directly to the pipeline instance.

    Returns:
        known_args, pipe_args: Input parameter pass as input

    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--gcs_to_bq_configs",
        type=str,
        default=None,
        help="Files of the pipeline config",
    )
    parser.add_argument(
        "--final_columns_transform_configs",
        type=str,
        default=None,
        help="Path to the mapping config file to transform columns",
    )

    parser.add_argument(
        "--final_rows_filter_configs",
        type=str,
        default=None,
        help="Path to the filtering config file to transform rows",
    )

    known_args, pipe_args = parser.parse_known_args()
    return known_args, pipe_args
