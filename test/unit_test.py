import pytest 
from streamrec.Data.data_collection import HuggingFaceCollector


@pytest.mark.asyncio
async def test_basic():
    config = {
        "address": "mnist",
        "limit": 5
    }
    collector = HuggingFaceCollector(config)
    await collector.request()
    assert hasattr(collector, 'data')
    assert len(collector.data) > 0
    assert isinstance(collector.data, list)
    print(f"Loaded {len(collector.data)} items")
    print(f"First item: {collector.data[0]}")