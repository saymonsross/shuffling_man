"""Перекладывает текст, набранный не в той раскладке: латиница QWERTY → ЙЦУКЕН и обратно.

python fix_layout.py "ghbdtn"         → привет
python fix_layout.py --to-en "руддщ"  → hello
Без аргументов читает stdin.
"""
import sys

EN = "`qwertyuiop[]asdfghjkl;'zxcvbnm,./~QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?@#$^&"
RU = "ёйцукенгшщзхъфывапролджэячсмитьбю.ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,\"№;:?"
TO_RU = str.maketrans(EN, RU)
TO_EN = str.maketrans(RU, EN)


def main():
    args = sys.argv[1:]
    to_en = "--to-en" in args
    args = [a for a in args if a != "--to-en"]
    text = " ".join(args) if args else sys.stdin.read()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(text.translate(TO_EN if to_en else TO_RU))


if __name__ == "__main__":
    main()
