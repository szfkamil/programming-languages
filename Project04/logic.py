import random

class World:
    """
    Represents the 2D simulation world.
    Holds all organisms and manages turn execution.
    """

    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.organisms: list = []
        self.turn: int = 0
        self.plague_turns_remaining: int = 0

    def add_organism(self, org) -> None:
        """Add an organism to the world."""
        self.organisms.append(org)

    def get_organism_at(self, x: int, y: int):
        """Return the living organism at (x, y), or None if the tile is empty."""
        for i in range(len(self.organisms)):
            org = self.organisms[i]
            if org.is_alive and org.x == x and org.y == y:
                return org
        return None

    def is_tile_free(self, x: int, y: int) -> bool:
        """Return True if no living organism occupies (x, y)."""
        return self.get_organism_at(x, y) is None

    def is_within_bounds(self, x: int, y: int) -> bool:
        """Return True if (x, y) is inside the world grid."""
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def trigger_plague(self) -> None:
        """
        Plague Feature:
        Immediately halves the liveLength (integer division) of every living
        organism. The plague status flag lasts for 2 turns (visual indicator
        only). Organisms born AFTER this call are not retroactively affected.
        """
        self.plague_turns_remaining = 2
        for i in range(len(self.organisms)):
            org = self.organisms[i]
            if org.is_alive:
                org.live_length = org.live_length // 2

    def do_turn(self) -> None:
        """
        Advance the simulation by one turn.
        1. Increment turn counter.
        2. Sort organisms by initiative descending (bubble sort).
        3. Each alive organism acts, then updates its own stats.
        4. Remove dead organisms.
        5. Decrement plague countdown.
        """
        self.turn = self.turn + 1

        # --- Step 2: Sort by initiative descending (bubble sort) ---
        n: int = len(self.organisms)
        for i in range(n):
            for j in range(n - i - 1):
                if self.organisms[j].initiative < self.organisms[j + 1].initiative:
                    temp = self.organisms[j]
                    self.organisms[j] = self.organisms[j + 1]
                    self.organisms[j + 1] = temp

        # --- Step 3: Collect snapshot of organisms that will act this turn ---
        # New organisms added via reproduction must NOT act in the turn they are born.
        acting_organisms: list = []
        for i in range(len(self.organisms)):
            if self.organisms[i].is_alive:
                acting_organisms.append(self.organisms[i])

        for i in range(len(acting_organisms)):
            org = acting_organisms[i]
            if org.is_alive:
                org.act()
                org.update()

        # --- Step 4: Remove dead organisms ---
        new_organisms: list = []
        for i in range(len(self.organisms)):
            if self.organisms[i].is_alive:
                new_organisms.append(self.organisms[i])
        self.organisms = new_organisms

        # --- Step 5: Decrement plague countdown ---
        if self.plague_turns_remaining > 0:
            self.plague_turns_remaining = self.plague_turns_remaining - 1

    def get_board(self) -> list:
        """
        Return a 2D list of characters representing the current world state.
        '.' means empty. Each organism's sign fills its cell.
        board[y][x] is the character at column x, row y.
        """
        board: list = []
        for y in range(self.height):
            row: list = []
            for x in range(self.width):
                row.append('.')
            board.append(row)

        for i in range(len(self.organisms)):
            org = self.organisms[i]
            if org.is_alive:
                board[org.y][org.x] = org.sign

        return board


