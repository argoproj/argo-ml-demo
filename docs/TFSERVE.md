# TF Serving

###### [back to kubeflow](KUBEFLOW.md)

## Description:

TF Serving is a way to deploy a Tensorflow model in a server-like fashion. To talk to the server a client python file uses gRPC to communicate with the server.

## Creating the TF-server /w kubeflow

The main idea behind a tf-server is to save an entire TF model within a binary/txt format, so it can easily be deployed on many devices.

This tutorial assumes that you are starting with a working TF model. I would recommend cloning your model, so the end result is your initial model for quick developer testing, and a final model for user experience.

1. Identify your inputs and output tensors.

The input tensor can be found declared as a `tf.placeholder()`

```python
x = tf.placeholder("float", [None, n_input, 1])
```

The output tensor will be the final step of your tensorflow model which usually is on the same line as a `session.run()` or `eval()` function. You do not want to actually run the output, rather you want to stage it so remove the execution functons.

```python
#this
symbols_out_pred = reverse_dictionary[int(tf.argmax(onehot_pred, 1).eval())]

#becomes
output = tf.argmax(onehot_pred, 1)
```

2. Convert the input and output to TensorInfo protocol buffers

Multiple inputs are allowed

```python
tensor_info_input = tf.saved_model.utils.build_tensor_info(x)
tensor_info_output = tf.saved_model.utils.build_tensor_info(output)
```

3. Pick place to build path to and intialize builder

Choose a larger version number for each new version of your model

```python
export_path_base = /path/to/build/to
export_path = os.path.join(
    export_path_base,
    version_numer)
builder = tf.saved_model.builder.SavedModelBuilder(export_path)
```

4. Writing a signature
A signature is a way for the builder to identify the inputs and outputs of the TF model.

Map the protobuffs created before to input and output strings, these strings can be called anything, and will be needed by the client.

The method_name field will be dealt with by kubeflow.

The signature name under `signature_def_map` will also be needed by the client

```python
#signature (i/o)
prediction_signature = (
    tf.saved_model.signature_def_utils.build_signature_def(
        inputs={'actual_logs': tensor_info_input},
        outputs={'predicted_logs': tensor_info_output},
        method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME))

builder.add_meta_graph_and_variables(
    sess, [tf.saved_model.tag_constants.SERVING],
    signature_def_map={
        'log_guess': prediction_signature,
    })
```

5. Save the model

```py
builder.save(as_text=True)
```

Now run the python script and the output directory should contain files similar to the following

```bash
#/tmp/test is my chosen output directory
→ ls -Rt /tmp/test
1

/tmp/test/1:
saved_model.pbtxt variables

/tmp/test/1/variables:
variables.index               variables.data-00000-of-00001
```

6. Create Kubeflow component

Inside your Kubeflow ks directory run the following:

Note: MODEL_PATH should be the directory **in** which /version_numer is located

```bash
MODEL_COMPONENT=serveModel
MODEL_NAME=log-server
MODEL_PATH=gs://your/web/container
ks generate tf-serving ${MODEL_COMPONENT} --name=${MODEL_NAME}
```

add parameters
```bash
# path to model
ks param set ${MODEL_COMPONENT} modelPath ${MODEL_PATH}
# optional
ks param set ${MODEL_COMPONENT} numGpus 1
ks param set ${MODEL_COMPONENT} serviceType LoadBalancer
```

7. Launch or remove component
To launch your component
```bash
ks apply default -c ${MODEL_COMPONENT}
```

To remove your component
```bash
ks delete default -c ${MODEL_COMPONENT}
```

If everything is working as plan your tensorflow server should be up and running and pingable through a port-forward or through the Loadbalancer's external IP. To ping the server you now have to set up a client.

## Creating the client

1. Install Dependencies

A client can either be run inside of a pod or locally. To create a client you need to make sure a couple of dependencies are installed
```bash
pip install tensorflow-serving-api
pip install tensorflow
pip install requests
```

2. Set up a channel

A channel is a way for the client to connect to the server through the host:port. To set a channel up create another python file with some imports at the top

```py
from __future__ import print_function
from grpc.beta import implementations
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
import requests
import numpy as np

server = '35.185.218.27:9000'
host, port = server.split(':')
channel = implementations.insecure_channel(host, int(port))
stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
```

3. Send a request

Now to send a request you need to think back to the `${MODEL_NAME}`, signature name, inputs, and outputs from before.

```py
request = predict_pb2.PredictRequest()
request.model_spec.name = 'log-server'
request.model_spec.signature_name = 'log_guess'
```

To set up the inputs you now need to get the data that you want the model to run on. This data should be in the same shape as you specified for your input data inside of a numpy or tensorflow matrix. The data must be converted to a float

```py
#keys is a numpy array
request.inputs['actual_logs'].CopyFrom(
tf.contrib.util.make_tensor_proto(keys.astype(dtype=np.float32), shape=[n_input,1]))
#30.0 should be changed to 10.0 for async use
result_future = stub.Predict(request, 30.0)
output = np.array(result_future.outputs['predicted_logs'].float_val)
```
The float_val should be changed depending on the output of your model. Otherwise, it will return a blank matrix

Note: the above code can be put into a loop and run multiple time. This is especially useful in cases like an LSTM where your data is constantly updated.

## Helpful resources:
+ [How to deploy TensorFlow models to production using TF Serving - Thalles Silva](https://medium.freecodecamp.org/how-to-deploy-tensorflow-models-to-production-using-tf-serving-4b4b78d41700)
+ [Kubeflow TF-serving tutorial](https://www.kubeflow.org/docs/guides/components/tfserving/)