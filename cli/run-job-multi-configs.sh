# Run a dataflow job
export PIPELINE_NAME=$1
export CONFIGS_NAME=$2
export TEMPLATE_VERSION=$3
export DDA_CODE="brm"
export PROCESSING_PROJECT="brm-processing-dev-1098"
gcloud dataflow flex-template run "${PIPELINE_NAME//_/-}-${CONFIGS_NAME//_/-}-${TEMPLATE_VERSION}-`date +%Y%m%d-%H%M%S`" \
--template-file-gcs-location "gs://${PROCESSING_PROJECT}-dataflow-artifacts/${PIPELINE_NAME}/templates/${TEMPLATE_VERSION}/${PIPELINE_NAME}_template.json" \
--parameters gcs_to_bq_configs="gs://${PROCESSING_PROJECT}-dataflow-artifacts/${PIPELINE_NAME}/configs/${TEMPLATE_VERSION}/${CONFIGS_NAME}/io_configs.json" \
--parameters final_columns_transform_configs="gs://${PROCESSING_PROJECT}-dataflow-artifacts/${PIPELINE_NAME}/configs/${TEMPLATE_VERSION}/${CONFIGS_NAME}/final_columns_transform_configs.json" \
--parameters experiment="use_runner_v2" \
--parameters sdk_container_image="europe-west1-docker.pkg.dev/dda-artifact-registries-f8b0/${DDA_CODE}-nightly-registry/dataflow-worker:${TEMPLATE_VERSION}" \
--parameters sdk_worker_parallelism=4 \
--region "europe-west1" \
--worker-region "europe-west1" \
--network "${DDA_CODE}-local-vpc-dev" \
--subnetwork "regions/europe-west1/subnetworks/brm-local-vpc-dev-subnet-1" \
--disable-public-ips \
--staging-location "gs://${PROCESSING_PROJECT}-dataflow-staging/${PIPELINE_NAME}" \
--temp-location "gs://${PROCESSING_PROJECT}-dataflow-temp/${PIPELINE_NAME}" \
--service-account-email "dataflow-etl-sa-dev@${PROCESSING_PROJECT}.iam.gserviceaccount.com" \
--project ${PROCESSING_PROJECT} \
--worker-machine-type="n1-standard-4" \
--num-workers 1 \
--max-workers 5