"""Model loading and prediction. The model is loaded once and reused."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image

from . import config
from .preprocessing import preprocess

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")  # quieter TensorFlow console


class ModelLoadError(RuntimeError):
    """The trained model file is missing or could not be loaded."""


class PredictionError(RuntimeError):
    """The model ran but produced an unusable result."""


@dataclass
class PredictionResult:
    grade: int
    label: str
    score: float  # model output score for the predicted class, 0-1
    scores: list = field(default_factory=list)  # five scores, index = grade
    pixel_scaling: str = config.PIXEL_SCALING
    resize_backend: str = config.RESIZE_BACKEND


@lru_cache(maxsize=1)
def get_model():
    """Load the trained model from models/ once; later calls return the same object."""
    path = Path(config.MODEL_PATH)
    if not path.is_file():
        raise ModelLoadError(
            f"Model file not found at: {path}\n"
            "Place 'diabetic_retinopathy_model.keras' inside the 'models' folder."
        )
    try:
        import keras

        model = keras.models.load_model(path, compile=False)  # weights are NOT modified
    except Exception as exc:  # noqa: BLE001 - show any loader problem to the user
        raise ModelLoadError(
            f"The model file exists but could not be loaded: {type(exc).__name__}: {exc}\n"
            "This usually means TensorFlow/Keras is too old. Run: "
            "pip install --upgrade -r requirements.txt"
        ) from exc

    in_shape, out_shape = model.input_shape, model.output_shape
    if tuple(in_shape[1:]) != (config.IMG_SIZE[1], config.IMG_SIZE[0], 3):
        raise ModelLoadError(f"Unexpected model input shape {in_shape}; expected (None, 224, 224, 3).")
    if out_shape[-1] != config.NUM_CLASSES:
        raise ModelLoadError(f"Unexpected model output shape {out_shape}; expected 5 classes.")
    return model


def predict_batch(model, batch: np.ndarray) -> np.ndarray:
    """Run the model on a preprocessed batch and return an (N, 5) array of outputs."""
    out = np.asarray(model.predict(batch, verbose=0), dtype=np.float64)
    if out.ndim != 2 or out.shape[1] != config.NUM_CLASSES or not np.all(np.isfinite(out)):
        raise PredictionError(f"The model returned an unusable output of shape {out.shape}.")
    if not np.allclose(out.sum(axis=1), 1.0, atol=1e-3):
        raise PredictionError("The model output is not a softmax distribution (scores do not sum to 1).")
    return out


def predict(
    model,
    image: Image.Image,
    pixel_scaling: str | None = None,
    resize_backend: str | None = None,
) -> PredictionResult:
    """Predict the DR grade of one PIL image using the real model output."""
    pixel_scaling = pixel_scaling or config.PIXEL_SCALING
    resize_backend = resize_backend or config.RESIZE_BACKEND
    batch = preprocess(image, pixel_scaling, resize_backend)
    scores = predict_batch(model, batch)[0]
    grade = int(np.argmax(scores))
    return PredictionResult(
        grade=grade,
        label=config.CLASS_NAMES[grade],
        score=float(scores[grade]),
        scores=[float(s) for s in scores],
        pixel_scaling=pixel_scaling,
        resize_backend=resize_backend,
    )
