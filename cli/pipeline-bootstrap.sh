# BEFORE USING THIS SCRIPT PLEASE INSTALL envsubst (could be found here https://github.com/a8m/envsubst)
export PIPELINE_NAME=$1

create_devops(){
  mkdir ../devops/"${PIPELINE_NAME}"
  cp -rf pipeline_template/devops/* "../devops/${PIPELINE_NAME}"
  envsubst < "pipeline_template/devops/cicd.yaml" > "../devops/${PIPELINE_NAME}/cicd.yaml"
  echo """
${PIPELINE_NAME}_deployment:
  stage: build-and-deliver
  trigger:
    include:
      - local: devops/${PIPELINE_NAME}/cicd.yaml
      - local: devops/cicd-template.yaml
    strategy: depend
  when: manual
  allow_failure: true
  """ >> ../.gitlab-ci.yml
}

create_python(){
  mkdir ../python/pipelines/"${PIPELINE_NAME}"
  cp -rf pipeline_template/python ../python/pipelines/"${PIPELINE_NAME}"
}

create_devops
create_python