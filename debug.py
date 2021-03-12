from tensorflow.python.client import device_lib
import tensorflow as tf
print("Listando devices:")
print(device_lib.list_local_devices())
#print("Listando devices GPU:")
#print(tf.config.experimental.list_physical_devices('GPU'))
input("Press Enter to exit...")
