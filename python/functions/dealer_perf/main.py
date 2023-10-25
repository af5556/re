"""Cloud function to create from each scoring table a dealer perf table
    where we apply the needed transformations

This cloud function takes as parameters:
    project_id: id of the project where to write raw data
    dataset_id: id of the dataset where to write the raw data
    landing_bucket: bucket within the data processing project where csv files are
    table_schema: file with the schema of the table
"""

from typing import Generator, List
# import pandas as pd  # type: ignore
from google.cloud.bigquery import Client
from google.cloud.bigquery.table import TableReference
from google.cloud import storage
# import gcsfs


def generate_scoring_tables(country_list: str) -> Generator[List, None, None]:
    """
    temporary function to generate all the scoring tables in ols
    :param country_list:
    :return:
    """
    return



def main(request):
    """
    Read data from the landing bucket, and return the output table
    """
    request_json = request.get_json()
    print(request_json)
    file_path = request_json["file_path"]
    project = request_json["project"]
    output_table = request_json["output_table"]
    forced_tables = request_json["forced_tables"]


for month in scoring:
        query = """
                     SELECT
                        UPPER(SUBSTR(table_name, STRPOS(table_name, 'v'), 3)) AS CASE_1,
                        UPPER(SUBSTR(table_name, STRPOS(table_name, 'v') + 2 , 2)) AS CASE_2,
                      CASE UPPER(SUBSTR(TAB.table_name, STRPOS(TAB.table_name, 'v'), 3))
                        WHEN "VO_" THEN "EURO"
                      ELSE
                      CASE UPPER(SUBSTR(TAB.table_name, STRPOS(TAB.table_name, 'v'), 4))
                        WHEN 'VOSE' THEN 'SEK'
                        WHEN 'VOCH' THEN 'CHF'
                        WHEN 'VONO' THEN 'NOK'
                        WHEN 'VOCZ' THEN 'CZK'
                        WHEN 'VOPL' THEN 'PLN'
                    END
                    END
                      AS CURRENCY,
                    FROM (
                      SELECT
                        table_name
                      FROM
                        {table}.COLUMNS ) AS TAB
    """

    try:
        for dealer_list in dealer_lists:
            # read data
            client = Client(project=project)
            input_data = read_gcs_csv_file(f"{file_path}/{dealer_list}")

            # delete old contents of the output table
            client.query(
                f"DELETE FROM `{output_table}_{dealer_list}` WHERE true;"
            ).result()

            # get output tableref
            table_ref = TableReference.from_string(f"{output_table}_{dealer_list}")
            client.load_table_from_dataframe(
                dataframe=pd.DataFrame(input_data),
                destination=client.get_table(table_ref),
            )
    except (ValueError, KeyError, TypeError):
        print(ValueError, KeyError, TypeError)
