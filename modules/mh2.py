import re
from time import time
from math import ceil

from ahk import AHK
import pymem

from modules.utils import read_int, max_monsters, set_initial_pointer
from modules.pcsx2 import get_memory_base_address
from modules.monsters_mh2 import MonstersMH2

initial_pointer = {
    "SLPM-66280": {"hp_pointer": 0x5EC842, "game_id_pointer": 0x4B05C2},
}


def get_mh2_data(pid, base_address, show_small_monsters=True):
    large_monster_results = []
    small_monster_results = []

    process_handle = pymem.process.open(pid)

    pointer = set_initial_pointer(process_handle, base_address, initial_pointer)

    address = base_address + pointer

    large_monsters = MonstersMH2.large_monsters
    small_monsters = MonstersMH2.small_monsters if show_small_monsters else {}

    for i in range(0, max_monsters):
        offset = 0x9D0 * i
        p0 = address + offset
        if p0 != 0:
            abnormal_status = {}

            def add_abnormal_status(status_name: str, values: list):
                if values[1] != 0xFFFF:
                    abnormal_status.update({
                        status_name: values,
                    })

            name = read_int(process_handle, p0 - 0x2C0, 1)
            hp = read_int(process_handle, p0)
            max_hp = read_int(process_handle, p0 + 0x41C)
            if large_monsters.get(name):
                size = read_int(process_handle, p0 + 0x6C2)
                add_abnormal_status("Poison", [
                    read_int(process_handle, p0 + 0x444),
                    read_int(process_handle, p0 + 0x442)
                ])
                add_abnormal_status("Sleep", [
                    read_int(process_handle, p0 + 0x43C),
                    read_int(process_handle, p0 + 0x43A),
                ])
                add_abnormal_status("Paralysis", [
                    read_int(process_handle, p0 + 0x44E),
                    read_int(process_handle, p0 + 0x44C)
                ])
                add_abnormal_status("Dizzy", [
                    read_int(process_handle, p0 + 0x434, 2),
                    read_int(process_handle, p0 + 0x512, 2)
                ])
                abnormal_status.update({
                    "Rage": int(ceil(
                        read_int(process_handle, p0 + 0x546) / 60
                    ))
                })
                large_monster_results.append([name, hp, max_hp, size, abnormal_status, hex(p0)])
            elif small_monsters.get(name) and show_small_monsters:
                small_monster_results.append([name, hp, max_hp, hex(p0)])

    return {
        "monsters": large_monster_results + small_monster_results,
        "total": [len(large_monster_results), len(small_monster_results)]
    }


if __name__ == "__main__":
    class Test:
        start = time()
        ahk = AHK(version="v2")
        keys_regex = "|".join(map(re.escape, initial_pointer.keys()))
        target_window_title = r"モンスターハンター2（dos）"
        not_responding_title = r" \([\w\s]+\)"
        end_regex_title = "$"
        win = None
        not_responding = ahk.find_window(
            title=target_window_title + not_responding_title + end_regex_title, title_match_mode="RegEx"
        )
        if not not_responding:
            win = ahk.find_window(
                title=target_window_title + end_regex_title, title_match_mode="RegEx"
            )

        if win and "pcsx2" in win.process_name:
            base_address = get_memory_base_address(win.pid, win.process_name)

            print("base_address:", hex(base_address))

            data = get_mh2_data(win.pid, base_address)
            monsters = data["monsters"]
            for monster in monsters:
                if monster[2] > 5:
                    large_monster = MonstersMH2.large_monsters.get(monster[0])
                    small_monster_name = MonstersMH2.small_monsters.get(monster[0])
                    if large_monster:
                        print([large_monster["name"], *monster[1::], monster[0]])
                    if small_monster_name:
                        print([small_monster_name, *monster[1::], monster[0]])
        end = time()
        print(end - start)
    Test()
