import logic

def test_plague_halves_life():
    world = logic.World(10, 10)
    sheep = logic.Sheep(0, 0, world)
    
    # Set explicit life length for testing
    sheep.live_length = 20
    world.add_organism(sheep)

    # Trigger plague
    world.trigger_plague()

    # 20 // 2 = 10
    assert sheep.live_length == 10
    assert world.plague_turns_remaining == 2


def test_manual_addition_logic():
    world = logic.World(10, 10)
    
    # Verify tile is free
    assert world.is_tile_free(5, 5) == True

    # Add organism manually
    lynx = logic.Lynx(5, 5, world)
    world.add_organism(lynx)

    # Verify tile is now occupied
    assert world.is_tile_free(5, 5) == False
    
    # Verify it is the correct organism
    org = world.get_organism_at(5, 5)
    assert org is not None
    assert org.sign == 'R'


def test_antelope_flees_from_lynx():
    world = logic.World(10, 10)
    
    # Place Antelope at (5, 5)
    antelope = logic.Antelope(5, 5, world)
    world.add_organism(antelope)

    # Place Lynx at (4, 5) - directly to the left of Antelope
    lynx = logic.Lynx(4, 5, world)
    world.add_organism(lynx)

    # Trigger Antelope action
    antelope.act()

    # The Lynx is at X=4, Antelope is at X=5. 
    # Direction vector is (5 - 4) = 1 in X.
    # Antelope should flee 2 tiles to the right: 5 + (1 * 2) = 7.
    assert antelope.x == 7
    assert antelope.y == 5


def test_antelope_attacks_when_cannot_flee():
    world = logic.World(10, 10)
    
    # Place Antelope at the top-left edge (0, 0)
    antelope = logic.Antelope(0, 0, world)
    
    # Make Antelope super strong so we know it will win the fight
    antelope.power = 100 
    world.add_organism(antelope)

    # Place Lynx right next to it at (1, 0)
    lynx = logic.Lynx(1, 0, world)
    world.add_organism(lynx)

    # Antelope wants to flee left to (-2, 0), but that is out of bounds.
    # Therefore, it must attack the Lynx at (1, 0).
    antelope.act()

    # Antelope wins, moves to the Lynx's position
    assert antelope.x == 1
    assert antelope.y == 0
    assert lynx.is_alive == False

def test_organism_power_and_age_update():
    world = logic.World(5, 5)
    sheep = logic.Sheep(2, 2, world)
    sheep.power = 4
    sheep.live_length = 15
    
    # update() is called at the end of a turn
    sheep.update()
    
    # Power should increase by 1, live length should decrease by 1
    assert sheep.power == 5
    assert sheep.live_length == 14


def test_death_by_old_age():
    world = logic.World(5, 5)
    sheep = logic.Sheep(2, 2, world)
    
    # 1 turn left to live
    sheep.live_length = 1 
    
    # After update, live_length hits 0
    sheep.update()
    
    assert sheep.is_alive == False


def test_reproduction_mechanic():
    world = logic.World(5, 5)
    sheep = logic.Sheep(2, 2, world)
    
    # Sheep needs 8 power to reproduce. Give it exactly 8.
    sheep.power = 8 
    world.add_organism(sheep)
    
    # Initial state: 1 organism in the world
    assert len(world.organisms) == 1
    
    sheep.try_reproduce()
    
    # After reproduction, power is halved (8 // 2 = 4)
    assert sheep.power == 4
    # The world should now have 2 organisms (parent and child)
    assert len(world.organisms) == 2


def test_lynx_wins_combat():
    # Use a 1x2 world to force the Lynx to move exactly onto the Sheep
    small_world = logic.World(1, 2)
    
    lynx = logic.Lynx(0, 0, small_world)
    lynx.power = 6
    small_world.add_organism(lynx)
    
    sheep = logic.Sheep(0, 1, small_world)
    sheep.power = 4
    small_world.add_organism(sheep)
    
    # Lynx has only one adjacent tile (0, 1) to move to
    lynx.act()
    
    assert lynx.x == 0
    assert lynx.y == 1
    assert sheep.is_alive == False


def test_lynx_loses_combat():
    # Use a 1x2 world to force the interaction
    small_world = logic.World(1, 2)
    
    lynx = logic.Lynx(0, 0, small_world)
    lynx.power = 2 # Weak Lynx
    small_world.add_organism(lynx)
    
    sheep = logic.Sheep(0, 1, small_world)
    sheep.power = 10 # Super strong mutant Sheep
    small_world.add_organism(sheep)
    
    # Lynx attacks
    lynx.act()
    
    # Lynx loses and dies, Sheep stays alive
    assert lynx.is_alive == False
    assert sheep.is_alive == True


def test_grass_does_not_move():
    world = logic.World(5, 5)
    grass = logic.Grass(2, 2, world)
    
    # Trigger the action for grass
    grass.act()
    
    # Grass should remain exactly where it was spawned
    assert grass.x == 2
    assert grass.y == 2