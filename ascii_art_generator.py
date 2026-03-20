import os
import time
import datetime

# ============================================
#   🎨 ASCII ART GENERATOR
#   by Ankit Sharma, Rohtak
#   Pydroid 3 Compatible - No Libraries!
# ============================================

# Full ASCII font - every letter A-Z + 0-9
FONT = {
    'A': ["  ██  ", " █  █ ", "██████", "█    █", "█    █"],
    'B': ["█████ ", "█    █", "█████ ", "█    █", "█████ "],
    'C': [" ████ ", "█    █", "█     ", "█    █", " ████ "],
    'D': ["████  ", "█   █ ", "█    █", "█   █ ", "████  "],
    'E': ["██████", "█     ", "████  ", "█     ", "██████"],
    'F': ["██████", "█     ", "████  ", "█     ", "█     "],
    'G': [" ████ ", "█     ", "█  ███", "█    █", " ████ "],
    'H': ["█    █", "█    █", "██████", "█    █", "█    █"],
    'I': ["██████", "  ██  ", "  ██  ", "  ██  ", "██████"],
    'J': ["██████", "   █  ", "   █  ", "█  █  ", " ██   "],
    'K': ["█   █ ", "█  █  ", "███   ", "█  █  ", "█   █ "],
    'L': ["█     ", "█     ", "█     ", "█     ", "██████"],
    'M': ["█    █", "██  ██", "█ ██ █", "█    █", "█    █"],
    'N': ["█    █", "██   █", "█ █  █", "█  █ █", "█    █"],
    'O': [" ████ ", "█    █", "█    █", "█    █", " ████ "],
    'P': ["█████ ", "█    █", "█████ ", "█     ", "█     "],
    'Q': [" ████ ", "█    █", "█  █ █", "█   ██", " ██████"],
    'R': ["█████ ", "█    █", "█████ ", "█  █  ", "█    █"],
    'S': [" ████ ", "█     ", " ████ ", "     █", " ████ "],
    'T': ["██████", "  ██  ", "  ██  ", "  ██  ", "  ██  "],
    'U': ["█    █", "█    █", "█    █", "█    █", " ████ "],
    'V': ["█    █", "█    █", "█    █", " █  █ ", "  ██  "],
    'W': ["█    █", "█    █", "█ ██ █", "██  ██", "█    █"],
    'X': ["█    █", " █  █ ", "  ██  ", " █  █ ", "█    █"],
    'Y': ["█    █", " █  █ ", "  ██  ", "  ██  ", "  ██  "],
    'Z': ["██████", "    █ ", "  ██  ", " █    ", "██████"],
    '0': [" ████ ", "█   ██", "█  █ █", "██   █", " ████ "],
    '1': ["  █   ", " ██   ", "  █   ", "  █   ", "██████"],
    '2': [" ████ ", "█    █", "   ██ ", "  █   ", "██████"],
    '3': ["█████ ", "     █", " ████ ", "     █", "█████ "],
    '4': ["█   █ ", "█   █ ", "██████", "    █ ", "    █ "],
    '5': ["██████", "█     ", "█████ ", "     █", "█████ "],
    '6': [" ████ ", "█     ", "█████ ", "█    █", " ████ "],
    '7': ["██████", "    █ ", "   █  ", "  █   ", " █    "],
    '8': [" ████ ", "█    █", " ████ ", "█    █", " ████ "],
    '9': [" ████ ", "█    █", " █████", "     █", " ████ "],
    ' ': ["      ", "      ", "      ", "      ", "      "],
    '!': ["  ██  ", "  ██  ", "  ██  ", "      ", "  ██  "],
    '?': [" ████ ", "█    █", "   ██ ", "      ", "  ██  "],
}

STYLES = {
    "1": ("🔥 FIRE",     "\033[91m",  "▓"),
    "2": ("💎 DIAMOND",  "\033[96m",  "◆"),
    "3": ("⚡ ELECTRIC", "\033[93m",  "▒"),
    "4": ("🌿 MATRIX",   "\033[92m",  "░"),
    "5": ("👑 ROYAL",    "\033[95m",  "█"),
    "6": ("❄️  ICE",      "\033[94m",  "▪"),
}

RESET = "\033[0m"
BOLD  = "\033[1m"

BORDERS = {
    "1": ("╔","═","╗","║","╚","╝"),
    "2": ("┌","─","┐","│","└","┘"),
    "3": ("▛","▀","▜","▌","▙","▄▟"),
    "4": ("★","─","★","│","★","★"),
}

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def slow_print(text, delay=0.03):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def render_ascii(text, fill_char="█"):
    text = text.upper()
    rows = ["", "", "", "", ""]
    for char in text:
        if char in FONT:
            letter = FONT[char]
        else:
            letter = FONT.get(' ', ["      "]*5)
        for i in range(5):
            row = letter[i].replace("█", fill_char)
            rows[i] += row + "  "
    return rows

