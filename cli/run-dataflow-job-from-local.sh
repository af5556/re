export PYTHONPATH=../python
export PROCESSING_PROJECT="chk-processing-dev-d3f8"
export PIPELINE_NAME="silver-to-row"
export FINAL_ROW_CONFIG="$(pwd)/../configs/raw-to-silver/final_rows_filter_configs.json"
export FINAL_COLUMNS_CONFIG="$(pwd)/../configs/raw-to-silver/final_columns_transform_configs.json"
export IO_CONFIGS="$(pwd)/../configs/raw-to-silver/io_configs.json"

python ../python/pipelines/raw_to_silver/job_launcher.py \
--project=chk-processing-dev-22b0 \
--staging_location=gs://${PROCESSING_PROJECT}-dataflow-staging/${PIPELINE_NAME} \
--service_account_email=dataflow-etl-sa-dev@${PROCESSING_PROJECT}.iam.gserviceaccount.com \
--final_rows_filter_configs=${FINAL_ROW_CONFIG} \
--max_num_workers=5 \
--runner=DataflowRunner \
--job_name=${PIPELINE_NAME}-`date +%Y%m%d-%H%M%S` \
--temp_location=gs://chk-processing-dev-22b0-dataflow-temp/${PIPELINE_NAME} \
--bq_to_bq_configs=${IO_CONFIGS} \
--subnetwork=regions/europe-west1/subnetworks/chk-local-vpc-dev-subnet-1 \
--num_workers=1 \
--machine_type=e2-standard-2 \
--network=chk-local-vpc-dev \
--region=europe-west1 \
--final_columns_transform_configs=${FINAL_COLUMNS_CONFIG} \
--no_use_public_ips