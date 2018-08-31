

# Deploying Kubeflow

###### [back to the argo 3d](../README.md)

Guide for those looking to run Kubeflow Version 0.2.2 on their Kuberenetes Cluster

##### Kubeflows guide in its current state needs lots of work. However, their guide is progressively being updated at [Kubeflow.org](https://www.kubeflow.org/docs/guides/requirements/) 

### Install ksonnet command line utility
```bash
brew install ksonnet/tap/ks
```

### RBAC

Before deploying kubeflow make sure you have cluster admin privileges on your kubernetes cluster

```bash
kubectl create clusterrolebinding YOURNAME-cluster-admin-binding --clusterrole=cluster-admin --user=YOUREMAIL@gmail.com
```

### Install Kubeflow
Kubeflow is required in order to deploy the custom resources that use Tensorflow: TFJobs.

To install Kubeflow run the following command:
```bash
export KUBEFLOW_VERSION=0.2.2
export KUBEFLOW_DEPLOY=false
curl https://raw.githubusercontent.com/kubeflow/kubeflow/v$KUBEFLOW_VERSION/scripts/deploy.sh | bash
``` 
This command will automatically deploy a bash script which will set up a ksonnet directory called ksonnet_ks_app with all the necessary built-in packages and deploy them. The `export KUBEFLOW_DEPLOY=false` command disables ks from deploying to your default namespace.

Now all thats left to deploy kubeflow is a couple ksonnet commands which can only be run inside the kubeflow_ks_app directory
```bash
#The first two commands are for running deploying kubeflow in a new namespace.
#Without these commands kubeflow will deploy to the default namespace
cd kubeflow_ks_app
NAMESPACE=mykubeflow
kubectl create ns $NAMESPACE
ks env set default --namespace=$NAMESPACE
ks apply default
```

If you would like to delete an old instance of kubeflow, or delete it all together use the following commands inside the kubeflow_ks_app directory:
```bash
#Undeploy
ks delete $NAMESPACE

#delete ks application (Only necessary if you really f*k'd up)
cd ..
rm -rf kubeflow_ks_app kubeflow_repo
```

## Creating your own TFJob/TFService

#### This part of the tutorial is simply documentation for creating your own tensorflow application since websites like [kubeflow.org](http://kubeflow.org/docs/started/getting-started) are often hard to follow or outdated as of June, 31, 2018.

+ [TFJobs](TFJOBS.md)
+ [TFServing](TFSERVE.md)

##### Kubeflows guide in its current state needs lots of work. Their guide is progressively being updated at [Kubeflow.org](https://www.kubeflow.org/docs/guides/requirements/) 