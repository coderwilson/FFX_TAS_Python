from typing import Callable

from ..data.actions import ACTIONS, YOJIMBO_ACTIONS
from ..data.characters import CHARACTERS, Character
from ..data.constants import Stat
from ..data.encounter_formations import BOSSES, SIMULATIONS, ZONES
from ..data.monsters import MONSTERS
from ..errors import EventParsingError
from ..gamestate import GameState
from ..utils import stringify
from .advance_rng import AdvanceRNG
from .change_party import ChangeParty
from .change_stat import ChangeStat
from .character_action import CharacterAction
from .comment import Comment
from .death import Death
from .encounter import (Encounter, MultizoneRandomEncounter, RandomEncounter,
                        SimulatedEncounter)
from .escape import Escape
from .kill import Bribe, Kill
from .main import Event
from .monster_action import MonsterAction
from .steal import Steal
from .yojimbo_turn import YojimboTurn

ParsingFunction = (Callable[[GameState, str], Event]
                   | Callable[[GameState, str, str], Event]
                   | Callable[[GameState, str, str, str], Event]
                   | Callable[..., Event]
                   )


def parse_encounter(gs: GameState,
                    type_: str = '',
                    name: str = '',
                    initiative: str = '',
                    *_,
                    ) -> Encounter:
    match type_:
        case 'boss' | 'optional_boss':
            encounter_type = Encounter
            if name not in BOSSES:
                raise EventParsingError(f'No boss named {name}')
        case 'random':
            encounter_type = RandomEncounter
            if name not in ZONES:
                raise EventParsingError(f'No zone named {name}')
        case 'simulated':
            encounter_type = SimulatedEncounter
            if name not in SIMULATIONS:
                raise EventParsingError(f'No simulation named {name}')
        case 'multizone':
            encounter_type = MultizoneRandomEncounter
            name = name.split('/')
            for zone in name:
                if zone not in ZONES:
                    raise EventParsingError(f'No zone named {name}')
        case _:
            raise EventParsingError(f'Invalid encounter type: {type_}')
    initiative = initiative and 'initiative'.startswith(initiative)
    return encounter_type(gs, name, initiative)


def parse_steal(gs: GameState,
                monster_name: str = '',
                successful_steals: str = '0',
                *_,
                ) -> Steal:
    usage = 'Usage: steal [monster_name] (successful steals)'
    if not monster_name:
        raise EventParsingError(usage)
    try:
        monster = MONSTERS[monster_name]
    except KeyError:
        raise EventParsingError(f'No monster named {monster_name!r}')
    try:
        successful_steals = int(successful_steals)
    except ValueError:
        raise EventParsingError(usage)
    return Steal(gs, monster, successful_steals)


def parse_kill(gs: GameState,
               monster_name: str = '',
               killer_name: str = '',
               overkill: str = '',
               *_,
               ) -> Kill:
    usage = 'Usage: (kill) [monster_name] [killer] (overkill/ok)'
    if not monster_name or not killer_name:
        raise EventParsingError(usage)
    try:
        monster = MONSTERS[monster_name]
    except KeyError as error:
        raise EventParsingError(f'No monster named {error}')
    overkill = overkill in ('overkill', 'ok')
    killer = CHARACTERS.get(killer_name, Character('Unknown', 18))
    return Kill(gs, monster, killer, overkill)


def parse_bribe(gs: GameState,
                monster_name: str = '',
                user_name: str = '',
                *_,
                ) -> Bribe:
    usage = 'Usage: bribe [monster_name] [user]'
    if not monster_name or not user_name:
        raise EventParsingError(usage)
    try:
        monster = MONSTERS[monster_name]
    except KeyError as error:
        raise EventParsingError(f'No monster named {error}')
    killer = CHARACTERS.get(user_name, Character('Unknown', 18))
    return Bribe(gs, monster, killer)


def parse_death(gs: GameState, character_name: str = 'Unknown', *_) -> Death:
    character = CHARACTERS.get(character_name, Character('Unknown', 18))
    return Death(gs, character)


def parse_roll(gs: GameState,
               rng_index: str = '',
               times: str = '1',
               *_,
               ) -> AdvanceRNG:
    usage = 'Usage: waste/advance/roll [rng#] [amount]'
    try:
        if rng_index.startswith('rng'):
            rng_index = int(rng_index[3:])
        else:
            rng_index = int(rng_index)
        times = int(times)
    except ValueError:
        raise EventParsingError(usage)
    if times > 100000:
        raise EventParsingError('Can\'t advance rng more than 100000 times.')
    if not (0 <= rng_index < 68):
        raise EventParsingError(f'Can\'t advance rng index {rng_index}')
    return AdvanceRNG(gs, rng_index, times)


def parse_party_change(gs: GameState,
                       party_formation_string: str = '',
                       *_,
                       ) -> ChangeParty:
    usage = 'Usage: party [party members initials]'
    if not party_formation_string:
        raise EventParsingError(usage)
    party_formation = []
    for character in tuple(CHARACTERS.values())[:7]:
        initial = character.name[0].lower()
        for letter in party_formation_string:
            if initial == letter:
                party_formation.append(character)
                break

    if not party_formation:
        raise EventParsingError(usage)
    return ChangeParty(gs, party_formation)


