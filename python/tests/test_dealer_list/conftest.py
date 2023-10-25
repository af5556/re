import os
import pathlib
import pandas as pd
import pkg_resources
from typing import Dict
from pytest import fixture


@fixture()
def test_resources() -> pathlib.PurePath:
    """Absolute path to test resources"""
    return pathlib.PurePath(
        pkg_resources.resource_filename(
            "tests", "test_deaLer_list/resources"
        )
    )


class MockedRequestMock:
    def __init__(self, request_dict: Dict):
        self.request_dict = request_dict

    def get_json(self):
        return self.request_dict


class BQQueryMock:
    def __init__(self, query_output: pd.DataFrame):
        self.query_output = query_output

    def to_dataframe(self):
        return self.query_output

    def result(self):
        pass


class BQClientMock:
    def __init__(self, data: pd.DataFrame, mocked_output_path: pathlib.Path):
        self.data = data
        self.mocked_output_path = mocked_output_path

    def query(self, _: str) -> BQQueryMock:
        return BQQueryMock(query_output=self.data)

    def load_table_from_dataframe(self, dataframe: pd.DataFrame, destination):  # type: ignore
        dataframe.to_csv(
            self.mocked_output_path / "actual_output.csv",
            sep="|",
            index=False,
            header=True,
        )

    def get_table(self, table_ref):  # type: ignore
        return ""


@fixture()
def mocked_bq_client_instantiate(test_resources, tmp_path):
    def _(project: str):
        return BQClientMock(
            data=pd.read_csv(
                os.path.join(test_resources, "local_dealer_list.csv"), sep="|"
            ),
            mocked_output_path=tmp_path,
        )

    return _


@fixture()
def mocked_request():
    return MockedRequestMock(
        request_dict={
            "project": "test_project",
            "file_path": "test_file_path",
            "dealer_lists": "test_dealer_list",
           "output_table": "test_project.test_dataset.test_output_table",
        }
    )