class Organism:
    """
    Base class for all organisms in the simulation.
    Subclasses must override act() and create_new_instance().
    """

    def __init__(self, power: int, initiative: int, live_length: int,
                 power_to_reproduce: int, sign: str, x: int, y: int, world: World):
        self.power: int = power
        self.initiative: int = initiative
        self.live_length: int = live_length
        self.power_to_reproduce: int = power_to_reproduce
        self.sign: str = sign
        self.x: int = x
        self.y: int = y
        self.world: World = world
        self.is_alive: bool = True

    def get_adjacent_positions(self) -> list:
        """
        Return all valid (x, y) positions adjacent to this organism
        (4-directional: left, right, up, down).
        """
        directions: list = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        result: list = []
        for i in range(len(directions)):
            dx: int = directions[i][0]
            dy: int = directions[i][1]
            nx: int = self.x + dx
            ny: int = self.y + dy
            if self.world.is_within_bounds(nx, ny):
                result.append((nx, ny))
        return result

    def get_free_adjacent_positions(self) -> list:
        """Return all adjacent positions that have no living organism on them."""
        adjacent: list = self.get_adjacent_positions()
        free: list = []
        for i in range(len(adjacent)):
            nx: int = adjacent[i][0]
            ny: int = adjacent[i][1]
            if self.world.is_tile_free(nx, ny):
                free.append((nx, ny))
        return free

    def try_reproduce(self) -> None:
        """
        If power >= power_to_reproduce, spawn a new child organism on a random
        free adjacent tile and halve this organism's power (integer division).
        """
        if self.power >= self.power_to_reproduce:
            free_tiles: list = self.get_free_adjacent_positions()
            if len(free_tiles) > 0:
                idx: int = random.randint(0, len(free_tiles) - 1)
                nx: int = free_tiles[idx][0]
                ny: int = free_tiles[idx][1]
                new_org = self.create_new_instance(nx, ny)
                if new_org is not None:
                    self.world.add_organism(new_org)
                    self.power = self.power // 2

    def create_new_instance(self, x: int, y: int):
        """
        Factory method. Subclasses must override this to return a new
        instance of themselves at position (x, y).
        """
        return None

    def act(self) -> None:
        """
        Called once per turn before update(). Subclasses override this
        with their specific behavior (movement, combat, reproduction, etc.).
        """
        pass

    def update(self) -> None:
        """
        Called once per turn after act().
        Increments power by 1 and decrements live_length by 1.
        Marks the organism as dead if live_length reaches 0.
        """
        self.power = self.power + 1
        self.live_length = self.live_length - 1
        if self.live_length <= 0:
            self.is_alive = False


class Grass(Organism):
    """
    Grass (sign 'G').
    Does not move. Reproduces when power is sufficient.
    """

    def __init__(self, x: int, y: int, world: World):
        super().__init__(
            power=1,
            initiative=0,
            live_length=20,
            power_to_reproduce=3,
            sign='G',
            x=x,
            y=y,
            world=world
        )

    def create_new_instance(self, x: int, y: int):
        return Grass(x, y, self.world)

    def act(self) -> None:
        """Grass only tries to reproduce. It never moves."""
        self.try_reproduce()


class Sheep(Organism):
    """
    Sheep (sign 'S').
    Moves to a random free adjacent tile each turn.
    """

    def __init__(self, x: int, y: int, world: World):
        super().__init__(
            power=4,
            initiative=2,
            live_length=15,
            power_to_reproduce=8,
            sign='S',
            x=x,
            y=y,
            world=world
        )

    def create_new_instance(self, x: int, y: int):
        return Sheep(x, y, self.world)

    def act(self) -> None:
        """Move to a random free adjacent tile, then try to reproduce."""
        free_tiles: list = self.get_free_adjacent_positions()
        if len(free_tiles) > 0:
            idx: int = random.randint(0, len(free_tiles) - 1)
            self.x = free_tiles[idx][0]
            self.y = free_tiles[idx][1]
        self.try_reproduce()