def parse_summon(gs: GameState,
                 aeon_name: str = '',
                 *_,
                 ) -> ChangeParty:
    usage = 'Usage: summon [aeon name]'
    if not aeon_name:
        raise EventParsingError(usage)
    if 'magus_sisters'.startswith(aeon_name):
        party_formation = [
            CHARACTERS['cindy'], CHARACTERS['sandy'], CHARACTERS['mindy']
            ]
    else:
        for aeon in tuple(CHARACTERS.values())[7:]:
            if aeon.name.lower().startswith(aeon_name):
                party_formation = [aeon]
                break
        else:
            raise EventParsingError(usage)
    return ChangeParty(gs, party_formation)


def parse_action(gs: GameState,
                 character_name: str = '',
                 action_name: str = '',
                 target_name: str = '',
                 *_,
                 ) -> CharacterAction | Escape:
    usage = 'Usage: [character] [action name] (target)'
    if not character_name or not action_name:
        raise EventParsingError(usage)

    if target_name.endswith('_c'):
        try:
            target = gs.characters[target_name[:-2]]
        except KeyError as error:
            raise EventParsingError(f'No character named {error}')
    elif target_name:
        try:
            target = MONSTERS[target_name]
        except KeyError:
            try:
                target = gs.characters[target_name]
            except KeyError as error:
                raise EventParsingError(f'No target named {error}')
    else:
        target = None

    try:
        character = gs.characters[character_name]
    except KeyError:
        raise EventParsingError(f'No character named {character_name}')

    if action_name == 'escape':
        if character.index > 6:
            raise EventParsingError(
                f'Character {character.name!r} can\'t perform action "Escape"'
            )
        return Escape(gs, character)
    else:
        try:
            action = ACTIONS[action_name]
        except KeyError:
            raise EventParsingError(
                f'No action named {action_name!r}'
            )
        if target is None:
            raise EventParsingError(
                f'Action {action.name!r} requires a target.'
            )
        return CharacterAction(gs, character, action, target)


def parse_stat_update(gs: GameState,
                      character_name: str = '',
                      stat_name: str = '',
                      amount: str = '',
                      *_,
                      ) -> ChangeStat:
    usage = 'Usage: stat [character] [stat] [(+/-) amount]'
    if not character_name or not stat_name or not amount:
        raise EventParsingError(usage)
    try:
        character = gs.characters[character_name]
    except KeyError as error:
        raise EventParsingError(f'No character named {error}')
    for stat in Stat:
        if stringify(stat) == stat_name:
            stat_value = character.stats[stat]
            break
    else:
        raise EventParsingError(f'No stat named {stat_name}')
    try:
        if amount.startswith('+'):
            stat_value += int(amount[1:])
        elif amount.startswith('-'):
            stat_value -= int(amount[1:])
        else:
            stat_value = int(amount)
    except ValueError:
        raise EventParsingError('Stat value should be an integer.')
    return ChangeStat(gs, character, stat, stat_value)


def parse_yojimbo_action(gs: GameState,
                         action_name: str = '',
                         monster_name: str = '',
                         overdrive: str = '',
                         *_,
                         ) -> YojimboTurn:
    usage = 'Usage: [action] [monster] (overdrive)'
    if not action_name or not monster_name:
        raise EventParsingError(usage)
    try:
        attack = YOJIMBO_ACTIONS[action_name]
    except KeyError as error:
        raise EventParsingError(f'No action named {error}')

    try:
        monster = MONSTERS[monster_name]
    except KeyError as error:
        raise EventParsingError(f'No monster named {error}')

    overdrive = overdrive == 'overdrive'

    return YojimboTurn(gs, attack, monster, overdrive)


def parse_compatibility_update(gs: GameState,
                               compatibility: str = '',
                               *_,
                               ) -> Comment:
    usage = 'Usage: compatibility [(+/-)amount]'
    try:
        if compatibility.startswith('+'):
            gs.compatibility += int(compatibility[1:])
        elif compatibility.startswith('-'):
            gs.compatibility -= int(compatibility[1:])
        else:
            gs.compatibility = int(compatibility)
    except ValueError:
        raise EventParsingError(usage)

    return Comment(gs, f'Compatibility changed to {gs.compatibility}')


def parse_monster_action(gs: GameState,
                         monster_name: str = '',
                         slot: str = '',
                         action_name: str = '',
                         *_,
                         ) -> MonsterAction:
    usage = 'Usage: monsteraction [monster_name] [slot] [action_name]'
    try:
        monster = MONSTERS[monster_name]
    except KeyError:
        raise EventParsingError(usage)
    try:
        slot = int(slot)
    except ValueError:
        raise EventParsingError('Slot must be an integer')
    if not (1 <= slot <= 8):
        raise EventParsingError('Slot must be between 1 and 8')
    slot -= 1
    try:
        action = monster.actions[action_name]
    except KeyError:
        action_names = ', '.join(str(a) for a in monster.actions.values())
        raise EventParsingError(f'Available actions for {monster.name}: '
                                f'{action_names}')
    return MonsterAction(gs, monster, action, slot)