def add_border(lines, style="1", color=""):
    tl, top, tr, side, bl, br = BORDERS[style]
    width = max(len(l) for l in lines) + 4
    result = []
    result.append(color + tl + top * width + tr + RESET)
    for line in lines:
        padding = width - len(line)
        result.append(color + side + RESET + "  " + line + " " * padding + color + side + RESET)
    result.append(color + bl + top * width + br + RESET)
    return result

def animate_reveal(lines, color):
    for line in lines:
        print(color + line + RESET)
        time.sleep(0.07)

def generate_art():
    clear()
    print(BOLD + "\033[93m")
    slow_print("  ╔══════════════════════════════════╗")
    slow_print("  ║   🎨  ASCII ART GENERATOR  🎨   ║")
    slow_print("  ║      by Ankit Sharma, Rohtak     ║")
    slow_print("  ╚══════════════════════════════════╝" + RESET)
    time.sleep(0.3)

    text = input("\n  📝 Text daalo (naam ya kuch bhi): ").strip()
    if not text:
        print("  ❌ Kuch toh likho!")
        return

    print("\n  🎨 Style chuno:")
    for k, (name, _, _) in STYLES.items():
        print(f"    {k}. {name}")
    style_choice = input("\n  Style number (1-6): ").strip()
    if style_choice not in STYLES:
        style_choice = "1"
    style_name, color, fill = STYLES[style_choice]

    print("\n  🖼️  Border chuno:")
    print("    1. ╔═══╗  Classic")
    print("    2. ┌───┐  Simple")
    print("    3. ▛▀▀▜  Block")
    print("    4. ★───★  Star")
    border_choice = input("\n  Border number (1-4): ").strip()
    if border_choice not in BORDERS:
        border_choice = "1"

    print("\n")
    slow_print("  ⚡ Generating...", 0.05)
    time.sleep(0.5)
    clear()

    # Render
    rows = render_ascii(text, fill)
    bordered = add_border(rows, border_choice, color)

    # Animate reveal
    print("\n")
    animate_reveal(bordered, color)

    # Stats line
    print(f"\n  {BOLD}✨ Style: {style_name}  |  Characters: {len(text)}  |  Width: {max(len(r) for r in rows)}{RESET}")
    print(f"  🕐 Generated: {datetime.datetime.now().strftime('%d %b %Y, %I:%M %p')}")
    print(f"  👤 by Ankit Sharma, Rohtak\n")

def save_art():
    text = input("  📝 Text daalo: ").strip().upper()
    if not text:
        return

    style_choice = input("  Style (1-6): ").strip()
    if style_choice not in STYLES:
        style_choice = "1"
    _, _, fill = STYLES[style_choice]

    rows = render_ascii(text, fill)
    filename = text.replace(" ", "_") + "_art.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("=" * 50 + "\n")
        f.write(f"  ASCII ART: {text}\n")
        f.write(f"  by Ankit Sharma, Rohtak\n")
        f.write(f"  {datetime.datetime.now().strftime('%d %b %Y')}\n")
        f.write("=" * 50 + "\n\n")
        for row in rows:
            f.write(row + "\n")
        f.write("\n" + "=" * 50 + "\n")

    print(f"\n  ✅ Saved: {filename}")

def demo_mode():
    demos = ["ANKIT", "WOW", "ROHTAK", "PYTHON"]
    _, color, fill = STYLES["1"]
    for word in demos:
        clear()
        rows = render_ascii(word, fill)
        bordered = add_border(rows, "1", color)
        print("\n")
        animate_reveal(bordered, color)
        time.sleep(1.2)

def main():
    while True:
        clear()
        print(BOLD + "\033[93m")
        print("  ╔══════════════════════════════════╗")
        print("  ║   🎨  ASCII ART GENERATOR  🎨   ║")
        print("  ║      by Ankit Sharma, Rohtak     ║")
        print("  ╚══════════════════════════════════╝" + RESET)
        print()
        print("  1. 🎨  Art banao")
        print("  2. 💾  Art banao + file save karo")
        print("  3. 🎬  Demo dekho (ANKIT, WOW, ROHTAK...)")
        print("  0. 🚪  Exit")
        print()

        choice = input("  Option chuno: ").strip()

        if choice == "1":
            generate_art()
            input("\n  Enter dabao menu pe jaane ke liye...")
        elif choice == "2":
            clear()
            print(BOLD + "  💾 ART SAVE KARO\n" + RESET)
            save_art()
            input("\n  Enter dabao...")
        elif choice == "3":
            demo_mode()
            input("\n  Enter dabao menu pe jaane ke liye...")
        elif choice == "0":
            print(BOLD + "\033[92m\n  Bye Ankit bhai! Keep creating! 🎨👋\n" + RESET)
            break
        else:
            print("  ❌ Galat option!")
            time.sleep(1)

if __name__ == "__main__":
    main()
