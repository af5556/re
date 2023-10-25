"""configurations for the pipeline tests"""

import pathlib
import pkg_resources
from pytest import fixture

import apache_beam as beam  # type: ignore
from apache_beam.coders import coders  # type: ignore
from apache_beam import PCollection, Pipeline  # type: ignore
from apache_beam.io.filesystem import CompressionTypes  # type: ignore

from autobiz_etl_tools.beamio.reads import ReadJsonFile
from autobiz_etl_tools.beamio.writes import WriteToJson
from autobiz_etl_tools.autobizetl.models.configs import GCSFileRef, BQTableRef


@fixture()
def test_resources() -> pathlib.PurePath:
    """Absolute path to test resources"""
    return pathlib.PurePath(
        pkg_resources.resource_filename("tests", "test_load_raw/resources")
    )


@fixture()
def mocked_read_gcs_json(tmp_path, test_resources):
    """Mock the read json method"""

    def _(pipeline: Pipeline, gcs_json_ref: GCSFileRef):
        """Read json entries pointed by a json ref"""
        full_path_patterns = [
            f"{test_resources}/{f_pattern}"
            for f_pattern in gcs_json_ref.file_name_patterns
        ]
        file_patterns_pcoll = (
            pipeline
            | f"Create Files PCOLL for {gcs_json_ref.source_name}"
            >> beam.Create(full_path_patterns)
        )
        return (
            file_patterns_pcoll
            | f"Read Json File {gcs_json_ref.source_name}" >> ReadJsonFile()
        )

    return _


@fixture()
def mocked_write_bq_table(tmp_path):
    """Mock the write to bq method"""

    def _(pcoll: PCollection, table_ref: BQTableRef, write_disposition):
        (
            pcoll
            | "Write to Table"
            >> WriteToJson(
                file_path_prefix=(tmp_path / "output").as_posix(),
                file_name_suffix=".json",
                num_shards=1,
                coder=coders.ToStringCoder(),
                compression_type=CompressionTypes.AUTO,
            )
        )
        print("enf of test")

    return _