class Lynx(Organism):
    """
    Lynx / Rys (sign 'R').
    Moves to a random adjacent tile. If that tile has an organism, the one
    with higher power survives; attacker wins on a tie.
    """

    def __init__(self, x: int, y: int, world: World):
        super().__init__(
            power=6,
            initiative=5,
            live_length=18,
            power_to_reproduce=14,
            sign='R',
            x=x,
            y=y,
            world=world
        )

    def create_new_instance(self, x: int, y: int):
        return Lynx(x, y, self.world)

    def act(self) -> None:
        """
        Pick a random adjacent tile (occupied or free).
        If occupied, resolve combat: higher power wins; attacker wins on tie.
        Then try to reproduce if still alive.
        """
        adjacent: list = self.get_adjacent_positions()
        if len(adjacent) == 0:
            return

        idx: int = random.randint(0, len(adjacent) - 1)
        nx: int = adjacent[idx][0]
        ny: int = adjacent[idx][1]
        target = self.world.get_organism_at(nx, ny)

        if target is None:
            # Tile is empty, just move.
            self.x = nx
            self.y = ny
        else:
            # Combat: attacker wins if power is equal or higher.
            if self.power >= target.power:
                target.is_alive = False
                self.x = nx
                self.y = ny
            else:
                # Defender has strictly higher power, attacker dies.
                self.is_alive = False

        if self.is_alive:
            self.try_reproduce()


class Antelope(Organism):
    """
    Antelope / Antylopa (sign 'A').
    Before moving, checks adjacent tiles for a Lynx ('R').
    If a Lynx is found: flees 2 tiles in the exact opposite direction.
    If fleeing is impossible (out of bounds or blocked): attacks the Lynx.
    Otherwise: moves like a Sheep (random free adjacent tile).
    """

    def __init__(self, x: int, y: int, world: World):
        super().__init__(
            power=4,
            initiative=3,
            live_length=11,
            power_to_reproduce=5,
            sign='A',
            x=x,
            y=y,
            world=world
        )

    def create_new_instance(self, x: int, y: int):
        return Antelope(x, y, self.world)

    def act(self) -> None:
        """
        1. Scan adjacent tiles for a Lynx.
        2. If Lynx found: attempt to flee 2 tiles in the opposite direction.
           If fleeing fails: attack the Lynx (same combat rules as Lynx).
        3. If no Lynx: move to a random free adjacent tile.
        4. Try to reproduce if still alive.
        """
        # --- Step 1: Look for an adjacent Lynx ---
        adjacent: list = self.get_adjacent_positions()
        lynx_found = None
        for i in range(len(adjacent)):
            nx: int = adjacent[i][0]
            ny: int = adjacent[i][1]
            candidate = self.world.get_organism_at(nx, ny)
            if candidate is not None and candidate.sign == 'R' and candidate.is_alive:
                lynx_found = candidate
                break  # React to the first Lynx spotted.

        if lynx_found is not None:
            # --- Step 2a: Calculate flee direction (away from Lynx) ---
            raw_dx: int = self.x - lynx_found.x
            raw_dy: int = self.y - lynx_found.y

            # Normalize to -1, 0, or 1.
            flee_dx: int = 0
            flee_dy: int = 0
            if raw_dx > 0:
                flee_dx = 1
            elif raw_dx < 0:
                flee_dx = -1
            if raw_dy > 0:
                flee_dy = 1
            elif raw_dy < 0:
                flee_dy = -1

            flee_x: int = self.x + flee_dx * 2
            flee_y: int = self.y + flee_dy * 2

            can_flee: bool = (
                self.world.is_within_bounds(flee_x, flee_y) and
                self.world.is_tile_free(flee_x, flee_y)
            )
 
            if can_flee:
                self.x = flee_x
                self.y = flee_y
            else:
                # --- Step 2b: Fleeing impossible -> attack the Lynx ---
                if self.power >= lynx_found.power:
                    # Antelope wins the fight.
                    lynx_found.is_alive = False
                    self.x = lynx_found.x
                    self.y = lynx_found.y
                else:
                    # Lynx wins the fight.
                    self.is_alive = False

        else:
            # --- Step 3: Normal Sheep-like movement ---
            free_tiles: list = self.get_free_adjacent_positions()
            if len(free_tiles) > 0:
                idx: int = random.randint(0, len(free_tiles) - 1)
                self.x = free_tiles[idx][0]
                self.y = free_tiles[idx][1]

        # --- Step 4: Reproduction (only if still alive) ---
        if self.is_alive:
            self.try_reproduce()
