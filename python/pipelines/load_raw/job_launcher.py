"""Job launcher for a simple pipeline that reads json files from gcs,
 transform rows and insert the result into BQ"""

import json

from google.cloud import storage
from apache_beam.options.pipeline_options import PipelineOptions  # type: ignore
from autobiz_etl_tools.autobizetl.models.configs import GCS2BQ  # type: ignore

from pipelines.load_raw.arguments_parser import arg_parse
from pipelines.load_raw.pipeline import LoadRawPipeline


def read_config_file(file_path: str) -> dict:
    """Read config file as a dict"""
    if file_path.startswith("gs://"):
        client = storage.Client()
        path_parts = file_path.replace("gs://", "").split("/")
        bucket_name = path_parts[0]
        bucket = client.get_bucket(bucket_name)
        blob = bucket.get_blob("/".join(path_parts[1:]))
        return json.loads(blob.download_as_string())
    with open(file_path, "r") as file_:
        config_dict = json.load(file_)
    return config_dict


if __name__ == "__main__":
    # Read pipeline io config from file
    known_args, pipeline_options = arg_parse()
    gcs_to_bq_configs_dict = read_config_file(known_args.gcs_to_bq_configs)
    gcs_to_bq_configs = GCS2BQ(**gcs_to_bq_configs_dict)

    # load raw should take only one input file
    if len(gcs_to_bq_configs.input) > 1:
        raise RuntimeError("load_raw pipeline only take configs with one input")

    # parse final_columns_transform_configs
    final_columns_transform_configs = None
    if known_args.final_columns_transform_configs:
        final_columns_transform_configs = read_config_file(
            known_args.final_columns_transform_configs
        )

    LoadRawPipeline(
        etl_configs=gcs_to_bq_configs,
        pipeline_options=PipelineOptions(pipeline_options),
        final_columns_transform_configs=final_columns_transform_configs,  # type: ignore
    ).run()
