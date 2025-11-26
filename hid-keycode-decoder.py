#!/usr/bin/env python3
# decode_hid.py
# Usage: python3 decode_hid.py file.bin

import sys

# Minimal HID usage -> character map for keycodes 0x04..0x38 (letters, digits, common punctuation)
hid_map = {
    # letters
    0x04: 'a',0x05: 'b',0x06: 'c',0x07: 'd',0x08: 'e',0x09: 'f',0x0A: 'g',0x0B: 'h',
    0x0C: 'i',0x0D: 'j',0x0E: 'k',0x0F: 'l',0x10: 'm',0x11: 'n',0x12: 'o',0x13: 'p',
    0x14: 'q',0x15: 'r',0x16: 's',0x17: 't',0x18: 'u',0x19: 'v',0x1A: 'w',0x1B: 'x',
    0x1C: 'y',0x1D: 'z',
    # numbers (top row)
    0x1E: '1',0x1F: '2',0x20: '3',0x21: '4',0x22: '5',0x23: '6',0x24: '7',0x25: '8',
    0x26: '9',0x27: '0',
    # enter/esc/backspace/tab/space
    0x28: '<ENTER>', 0x29: '<ESC>', 0x2A: '<BACKSPACE>', 0x2B: '<TAB>',
    0x2C: ' ',
    # punctuation common
    0x2D: '-', 0x2E: '=', 0x2F: '[', 0x30: ']', 0x31: '\\', 0x33: ';', 0x34: '\'', 
    0x35: '`', 0x36: ',', 0x37: '.', 0x38: '/',
    # function keys / others can be added if needed
}

# Shifted symbol map when shift modifier active (for digits/keys)
shift_map = {
    '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
    '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|', ';': ':', "'": '"', '`': '~', ',': '<', '.': '>', '/': '?'
}

# HID modifiers bits (bit mask)
MOD_LCTRL  = 0x01
MOD_LSHIFT = 0x02
MOD_LALT   = 0x04
MOD_LMETA  = 0x08
MOD_RCTRL  = 0x10
MOD_RSHIFT = 0x20
MOD_RALT   = 0x40
MOD_RMETA  = 0x80

def decode_pairs(data, mode='lowkey'):
    # mode 'lowkey': bytes are [key, mod] pairs? here we interpret as little-endian words where low byte is key
    # mode 'highkey': swapped: high byte is key
    out = []
    # parse as 16-bit words (little-endian)
    for i in range(0, len(data), 2):
        if i+1 >= len(data):
            break
        b0 = data[i]
        b1 = data[i+1]
        if mode == 'lowkey':
            key = b0
            mod = b1
        else:
            key = b1
            mod = b0
        out.append((i, key, mod))
    return out

def key_to_char(key, mod):
    if key == 0x00:
        return None
    ch = hid_map.get(key)
    shift = (mod & MOD_LSHIFT) or (mod & MOD_RSHIFT)
    if ch is None:
        return f'<KC_{key:02x}>'
    if ch == '<ENTER>' or ch == '<TAB>' or ch == '<BACKSPACE>' or ch == '<ESC>':
        return ch
    if shift:
        if ch in shift_map:
            return shift_map[ch]
        # letters become uppercase
        if 'a' <= ch <= 'z':
            return ch.upper()
    return ch

def render(decoded):
    # produce a text-like stream
    out = []
    for off, key, mod in decoded:
        ch = key_to_char(key, mod)
        if ch is None:
            continue
        out.append((off, key, mod, ch))
    return out

def pretty_print(stream, title):
    print("="*40)
    print(title)
    print("="*40)
    for off, key, mod, ch in stream:
        print(f"0x{off:06x}: key=0x{key:02x} mod=0x{mod:02x} -> {ch}")
    # quick line of reconstructed string (joining printable)
    text = []
    for _, _, _, ch in stream:
        if len(ch) == 1:
            text.append(ch)
        else:
            # show special tokens in brackets
            text.append(f'[{ch}]')
    print("\nReconstructed (best-effort):\n" + "".join(text))
    print()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 decode_hid.py file.bin")
        return
    fn = sys.argv[1]
    data = open(fn, "rb").read()
    # try two modes
    d_low = decode_pairs(data, mode='lowkey')
    d_high = decode_pairs(data, mode='highkey')

    s_low = render(d_low)
    s_high = render(d_high)

    print(f"File: {fn}  size={len(data)} bytes")
    pretty_print(s_low, "Decoded as (low-byte = key, high-byte = modifier)")
    pretty_print(s_high, "Decoded as (high-byte = key, low-byte = modifier)")

if __name__ == "__main__":
    main()
