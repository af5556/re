"""tests for the dealer_list cloud fucntion"""

import pandas as pd
from pandas.testing import assert_frame_equal
from functions.dealer_list.main import main
import pytest


#@pytest.mark.parametrize(
#     "output_table",
#     [
#         "volvo",
#     ],
#)
def test_function_main(
    test_resources, tmp_path, mocker, mocked_bq_client_instantiate, mocked_request
):
    """Test the main function of dealer_list"""
    mocker.patch(
        "functions.dealer_list.main.Client",
        side_effect=mocked_bq_client_instantiate,
    )
    # mock request
    main(request=mocked_request)

    # get expected and actual outputs to compare
    expected_dataframe = pd.read_csv(test_resources / "expected_output.csv", sep="|")
    actual_dataframe = pd.read_csv(tmp_path / "actual_output.csv", sep="|")

    assert_frame_equal(expected_dataframe, actual_dataframe)
