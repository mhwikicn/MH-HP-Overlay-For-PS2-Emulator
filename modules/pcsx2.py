import pymem
import pefile
from modules.utils import read_int


def get_memory_base_address(pid, process_name):
    process_handle = pymem.process.open(pid)
    module = pymem.process.module_from_name(process_handle, process_name)
    base = module.lpBaseOfDll

    # Parse PE only for the Export Table
    pe = pefile.PE(module.filename, fast_load=True)
    pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT']])

    # Find EEmem using a generator
    eemem_rva = next(
        (exp.address for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols
         if exp.name and exp.name.decode() == "EEmem"),
        None
    )

    if eemem_rva is None:
        raise Exception("EEmem no encontrado en exports")

    # Actual address in memory
    eemem = base + eemem_rva

    return read_int(process_handle, eemem, 8)
