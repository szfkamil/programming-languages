import logic

def print_board(world: logic.World) -> None:
    """Fetches the 2D character array and prints it to the terminal."""
    board: list = world.get_board()
    
    # Print top border
    top_border: str = "+"
    for i in range(world.width):
        top_border = top_border + "-"
    top_border = top_border + "+"
    print(top_border)

    # Print board rows
    for y in range(world.height):
        row_str: str = "|"
        for x in range(world.width):
            row_str = row_str + board[y][x]
        row_str = row_str + "|"
        print(row_str)

    # Print bottom border
    print(top_border)


def main() -> None:
    # Initialize a 20x10 world
    world = logic.World(20, 10)

    # Add some initial organisms
    world.add_organism(logic.Grass(2, 2, world))
    world.add_organism(logic.Grass(15, 8, world))
    world.add_organism(logic.Sheep(5, 5, world))
    world.add_organism(logic.Sheep(6, 5, world))
    world.add_organism(logic.Lynx(10, 5, world))
    world.add_organism(logic.Antelope(12, 5, world))

    print("=== VIRTUAL ECOSYSTEM SIMULATION ===")
    
    while True:
        print("\n--- Turn: " + str(world.turn) + " ---")
        if world.plague_turns_remaining > 0:
            print(">>> PLAGUE IS ACTIVE! (" + str(world.plague_turns_remaining) + " turns left) <<<")

        print_board(world)

        print("\nOptions:")
        print("[Enter] Next turn")
        print("[p] Trigger Plague")
        print("[a] Add Organism manually")
        print("[q] Quit")
        choice: str = input("Choose action: ")

        if choice == "q":
            print("Exiting simulation.")
            break
            
        elif choice == "p":
            world.trigger_plague()
            print("Plague triggered! Life lengths halved.")
            
        elif choice == "a":
            x_str: str = input("Enter x coordinate: ")
            y_str: str = input("Enter y coordinate: ")
            type_str: str = input("Enter type (S=Sheep, G=Grass, R=Lynx, A=Antelope): ")

            # Simple conversion of digits to strings
            if x_str.isdigit() and y_str.isdigit():
                x: int = int(x_str)
                y: int = int(y_str)

                if world.is_within_bounds(x, y):
                    if world.is_tile_free(x, y):
                        if type_str == "S":
                            world.add_organism(logic.Sheep(x, y, world))
                            print("Sheep added.")
                        elif type_str == "G":
                            world.add_organism(logic.Grass(x, y, world))
                            print("Grass added.")
                        elif type_str == "R":
                            world.add_organism(logic.Lynx(x, y, world))
                            print("Lynx added.")
                        elif type_str == "A":
                            world.add_organism(logic.Antelope(x, y, world))
                            print("Antelope added.")
                        else:
                            print("Error: Unknown organism type!")
                    else:
                        print("Error: Tile is already occupied!")
                else:
                    print("Error: Coordinates out of bounds!")
            else:
                print("Error: Coordinates must be numbers!")
                
        else:
            # Default action: process the next turn
            world.do_turn()

if __name__ == "__main__":
    main()