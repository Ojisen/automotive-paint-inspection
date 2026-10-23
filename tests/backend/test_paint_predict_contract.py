import os
import sys
import types
from unittest.mock import patch

from fastapi.testclient import TestClient

os.environ["AIP_DISABLE_MODEL_LOADING"] = "1"

fake_numpy = types.ModuleType("numpy")
fake_numpy.uint8 = "uint8"
fake_numpy.frombuffer = lambda contents, dtype: contents
fake_numpy.expand_dims = lambda value, axis=0: [value]


class FakeArray(list):
    @property
    def shape(self):
        return (len(self),)


class FakePredictionArray:
    def __init__(self, value):
        self.value = value

    def __getitem__(self, index):
        return FakeArray(self.value[index])


fake_numpy.asarray = lambda value: FakePredictionArray(value)


class FakeImage:
    shape = (384, 384, 3)


fake_cv2 = types.ModuleType("cv2")
fake_cv2.IMREAD_COLOR = 1
fake_cv2.COLOR_BGR2RGB = 2
fake_cv2.INTER_AREA = 3
fake_cv2.imdecode = lambda encoded, mode: FakeImage()
fake_cv2.cvtColor = lambda image, code: image
fake_cv2.resize = lambda image, size, interpolation: image

fake_tensorflow = types.ModuleType("tensorflow")


class DummyKeras:
    class models:
        @staticmethod
        def load_model(_path, compile=False):
            raise AssertionError("The real model must not be loaded in unit tests")


fake_tensorflow.keras = DummyKeras()

sys.modules.setdefault("numpy", fake_numpy)
sys.modules.setdefault("cv2", fake_cv2)
sys.modules.setdefault("tensorflow", fake_tensorflow)

from backend import main  # noqa: E402
from backend import paint_analysis  # noqa: E402

paint_analysis.np = fake_numpy
paint_analysis.cv2 = fake_cv2


class FakePaintModel:
    layers = [
        types.SimpleNamespace(name="crop_zone_utile"),
        types.SimpleNamespace(name="resize_apres_crop"),
        types.SimpleNamespace(name="data_augmentation"),
    ]

    def __init__(self, prediction):
        self.prediction = prediction
        self.calls = 0

    def predict(self, _value, verbose=0):
        self.calls += 1
        return [self.prediction]


def make_client():
    return TestClient(main.app)


def test_invalid_mime_type_rejected():
    response = make_client().post(
        "/paint/predict",
        files={"file": ("sample.txt", b"not-an-image", "text/plain")},
    )

    assert response.status_code == 400
    assert "JPG and PNG" in response.json()["detail"]


def test_oversized_file_rejected():
    oversized = b"x" * (paint_analysis.MAX_FILE_SIZE + 1)
    response = make_client().post(
        "/paint/predict",
        files={"file": ("large.png", oversized, "image/png")},
    )

    assert response.status_code == 413


def test_invalid_image_content_rejected():
    with patch.object(paint_analysis, "preprocess_paint_image", side_effect=ValueError("Unable to decode uploaded image")):
        response = make_client().post(
            "/paint/predict",
            files={"file": ("invalid.png", b"invalid", "image/png")},
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Unable to decode uploaded image"


def test_repaint_response_uses_index_one_and_thresholds():
    model = FakePaintModel([0.18, 0.82])
    with patch.object(paint_analysis, "paint_model", model), patch.object(
        paint_analysis, "preprocess_paint_image", return_value=FakeImage()
    ):
        response = make_client().post(
            "/paint/predict",
            files={"file": ("paint.png", b"valid", "image/png")},
        )

    assert response.status_code == 200, response.json()
    assert response.json() == {
        "verdict": "repeint",
        "confidence": 0.82,
        "probabilities": {"origine": 0.18, "repeint": 0.82},
        "model_version": "efficientnet-b0-atelier-phase2",
        "is_experimental": True,
    }
    assert model.calls == 1


def test_low_confidence_response_is_uncertain():
    model = FakePaintModel([0.42, 0.58])
    with patch.object(paint_analysis, "paint_model", model), patch.object(
        paint_analysis, "preprocess_paint_image", return_value=FakeImage()
    ):
        response = make_client().post(
            "/paint/predict",
            files={"file": ("paint.png", b"valid", "image/png")},
        )

    assert response.status_code == 200, response.json()
    assert response.json()["verdict"] == "incertain"
    assert response.json()["confidence"] == 0.58


def test_model_loader_is_mocked_and_cached():
    model = FakePaintModel([0.9, 0.1])
    with patch.object(paint_analysis, "paint_model", None), patch.object(
        paint_analysis.keras.models, "load_model", return_value=model
    ) as load_model, patch.object(os.path, "isfile", return_value=True):
        assert paint_analysis.load_paint_model() is model
        assert paint_analysis.load_paint_model() is model

    load_model.assert_called_once_with(
        paint_analysis.resolve_paint_model_path(),
        compile=False,
    )
