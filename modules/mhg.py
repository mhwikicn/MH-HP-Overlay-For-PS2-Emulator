import re
from time import time
from math import ceil

from ahk import AHK
import pymem

from modules.utils import read_int, max_monsters, set_initial_pointer
from modules.pcsx2 import get_memory_base_address
from modules.monsters_mh import MonstersMH

initial_pointer = {
    "SLPM-65869": {"hp_pointer": 0x340F42, "game_id_pointer": 0x2E9382},
}


def get_mhg_data(pid, base_address, show_small_monsters=True):
    large_monster_results = []
    small_monster_results = []

    process_handle = pymem.process.open(pid)

    pointer = set_initial_pointer(process_handle, base_address, initial_pointer)

    address = base_address + pointer

    large_monsters = MonstersMH.large_monsters
    small_monsters = MonstersMH.small_monsters if show_small_monsters else {}

    for i in range(0, max_monsters):
        offset = 0xA00 * i
        p0 = address + offset
        if p0 != 0:
            abnormal_status = {}

            def add_abnormal_status(status_name: str, values: list):
                if values[1] != 0xFFFF:
                    abnormal_status.update({
                        status_name: values,
                    })

            name = read_int(process_handle, p0 - 0x300, 1)
            hp = read_int(process_handle, p0)
            max_hp = read_int(process_handle, p0 + 0x490)
            if large_monsters.get(name):
                size = read_int(process_handle, p0 + 0x6F6)
                add_abnormal_status("Poison", [
                    read_int(process_handle, p0 + 0x4B8),
                    read_int(process_handle, p0 + 0x4B6)
                ])
                add_abnormal_status("Sleep", [
                    read_int(process_handle, p0 + 0x4B0),
                    read_int(process_handle, p0 + 0x4AE)
                ])
                add_abnormal_status("Paralysis", [
                    read_int(process_handle, p0 + 0x4C2),
                    read_int(process_handle, p0 + 0x4C0)
                ])
                add_abnormal_status("Tranq", [
                    read_int(process_handle, p0 + 0x4CA),
                    read_int(process_handle, p0 + 0x4C8)
                ])
                abnormal_status.update({
                    "Rage": int(ceil(
                        read_int(process_handle, p0 + 0x5B2) / 60
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
        target_window_title = r"モンスターハンターG"
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

            data = get_mhg_data(win.pid, base_address)
            monsters = data["monsters"]
            for monster in monsters:
                if monster[2] > 5:
                    large_monster = MonstersMH.large_monsters.get(monster[0])
                    small_monster_name = MonstersMH.small_monsters.get(monster[0])
                    if large_monster:
                        print([large_monster["name"], *monster[1::], monster[0]])
                    if small_monster_name:
                        print([small_monster_name, *monster[1::], monster[0]])
        end = time()
        print(end - start)
    Test()
