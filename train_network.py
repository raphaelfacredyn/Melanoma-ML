from keras.applications.inception_v3 import InceptionV3
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator
import sys
import time

def current_millis_time():
    return int(round(time.time() * 1000))


batch_size = 16
numTrainImgs = 2000
numValidationImgs = 150

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
    rescale=1. / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1. / 255)

# this is a generator that will read pictures found in
# subfolers of 'data/train', and indefinitely generate
# batches of augmented image data
train_generator = train_datagen.flow_from_directory(
    'train_resized',  # this is the target directory
    target_size=(299, 299),  # all images will be resized to 299x299
    batch_size=batch_size,
    class_mode='binary'
)  # since we use binary_crossentropy loss, we need binary labels

# this is a similar generator, for validation data
validation_generator = test_datagen.flow_from_directory(
    'validation_resized',
    target_size=(299, 299),
    batch_size=batch_size,
    class_mode='binary')

# create the base pre-trained model
base_model = InceptionV3(weights='imagenet', include_top=False)

# add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
# let's add a fully-connected layer
x = Dense(1024, activation='relu')(x)
# and an output layer with one neuron which is binary
predictions = Dense(1, activation='softmax')(x)

# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)

# first: train only the top layers (which were randomly initialized)
# i.e. freeze all convolutional InceptionV3 layers
for layer in base_model.layers:
    layer.trainable = False

# compile the model (should be done *after* setting layers to non-trainable)
model.compile(optimizer='rmsprop', loss='binary_crossentropy')

if sys.argv[1] == "load":
    model.load_weights(sys.argv[2])
else:
    # train the model on the new data for a few epochs
    model.fit_generator(
        train_generator,
        steps_per_epoch=numTrainImgs // batch_size,
        epochs=8,
        validation_data=validation_generator,
        validation_steps=numValidationImgs // batch_size)
    model.save('saves/trained_top_layers'+str(current_millis_time)+'.h5')
    model.save_weights('saves/trained_top_layers-weights'+str(current_millis_time)+'.h5')

# at this point, the top layers are well trained and we can start fine-tuning
# convolutional layers from inception V3. We will freeze the bottom N layers
# and train the remaining top layers.

# let's visualize layer names and layer indices to see how many layers
# we should freeze:
for i, layer in enumerate(base_model.layers):
    print(i, layer.name)

# we chose to train the top 2 inception blocks, i.e. we will freeze
# the first 249 layers and unfreeze the rest:
for layer in model.layers[:249]:
    layer.trainable = False
for layer in model.layers[249:]:
    layer.trainable = True

# we need to recompile the model for these modifications to take effect
# we use SGD with a low learning rate
model.compile(
    optimizer=SGD(lr=0.0001, momentum=0.9), loss='binary_crossentropy')

# we train our model again (this time fine-tuning the top 2 inception blocks
# alongside the top Dense layers
model.fit_generator(
    train_generator,
    steps_per_epoch=(numTrainImgs // batch_size),
    epochs=50,
    validation_data=validation_generator,
    validation_steps=numValidationImgs // batch_size)

model.save('saves/trained_final'+str(current_millis_time)+'.h5')
model.save_weights('saves/trained_final-weights'+str(current_millis_time)+'.h5')
