"""pipeline for load raw """

from typing import Dict

from apache_beam import PCollection  # type: ignore
from apache_beam.options.pipeline_options import PipelineOptions  # type: ignore
from apache_beam.io import BigQueryDisposition  # type: ignore

from autobiz_etl_tools.autobizetl.models.configs import GCS2BQ  # type: ignore
from autobiz_etl_tools.autobizetl.gcs2bq import GCS2BQETLPipeline  # type: ignore


class LoadRawPipeline(GCS2BQETLPipeline):
    """main class for load raw pipeline"""

    def __init__(
        self,
        etl_configs: GCS2BQ,
        pipeline_options: PipelineOptions = PipelineOptions(),
        final_rows_filter_configs: list = None,
        final_columns_transform_configs: dict = None,
    ):
        super().__init__(
            etl_configs=etl_configs,
            pipeline_options=pipeline_options,
            final_rows_filter_configs=final_rows_filter_configs,
            final_columns_transform_configs=final_columns_transform_configs,
            bq_write_disposition=BigQueryDisposition.WRITE_TRUNCATE,
        )

    def _custom_transform(
        self, sources_data: Dict[str, PCollection[dict]]
    ) -> PCollection[dict]:

        return list(sources_data.values())[0]
