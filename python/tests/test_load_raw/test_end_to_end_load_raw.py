"""pipeline tests"""

import os
import json

import pytest
from apache_beam.options.pipeline_options import PipelineOptions  # type: ignore

from autobiz_etl_tools.autobizetl.models.configs import GCS2BQ
from pipelines.load_raw.pipeline import LoadRawPipeline


@pytest.mark.parametrize(
    "table_name",
    [
        #        "depreciation_vr",
        "spot_spread",
        "stock_historique_monthly",
        "stock_historique_weekly",
    ],
)
def test_load_raw_pipe(
    table_name,
    tmp_path,
    mocker,
    test_resources,
    mocked_read_gcs_json,
    mocked_write_bq_table,
):
    """

    :param table_name:
    :param tmp_path:
    :param mocker:
    :param test_resources:
    :param mocked_read_gcs_json:
    :param mocked_write_bq_table:
    :return:
    """
    # mock read from gcs
    mocker.patch(
        "autobiz_etl_tools.autobizetl.gcs2bq.read_gcs_json",
        side_effect=mocked_read_gcs_json,
    )
    mocker.patch(
        "autobiz_etl_tools.autobizetl.gcs2bq.write_bq_table",
        side_effect=mocked_write_bq_table,
    )

    # get io configs examples
    with open(os.path.join(test_resources, f"{table_name}/io_configs.json")) as mp:
        etl_configs = json.load(mp)
        # add table name to each csv pattern
        table_input = etl_configs["input"][0]
        original_pattern = table_input["file_name_patterns"][0]
        table_input["file_name_patterns"] = [f"{table_name}/{original_pattern}"]
        etl_configs["input"] = [table_input]

    # get columns transform examples
    with open(
        os.path.join(
            test_resources, f"{table_name}/final_columns_transform_configs.json"
        )
    ) as mp:
        columns_transform = json.load(mp)

    pipeline_instance = LoadRawPipeline(
        etl_configs=GCS2BQ(**etl_configs),
        pipeline_options=PipelineOptions(),
        final_columns_transform_configs=columns_transform,
    )
    pipeline_instance.run()

    # compare actual and expected
    with open(tmp_path / "output-00000-of-00001.json", "r") as json_actual_output:
        with open(
            test_resources / f"{table_name}/json_expected_output.json", "r"
        ) as json_expected_output:
            expected = [json.loads(line) for line in json_expected_output.readlines()]
            actual = [json.loads(line) for line in json_actual_output.readlines()]
            for el in actual:
                assert el in expected
