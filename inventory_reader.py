"""
inventory_reader.py

Parses the confirmed inventory array (goods + weapons + armor), ported
from alfizari/Sekiro-Save-Editor's main_no_ai.py. Unlike event flags,
these offsets are already known and working -- no discovery needed.

Layout: a flat array of 16-byte records starting at 0x8F70C, running for
0x7000 bytes, each record = (gaitem_handle: u32, item_id: u32,
quantity: u32, index: u32), little-endian.

The top nibble of gaitem_handle tells you the item's category:
    0x0 = empty slot
    0x8 = weapon (includes prosthetic tools!)
    0x9 = armor
    0xB = good (includes key items like Lapis Lazuli)
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

INVENTORY_START = 0x8F70C
INVENTORY_LENGTH = 0x7000

# Confirmed from the full GUI editor (sekiro_save_editor_gui.py): goods can
# also live in the Storage box or the Key Items section, not just the
# carried-inventory block above. Same 16-byte record format in all three.
STORAGE_START = 0x987A0
STORAGE_LENGTH = 0x9000

KEY_ITEMS_START = 0x9670C
KEY_ITEMS_LENGTH = 0x2000

RECORD_SIZE = 16

ITEM_TYPE_EMPTY = 0x00000000
ITEM_TYPE_WEAPON = 0x80000000
ITEM_TYPE_ARMOR = 0x90000000
ITEM_TYPE_GOOD = 0xB0000000

ID_MASK = 0x00FFFFFF  # item_id's top byte carries other bits, mask it off


@dataclass
class InventoryRecord:
    gaitem_handle: int
    item_id: int
    quantity: int
    index: int
    offset: int

    @property
    def type_bits(self) -> int:
        return self.gaitem_handle & 0xF0000000

    @property
    def clean_item_id(self) -> int:
        return self.item_id & ID_MASK


def parse_region(slot_data: bytes, start: int, length: int) -> list[InventoryRecord]:
    records = []
    offset = start
    end = start + length
    while offset < end:
        gaitem_handle, item_id, quantity, index = struct.unpack_from("<IIII", slot_data, offset)
        records.append(InventoryRecord(gaitem_handle, item_id, quantity, index, offset))
        offset += RECORD_SIZE
    return records


def parse_inventory(slot_data: bytes) -> list[InventoryRecord]:
    """Carried inventory only. Kept for backwards compatibility -- prefer
    parse_all_goods_regions() when checking whether an item is owned
    anywhere, since goods can also sit in storage or key items."""
    return parse_region(slot_data, INVENTORY_START, INVENTORY_LENGTH)


def parse_all_goods_regions(slot_data: bytes) -> list[InventoryRecord]:
    """Every good/key-item across carried inventory, storage, and the
    key items section combined."""
    return (
        parse_region(slot_data, INVENTORY_START, INVENTORY_LENGTH)
        + parse_region(slot_data, STORAGE_START, STORAGE_LENGTH)
        + parse_region(slot_data, KEY_ITEMS_START, KEY_ITEMS_LENGTH)
    )


def get_good_quantity(slot_data: bytes, item_id: int, include_storage: bool = True) -> int:
    """Total quantity owned of a stackable good (e.g. Lapis Lazuli, id 6400),
    summed across carried inventory + storage + key items by default, since
    a player may have banked some in storage."""
    records = parse_all_goods_regions(slot_data) if include_storage else parse_inventory(slot_data)
    total = 0
    for record in records:
        if record.type_bits == ITEM_TYPE_GOOD and record.clean_item_id == item_id:
            total += record.quantity
    return total


def owns_weapon(slot_data: bytes, item_id: int) -> bool:
    """Whether a weapon-type item (includes prosthetic tools) with this
    item_id exists in carried inventory. Prosthetic tools aren't storable,
    so the main inventory block alone is sufficient here."""
    for record in parse_inventory(slot_data):
        if record.type_bits == ITEM_TYPE_WEAPON and record.clean_item_id == item_id:
            return True
    return False


def owns_armor(slot_data: bytes, item_id: int) -> bool:
    for record in parse_inventory(slot_data):
        if record.type_bits == ITEM_TYPE_ARMOR and record.clean_item_id == item_id:
            return True
    return False
