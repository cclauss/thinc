import numpy
import pytest
from thinc.api import NumpyOps, Softmax_v2

OPS = NumpyOps()

inputs = OPS.xp.asarray([[4, 2, 3, 4], [1, 5, 3, 1], [9, 8, 5, 7]], dtype="f")
outputs = OPS.xp.asarray(
    [
        [0.39948627, 0.05406459, 0.14696279, 0.39948627],
        [0.01562812, 0.8532666, 0.11547707, 0.01562812],
        [0.657233, 0.24178252, 0.01203764, 0.08894681],
    ],
    dtype="f",
)


def test_unnormalized_softmax_backprop():
    model = Softmax_v2(normalize_outputs=False)
    model.initialize(inputs, outputs)
    _, backprop = model(inputs, is_train=False)
    with pytest.raises(ValueError, match="backprop is not supported"):
        backprop(OPS.xp.zeros_like(outputs))

    # Backprop should not fail when training.
    _, backprop = model(inputs, is_train=True)
    dX = backprop(OPS.xp.zeros_like(outputs))
    assert OPS.xp.all(dX == 0.0)