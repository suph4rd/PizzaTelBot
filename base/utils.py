from aiogram.fsm.storage.memory import MemoryStorage


def get_storage() -> MemoryStorage:
    from main import storage
    return storage
