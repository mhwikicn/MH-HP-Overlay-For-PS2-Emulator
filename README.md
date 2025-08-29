<h1 align="center">MH-HP-Overlay-For-PS2-Emulator</h1>

<div align="center">

  [![StaticBadge](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
  [![App](https://img.shields.io/badge/App-1.0.0-green)](https://github.com/Alexander-Lancellott/MH-HP-Overlay-For-PS2-Emulator)

</div>

## Description

A simple open-source HP overlay that I've developed for MH/G/2 in Python. This project is a port of another one I previously created called [MH-HP-Overlay-For-PSP-Emulator](https://github.com/Alexander-Lancellott/MH-HP-Overlay-For-PSP-Emulator), but this time it's designed to work with PS2 emulator, [PCSX2](https://pcsx2.net/), on their PC (Windows) versions.

You can support me by donating! I’d really appreciate it. But either way, thank you for using this mod!

<a href='https://ko-fi.com/B0B115WKYH' target='_blank'>
  <img height='45' style='border:0px;height:45px;' src='https://storage.ko-fi.com/cdn/kofi2.png?v=6' border='0' alt='Buy Me a Coffee at ko-fi.com' />
</a>

## Compatibility

Tested on **PCSX2 v2.5.112**. This overlay only works properly on **versions 2.0.0 and above**.

- **MH (USA/EUR/JPN)** - SLES-52707 - SLUS-20896 - SLPM-65495
- **MHG (JPN)** - SLPM-65869
- **MH2 (JPN)** - SLPM-66280

## High DPI Scaling (optional, only if you notice it)

If your monitor has a resolution higher than 1080p, it's likely you're using a DPI scale above 100%. In this case, the initial position of the overlay may not be the same as when using 100% scaling. To mitigate this, you have three options:

- Set your screen scaling to 100%. You can follow this [guide](https://support.microsoft.com/en-us/windows/view-display-settings-in-windows-37f0e05e-98a9-474c-317a-e85422daa8bb).

- If setting your monitor’s scaling to 100% is not ideal for you, then disable automatic DPI scaling for PPSSPP. To do this, right-click on `pcsx2.exe`, select Properties, then go to the Compatibility tab. You'll see a checkbox that says, **"Override high DPI scaling behavior."** A drop-down menu will let you choose one of three options. Select `System` or `System Enhanced`. You can find a helpful guide [here](https://www.majorgeeks.com/content/page/how_to_change_dpi_scaling_settings_in_windows.html).

- If neither of the previous options suits you, use the [Fix X & Fix Y](#fix-x--fix-y) options to adjust the overlay more precisely and correct the slight misalignment.
