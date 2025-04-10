import os
import numpy as np
import tensorflow as tf
import argparse
from tensorflow import keras
import onnxruntime as ort

# Constants
SEQ_LEN = 32


def load_tensorflow_model(model_path):
    """Load a TensorFlow/Keras model from the specified path."""
    print(f"Loading TensorFlow model from {model_path}")
    model = keras.models.load_model(model_path)
    print("Model loaded successfully")
    return model


def load_onnx_model(model_path):
    """Load an ONNX model for inference."""
    print(f"Loading ONNX model from {model_path}")
    session = ort.InferenceSession(model_path)
    print("ONNX model loaded successfully")
    return session


def generate_random_input(batch_size=1):
    """Generate a random input tensor for testing."""
    return np.random.rand(batch_size, SEQ_LEN, 1).astype(np.float32)


def load_sample_from_file(file_path):
    """Load a sample input from a NumPy file."""
    if os.path.exists(file_path):
        return np.load(file_path)
    else:
        print(f"File {file_path} not found. Using random input instead.")
        return generate_random_input()


def infer_tensorflow(model, input_data):
    """Perform inference using a TensorFlow model."""
    predictions = model.predict(input_data)
    return predictions


def infer_onnx(session, input_data):
    """Perform inference using an ONNX model."""
    # Get input and output names
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    # Run inference
    results = session.run([output_name], {input_name: input_data})
    return results[0]


def main():
    parser = argparse.ArgumentParser(description="Model Inference Script")
    parser.add_argument("--model_type", type=str, choices=["tensorflow", "onnx"], default="tensorflow",
                        help="Type of model to use for inference")
    parser.add_argument("--model_path", type=str, default="general_lstm.keras",
                        help="Path to the saved model file")
    parser.add_argument("--input_file", type=str, default=None,
                        help="Path to a saved input file (.npy format)")
    parser.add_argument("--num_samples", type=int, default=1,
                        help="Number of random samples to generate for inference")
    parser.add_argument("--save_examples", action="store_true",
                        help="Save generated examples to files")

    args = parser.parse_args()

    # Create a directory for outputs if it doesn't exist
    os.makedirs("inference_outputs", exist_ok=True)

    # Load the appropriate model based on type
    if args.model_type == "tensorflow":
        model = load_tensorflow_model(args.model_path)
    else:  # onnx
        model = load_onnx_model(args.model_path)

    # Process input data
    if args.input_file:
        # Load input from file
        input_data = load_sample_from_file(args.input_file)
        print(f"Loaded input with shape: {input_data.shape}")

        # Perform inference
        if args.model_type == "tensorflow":
            predictions = infer_tensorflow(model, input_data)
        else:  # onnx
            predictions = infer_onnx(model, input_data)

        print(f"Predictions for loaded input:\n{predictions}")

    # Generate random examples
    for i in range(args.num_samples):
        random_input = generate_random_input()

        if args.save_examples:
            example_path = f"inference_outputs/sample_input_{i}.npy"
            np.save(example_path, random_input)
            print(f"Saved random input to {example_path}")

        # Perform inference
        if args.model_type == "tensorflow":
            predictions = infer_tensorflow(model, random_input)
        else:  # onnx
            predictions = infer_onnx(model, random_input)

        print(f"Predictions for random sample {i}:\n{predictions}")

        if args.save_examples:
            output_path = f"inference_outputs/sample_output_{i}.npy"
            np.save(output_path, predictions)
            print(f"Saved predictions to {output_path}")

    print("Inference completed successfully")


if __name__ == "__main__":
    main()
