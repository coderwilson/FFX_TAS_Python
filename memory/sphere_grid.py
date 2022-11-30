import logging
from enum import Enum

from memory.main import read_val

logger = logging.getLogger(__name__)


class SphereNodeType(Enum):
    Lvl3Lock = 0x00
    Empty = 0x01
    Strength1 = 0x02
    Strength2 = 0x03
    Strength3 = 0x04
    Strength4 = 0x05
    Defense1 = 0x06
    Defense2 = 0x07
    Defense3 = 0x08
    Defense4 = 0x09
    Magic1 = 0x0A
    Magic2 = 0x0B
    Magic3 = 0x0C
    Magic4 = 0x0D
    MagicDef1 = 0x0E
    MagicDef2 = 0x0F
    MagicDef3 = 0x10
    MagicDef4 = 0x11
    Agility1 = 0x12
    Agility2 = 0x13
    Agility3 = 0x14
    Agility4 = 0x15
    Luck1 = 0x16
    Luck2 = 0x17
    Luck3 = 0x18
    Luck4 = 0x19
    Evasion1 = 0x1A
    Evasion2 = 0x1B
    Evasion3 = 0x1C
    Evasion4 = 0x1D
    Accuracy1 = 0x1E
    Accuracy2 = 0x1F
    Accuracy3 = 0x20
    Accuracy4 = 0x21
    HP200 = 0x22
    HP300 = 0x23
    MP40 = 0x24
    MP20 = 0x25
    MP10 = 0x26
    Lvl1Lock = 0x27
    Lvl2Lock = 0x28
    Lvl4Lock = 0x29
    # Abilities
    DelayAttack = 0x2A
    DelayBuster = 0x2B
    SleepAttack = 0x2C
    SilenceAttack = 0x2D
    DarkAttack = 0x2E
    ZombieAttack = 0x2F
    SleepBuster = 0x30
    SilenceBuster = 0x31
    DarkBuster = 0x32
    TripleFoul = 0x33
    PowerBreak = 0x34
    MagicBreak = 0x35
    ArmorBreak = 0x36
    MentalBreak = 0x37
    Mug = 0x38
    QuickHit = 0x39
    Steal = 0x3A
    Use = 0x3B
    Flee = 0x3C
    Pray = 0x3D
    Cheer = 0x3E
    Focus = 0x3F
    Reflex = 0x40
    Aim = 0x41
    Luck = 0x42
    Jinx = 0x43
    Lancet = 0x44
    Guard = 0x45
    Sentinel = 0x46
    SpareChange = 0x47
    Threaten = 0x48
    Provoke = 0x49
    Entrust = 0x4A
    Copycat = 0x4B
    DoubleCast = 0x4C
    Bribe = 0x4D
    Cure = 0x4E
    Cura = 0x4F
    Curaga = 0x50
    NulFrost = 0x51
    NulBlaze = 0x52
    NulShock = 0x53
    NulTide = 0x54
    Scan = 0x55
    Esuna = 0x56
    Life = 0x57
    FullLife = 0x58
    Haste = 0x59
    Hastega = 0x5A
    Slow = 0x5B
    Slowga = 0x5C
    Shell = 0x5D
    Protect = 0x5E
    Reflect = 0x5F
    Dispel = 0x60
    Regen = 0x61
    Holy = 0x62
    AutoLife = 0x63
    Blizzard = 0x64
    Fire = 0x65
    Thunder = 0x66
    Water = 0x67
    Fira = 0x68
    Blizzara = 0x69
    Thundara = 0x6A
    Watera = 0x6B
    Firaga = 0x6C
    Blizzaga = 0x6D
    Thundaga = 0x6E
    Waterga = 0x6F
    Bio = 0x70
    Demi = 0x71
    Death = 0x72
    Drain = 0x73
    Osmose = 0x74
    Flare = 0x75
    Ultima = 0x76
    PilferGil = 0x77
    FullBreak = 0x78
    ExtractPower = 0x79
    ExtractMana = 0x7A
    ExtractSpeed = 0x7B
    ExtractAbility = 0x7C
    NabGil = 0x7D
    QuickPockets = 0x7E


class SphereGridNode:
    _NODE_TYPE_OFFSET = 0  # 1 byte value, matches the SphereNodeType Enum
    _ACTIVATED_BY_OFFSET = 1  # 1 byte value, bitfield where each bit indicates that a character has grabbed the node
    # The bitfield should match the character IDs, so bit[0] = Tidus, bit[1] = Yuna etc.

    def __init__(self, offset: int) -> None:
        self.offset = offset

    def get_node_type(self) -> SphereNodeType:
        """Return an enum of type SphereNodeType that can be compared, or printed with .name"""
        node_type = read_val(self.offset + self._NODE_TYPE_OFFSET, 1)  # 2
        return SphereNodeType(node_type)

    def get_activated_by(self) -> int:
        """This returns a one byte bitfield, where each bit indicates that a character has activated this node."""
        return read_val(self.offset + self._ACTIVATED_BY_OFFSET, 1)

    def is_activated_by(self, character_id: int) -> bool:
        """This checks if a specific bit in the bitfield is set or not."""
        activated_by = self.get_activated_by()
        bitmask = 1 << character_id
        return (activated_by & bitmask) != 0

    def __repr__(self) -> str:
        node_type = self.get_node_type()
        return node_type.name


class SphereGrid:
    _SPHERE_GRID_NODES_OFFSET = (
        0x00D2EC7C  # Base offset to sphere grid (taken from CSR)
    )
    _SPHERE_GRID_NODE_SIZE = 2  # Size in bytes of a single node (taken from CSR)
    _NUM_NODES = 860  # Should be 860 for standard grid

    _TIDUS_POS_OFFSET = 0x012BE93C
    _PLAYER_POS_SPACING = 0x50

    _CURRENT_NODE_OFFSET = 0x012BEB6C

    def __init__(self) -> None:
        """Load up all sphere grid nodes and put them in self.nodes"""
        self.nodes = [
            SphereGridNode(self._get_node_offset(node_idx))
            for node_idx in range(self._NUM_NODES)
        ]

    def _get_node_offset(self, node_idx: int) -> int:
        return self._SPHERE_GRID_NODES_OFFSET + self._SPHERE_GRID_NODE_SIZE * node_idx

    def _get_current_node_offset(self) -> int:
        return self._CURRENT_NODE_OFFSET

    def _get_player_node_offset(self, index: int) -> int:
        return self._TIDUS_POS_OFFSET + index * self._PLAYER_POS_SPACING

    def get_player_node_idx(self, index: int) -> int:
        """Get the index of the node where a specific player is located"""
        return read_val(self._get_player_node_offset(index), 4)

    def get_current_node_idx(self) -> int:
        """Get the index of the currently selected node in the sphere grid"""
        return read_val(self._get_current_node_offset(), 4)

    def get_current_node(self) -> SphereGridNode:
        """Get the currently selected node"""
        return self.nodes[self.get_current_node_idx()]

    def get_node_at(self, index: int) -> SphereGridNode:
        """Get a specific node given an index"""
        return self.nodes[index]


# Instantiation of sphere grid. Can be used to read out nodes
sphere_grid = SphereGrid()
