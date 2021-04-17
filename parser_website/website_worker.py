from actors_interface import game_info


def main():
    for i in range(1, 20):
        game_info.send(f"https://www.igromania.ru/games/all/all/all/all/all/0/{i}/")


if __name__ == "__main__":
    main()