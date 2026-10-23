from __future__ import annotations

import os
import base64
from typing import Literal

import cv2
import numpy as np
from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel, Field
from tensorflow import keras

paint_router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAINT_MODEL_PATH = os.getenv(
    "PAINT_MODEL_PATH",
    "models/paint/efficientnet_binaire_phase2_best.keras",
)
MAX_FILE_SIZE = 10 * 1024 * 1024
IMAGE_SIZE = (384, 384)
REPAINT_THRESHOLD = 0.52
UNCERTAINTY_THRESHOLD = 0.65
MODEL_VERSION = "efficientnet-b0-atelier-phase2"
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png"}

paint_model = None


class PaintProbabilities(BaseModel):
    origine: float = Field(..., ge=0.0, le=1.0)
    repeint: float = Field(..., ge=0.0, le=1.0)


class PaintPredictionResponse(BaseModel):
    verdict: Literal["origine", "repeint", "incertain"]
    confidence: float = Field(..., ge=0.0, le=1.0)
    probabilities: PaintProbabilities
    model_version: str
    is_experimental: bool
    cropped_image: str | None = None


def resolve_paint_model_path() -> str:
    if os.path.isabs(PAINT_MODEL_PATH):
        return PAINT_MODEL_PATH
    return os.path.join(BASE_DIR, PAINT_MODEL_PATH)


def validate_paint_model_layers(model) -> None:
    expected_layers = {"crop_zone_utile", "resize_apres_crop", "data_augmentation"}
    layer_names = {layer.name for layer in getattr(model, "layers", [])}
    missing_layers = expected_layers - layer_names
    if missing_layers:
        raise RuntimeError(
            "Paint model is missing expected internal preprocessing layers: "
            f"{sorted(missing_layers)}"
        )


def load_paint_model():
    global paint_model

    if paint_model is not None:
        return paint_model

    model_path = resolve_paint_model_path()
    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"Paint model not found: {model_path}")

    paint_model = keras.models.load_model(model_path, compile=False)
    validate_paint_model_layers(paint_model)
    return paint_model


def preprocess_paint_image(contents: bytes) -> np.ndarray:
    encoded = np.frombuffer(contents, dtype=np.uint8)
    image_bgr = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise ValueError("Unable to decode uploaded image")

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    image_rgb = cv2.resize(image_rgb, IMAGE_SIZE, interpolation=cv2.INTER_AREA)
    return image_rgb.astype(np.float32)


def create_cropped_image_data_url(contents: bytes) -> str | None:
    encoded = np.frombuffer(contents, dtype=np.uint8)
    image_bgr = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise ValueError("Unable to decode uploaded image")

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    resized_rgb = cv2.resize(image_rgb, IMAGE_SIZE, interpolation=cv2.INTER_AREA)
    cropped_rgb = resized_rgb[32:352, 32:352]
    cropped_display_rgb = cv2.resize(
        cropped_rgb,
        IMAGE_SIZE,
        interpolation=cv2.INTER_AREA,
    )
    cropped_display_bgr = cv2.cvtColor(cropped_display_rgb, cv2.COLOR_RGB2BGR)
    encoded_ok, encoded_crop = cv2.imencode(".jpg", cropped_display_bgr)
    if not encoded_ok:
        return None

    return (
        "data:image/jpeg;base64,"
        + base64.b64encode(encoded_crop.tobytes()).decode("ascii")
    )


def predict_paint(
    image: np.ndarray,
    cropped_image: str | None = None,
) -> PaintPredictionResponse:
    model = load_paint_model()
    prediction = np.asarray(model.predict(np.expand_dims(image, axis=0), verbose=0))[0]

    if len(prediction) != 2:
        raise RuntimeError("Paint model must return exactly two probabilities")

    proba_origine = float(prediction[0])
    proba_repeint = float(prediction[1])
    confidence = max(proba_origine, proba_repeint)

    if confidence < UNCERTAINTY_THRESHOLD:
        verdict = "incertain"
    elif proba_repeint >= REPAINT_THRESHOLD:
        verdict = "repeint"
    else:
        verdict = "origine"

    return PaintPredictionResponse(
        verdict=verdict,
        confidence=confidence,
        probabilities=PaintProbabilities(
            origine=proba_origine,
            repeint=proba_repeint,
        ),
        model_version=MODEL_VERSION,
        is_experimental=True,
        cropped_image=cropped_image,
    )


@paint_router.post(
    "/paint/predict",
    response_model=PaintPredictionResponse,
    response_model_exclude_none=True,
)
async def predict_paint_endpoint(file: UploadFile = File(...)) -> PaintPredictionResponse:
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only JPG and PNG images are supported",
        )

    contents = await file.read(MAX_FILE_SIZE + 1)
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Image file must not exceed 10 MB",
        )

    try:
        image = preprocess_paint_image(contents)
        try:
            cropped_image = create_cropped_image_data_url(contents)
        except (AttributeError, TypeError):
            cropped_image = None
        return predict_paint(image, cropped_image)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Paint inference failed") from exc
