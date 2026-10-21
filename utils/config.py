"""Central settings. Everything you might want to adjust lives here."""
from pathlib import Path

# ---------------------------------------------------------------- paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "diabetic_retinopathy_model.keras"
EVAL_DIR = BASE_DIR / "evaluation"
ASSETS_DIR = BASE_DIR / "assets"

# ---------------------------------------------------------------- model input
IMG_SIZE = (224, 224)  # (width, height) expected by the model

# PREPROCESSING -- READ THIS IF PREDICTIONS LOOK WRONG
# The saved model is an EfficientNetB0 whose first layers are Rescaling(1/255)
# and Normalization (found by inspecting the .keras file). That means the model
# normalises pixels itself and expects RAW pixel values in the range 0-255.
#   "raw_0_255"   -> feed 0-255 float values (default, matches the saved model)
#   "zero_to_one" -> divide by 255 first (ONLY use if your training code did
#                    this AND you were not relying on the built-in layers)
PIXEL_SCALING = "raw_0_255"

# How the image is resized to 224 x 224:
#   "pillow"     -> Pillow bilinear resize (smooths when shrinking big photos)
#   "tensorflow" -> tf.image.resize bilinear (what tf.keras image loaders use)
# If your training notebook used image_dataset_from_directory or
# tf.image.resize, try "tensorflow" and compare.
RESIZE_BACKEND = "pillow"

PIXEL_SCALING_OPTIONS = ("raw_0_255", "zero_to_one")
RESIZE_BACKEND_OPTIONS = ("pillow", "tensorflow")

# ---------------------------------------------------------------- upload rules
ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png"]
MAX_UPLOAD_MB = 15
MIN_SIDE_PX = 64

# ---------------------------------------------------------------- classes
CLASS_NAMES = {
    0: "No DR",
    1: "Mild DR",
    2: "Moderate DR",
    3: "Severe DR",
    4: "Proliferative DR",
}
NUM_CLASSES = len(CLASS_NAMES)

# ---------------------------------------------------------------- recorded project results
# These were measured earlier in the project. The website does NOT recompute them.
RECORDED = {
    "dataset": "APTOS 2019 Blindness Detection",
    "total_images": 3662,
    "train_images": 2563,
    "val_images": 549,
    "test_images": 550,
    "input_size": "224 × 224 pixels",
    "batch_size": 16,
    "epochs": 10,
    "test_accuracy_pct": 74.55,
    "test_loss": 0.649,
}

STUDENTS = [
    {"name": "Divyasri.V", "roll": "241801063"},
    {"name": "Divyadarshini.S", "roll": "241801059"},
]

APP_TITLE = "Diabetic Retinopathy Grading Using Deep Learning"
