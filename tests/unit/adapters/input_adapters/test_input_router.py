from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from regex_engine.adapters.input_adapters.input_router import InputRouter


def make_adapter(*, supports: bool, records=None):
    adapter = Mock()
    adapter.supports.return_value = supports
    adapter.to_records.return_value = records or []
    return adapter


def make_record(name: str):
    return SimpleNamespace(name=name)


def test_should_return_true_when_any_adapter_supports_data():
    data = object()

    first_adapter = make_adapter(supports=False)
    second_adapter = make_adapter(supports=True)

    router = InputRouter(first_adapter, second_adapter)

    assert router.supports(data) is True

    first_adapter.supports.assert_called_once_with(data)
    second_adapter.supports.assert_called_once_with(data)


def test_should_return_false_when_no_adapter_supports_data():
    data = object()

    first_adapter = make_adapter(supports=False)
    second_adapter = make_adapter(supports=False)

    router = InputRouter(first_adapter, second_adapter)

    assert router.supports(data) is False

    first_adapter.supports.assert_called_once_with(data)
    second_adapter.supports.assert_called_once_with(data)


def test_should_stop_checking_supports_after_first_matching_adapter():
    data = object()

    first_adapter = make_adapter(supports=True)
    second_adapter = make_adapter(supports=True)

    router = InputRouter(first_adapter, second_adapter)

    assert router.supports(data) is True

    first_adapter.supports.assert_called_once_with(data)
    second_adapter.supports.assert_not_called()


def test_should_convert_data_using_first_supported_adapter():
    data = object()
    records = [
        make_record("mleko"),
        make_record("mąka pszenna"),
    ]

    first_adapter = make_adapter(supports=False)
    second_adapter = make_adapter(supports=True, records=records)
    third_adapter = make_adapter(supports=True, records=[make_record("jajka")])

    router = InputRouter(first_adapter, second_adapter, third_adapter)

    result = router.to_records(data)

    assert result == records

    first_adapter.supports.assert_called_once_with(data)
    second_adapter.supports.assert_called_once_with(data)
    third_adapter.supports.assert_not_called()

    first_adapter.to_records.assert_not_called()
    second_adapter.to_records.assert_called_once_with(data)
    third_adapter.to_records.assert_not_called()


def test_should_raise_type_error_when_no_adapter_supports_data():
    data = object()

    first_adapter = make_adapter(supports=False)
    second_adapter = make_adapter(supports=False)

    router = InputRouter(first_adapter, second_adapter)

    with pytest.raises(TypeError, match="Unsupported data type: object"):
        router.to_records(data)

    first_adapter.to_records.assert_not_called()
    second_adapter.to_records.assert_not_called()


def test_should_raise_type_error_when_router_has_no_adapters():
    router = InputRouter()

    with pytest.raises(TypeError, match="Unsupported data type: object"):
        router.to_records(object())
