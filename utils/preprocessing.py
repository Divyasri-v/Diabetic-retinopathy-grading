"""Image validation and preprocessing for the DR model."""
from __future__ import annotations

import io

import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError

from . import config


class InvalidImageError(ValueError):
    """Raised when an uploaded file cannot be used as a retinal image."""


def load_image(data: bytes) -> Image.Image:
    """Validate raw upload bytes and return an RGB PIL image.

    Raises InvalidImageError with a plain-language message on any problem.
    """
    if not data:
        raise InvalidImageError("The uploaded file is empty. Choose a different image.")

    max_bytes = config.MAX_UPLOAD_MB * 1024 * 1024
    if len(data) > max_bytes:
        raise InvalidImageError(
            f"The file is {len(data) / 1024 / 1024:.1f} MB. "
            f"The limit is {config.MAX_UPLOAD_MB} MB. Resize or compress the image and try again."
        )

    try:
        probe = Image.open(io.BytesIO(data))
        fmt = probe.format
        probe.verify()  # detects truncated / corrupt files
        image = Image.open(io.BytesIO(data))  # verify() leaves the first handle unusable
        image.load()
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError, Image.DecompressionBombError):
        raise InvalidImageError(
            "This file could not be read as an image. It may be corrupted or not a real "
            "JPG/PNG file. Export the photo again as JPG or PNG and retry."
        ) from None

    if fmt not in ("JPEG", "PNG"):
        raise InvalidImageError(
            f"Unsupported image format ({fmt or 'unknown'}). Upload a JPG, JPEG or PNG file."
        )

    image = ImageOps.exif_transpose(image)  # respect camera orientation
    image = image.convert("RGB")  # drops alpha / converts greyscale and palette images

    if min(image.size) < config.MIN_SIDE_PX:
        raise InvalidImageError(
            f"The image is only {image.size[0]} × {image.size[1]} pixels. "
            f"Use a fundus photograph at least {config.MIN_SIDE_PX} pixels on each side."
        )
    return image


def preprocess(
    image: Image.Image,
    pixel_scaling: str | None = None,
    resize_backend: str | None = None,
) -> np.ndarray:
    """Convert a PIL image to a model-ready batch of shape (1, 224, 224, 3), float32."""
    pixel_scaling = pixel_scaling or config.PIXEL_SCALING
    resize_backend = resize_backend or config.RESIZE_BACKEND
    if pixel_scaling not in config.PIXEL_SCALING_OPTIONS:
        raise ValueError(f"Unknown pixel_scaling: {pixel_scaling!r}")
    if resize_backend not in config.RESIZE_BACKEND_OPTIONS:
        raise ValueError(f"Unknown resize_backend: {resize_backend!r}")

    image = image.convert("RGB")
    if resize_backend == "pillow":
        arr = np.asarray(image.resize(config.IMG_SIZE, Image.BILINEAR), dtype=np.float32)
    else:
        import tensorflow as tf  # imported lazily: only needed for this option

        arr = tf.image.resize(
            np.asarray(image, dtype=np.float32),
            (config.IMG_SIZE[1], config.IMG_SIZE[0]),
            method="bilinear",
        ).numpy()

    if pixel_scaling == "zero_to_one":
        arr = arr / 255.0
    # "raw_0_255": leave values as they are; the model's own layers normalise them.

    return np.expand_dims(arr.astype(np.float32), axis=0)
