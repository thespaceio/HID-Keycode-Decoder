# HID Keycode Decoder

A lightweight Python utility to decode raw HID (Human Interface Device) keyboard reports from binary capture files. This script helps reconstruct typed text from raw USB HID keystroke data, often found in forensic captures, packet dumps, or embedded device logs.

## 📌 What It Does

Many USB keyboards communicate using **HID reports**—small packets containing a modifier byte (e.g., Shift, Ctrl) and a keycode byte. This tool:
- Parses binary files as sequences of 2-byte HID reports.
- Tries two common byte-order interpretations:
  - **Low-byte = keycode**, high-byte = modifier
  - **High-byte = keycode**, low-byte = modifier
- Maps keycodes (0x04–0x38) to their corresponding ASCII characters.
- Applies shift logic (e.g., `1` → `!`, `a` → `A`).
- Outputs both a detailed hex dump and a reconstructed best-effort text string.

Ideal for analyzing keylog dumps, CTF challenges, or reverse-engineering embedded USB traffic.

## 🚀 Usage

```bash
python3 decode_hid.py capture.bin
```

The script will display two interpretations of the data and attempt to reconstruct readable text, including handling of:

- Letters (a–z)
- Digits (0–9)
- Common punctuation (-, =, [, ], ;, ', etc.)
- Shift-modified symbols (!, @, _, {, :, etc.)
- Special keys: <ENTER>, <TAB>, <BACKSPACE>, <ESC>, and space

##🔧 Requirements
- Python 3.x
- No external dependencies
