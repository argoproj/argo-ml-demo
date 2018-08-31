# Argo-ML-Demo
An Argo Workflow that takes in a photo, scans it for faces and produces a 3D obj rendering for each face detected. Our project uses **Ageitgey's** [face_recognition](https://github.com/ageitgey/face_recognition) to detect individual faces within a photo, **YadiaraF's** [PRNet](https://github.com/YadiraF/PRNet) to create a 3D Face Reconstruction, and various other bash commands inside of Ubuntu and Debian containers for most of the other pods. This project uses various new Argo Workflow features such as *conditional deployments, parallelism, custom resources, and loops*. Our project also utilizes kubeflow and tensorflow in order to run PRNet. PRNet uses CUDA which requires access to a GPU (We use the NVIDIA Tesla P100). In order to run our workflow at high performance we used a GKE cluster.

## Getting Started

### Prerequisites
In order to run our project you must have the following installed.

+ Argo
```
argo version
argo: v2.1.1
  BuildDate: 2018-05-29T20:38:37Z
  GitCommit: ac241c95c13f08e868cd6f5ee32c9ce273e239ff
  GitTreeState: clean
  GitTag: v2.1.1
  GoVersion: go1.9.3
  Compiler: gc
  Platform: darwin/amd64
```
+ Kubectl
```
kubectl version
Client Version: version.Info{Major:"1", Minor:"11", GitVersion:"v1.11.0", GitCommit:"91e7b4fd31fcd3d5f436da26c980becec37ceefe", GitTreeState:"clean", BuildDate:"2018-06-27T22:29:25Z", GoVersion:"go1.10.3", Compiler:"gc", Platform:"darwin/amd64"}
Server Version: version.Info{Major:"1", Minor:"10+", GitVersion:"v1.10.5-gke.3", GitCommit:"6265b9797fc8680c8395abeab12c1e3bad14069a", GitTreeState:"clean", BuildDate:"2018-07-19T23:02:51Z", GoVersion:"go1.9.3b4", Compiler:"gc", Platform:"linux/amd64"}
```
+ Ksonnet
```
ks version
ksonnet version: 0.12.0-rc1
jsonnet version: v0.10.0
client-go version:
```

+ Kubeflow

*Instructions for deploying kubeflow can be found [here](docs/KUBEFLOW.md)*

+ Kubernetes Cluster w/ NVIDIA GPU's enabled

For GKE users, GPU deployment can be found [here](https://cloud.google.com/kubernetes-engine/docs/how-to/gpus) 

For other users, make sure you have the NVIDIA driver set up in your cluster. The following command will install a Daemeonset with the driver which is needed in order to utilize the `limits: nvidia.com/gpu: 1` line in the yaml.

```bash
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/stable/nvidia-driver-installer/cos/daemonset-preloaded.yaml
```

### Custom images

##### This project uses some custom docker images in the workflow. The face recognition project can be found [here](https://github.com/EliZucker/face_recognition)

### Give Workflow RBAC privileges
In order for a workflow to create custom resources (e.g. TensorflowJob), a cluster-admin role should be used. The following will grant the default service account in the default namespace cluster-admin:
```kubectl create rolebinding default-admin --clusterrole=cluster-admin --serviceaccount=default:default```

### Deploy Our Project
```bash
git clone https://github.com/argoproj/argo-ml-demo.git
cd argo-ml-demo
# image must be publicly available on the internet
argo submit demo.yaml -p image-url="yourimagehere.jpg"
```

## Authors
+ **[Edan Sneh](https://github.com/EdanSneh)** - Intuit Intern
+ **[Eli Zucker](http://github.com/EliZucker)** - Intuit Intern

## Acknowledgments
Special thanks to:
+ [Jesse Suen](http://github.com/jessesuen) and [Alexander Matyushentsev](http://github.com/alexmt) for countless help along the way