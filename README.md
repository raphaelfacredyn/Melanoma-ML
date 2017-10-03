# Procedure
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fraphy1234%2FMelanoma-ML.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fraphy1234%2FMelanoma-ML?ref=badge_shield)

* Download data and unzip as it train, test, validation
* Name the csv's train.csv, test.csv, validation.csv
* Create directories train_resized, test_resized, validation_resized
  * Inside each of these make the directories pos, neg
* Complete folder structure:

      out/

      preview/

      train_resized/
      ├── neg/
      └── pos/

      test_resized/
      ├── neg/
      └── pos/

      validation_resized/
      ├── neg/
      └── pos/

      train/

      test/

      validation/
* call ```python scale.py```
* call ```python split_data.py```
* call ```python train_network.py noLoad``` if you don't want to load weights, other wise call ```python train_network.py path/to/weights.h5```
* call ```python keras_to_tensorflow.py nameOfYourTrainedH5.h5```
      Note: Do not include the out/ just write the name of the file in the out folder
* call ```python path/to/strip_unused.py --input_graph=out/tensorflow.pb --output_graph=out/tensorflow-optimized.pb  --input_node_names=input_1 --output_node_names=predictions/Softmax --input_binary=true```


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fraphy1234%2FMelanoma-ML.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fraphy1234%2FMelanoma-ML?ref=badge_large)