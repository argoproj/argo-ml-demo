# TFJobs

###### [back to kubeflow](KUBEFLOW.md)

TFJobs are a Kubeflow custom resource for distrubuted tensorflow jobs on kubeflow

To create a TF Job:
```bash
ks generate tf-job-simple $JOBNAME --name=$JOBNAME
```

This will create a pre-built stencil for a tf-job (good for beginners) within a .jsonnet component inside of kubeflow_ks_app/components

Next enter the components directory and open the $JOBNAME.jsonnet file in a text editor

```bash
cd kubeflow_ks_app/components
vim $JOBENAME.jsonnet
```

Replace the image with a custom image.
```diff
-local image = "gcr.io/kubeflow/tf-benchmarks-cpu:v20171202-bdab599-dirty-284af3";

+++ image can be replaced with any image running tensorflow
+local image = "tensorflow/tensorflow:latest-gpu";
```
And change the commands and arguments to run your python file instead

Kubeflow is best used to utilize Tensorflow's unique architecture of deploying chief's and worker's and PS's. If you simply want to run tensorflow without these custom resources it is possible by deploying only workers.

If you want to learn more about TF architecture go to [this link](https://www.tensorflow.org/extend/architecture).