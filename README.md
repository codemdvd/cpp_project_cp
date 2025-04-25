# Minimum Consistent DFA — project README

## 1  Build instructions

1. **Enter the source directory**
   ```bash
   cd src
   ```
2. **Compile**  
   The supplied *Makefile* already contains correct include‑/link‑flags for Gecode:
   ```bash
   make          # builds the executable `dfa`
   ```
   Successful build leaves you with `dfa` in the same directory.

---

## 2  Running the solver on a single instance

```bash
./dfa < ../instances/filename.inp > ../out/filename.out
```
* **stdin**  – instance file (`.inp`),
* **stdout** – solution file (`.out`).

> A non‑empty `.out` indicates a DFA was found; an empty (or missing) file means the search exceeded the time‑limit or the instance is inconsistent.

You can manually call the contest‑supplied checker to verify:
```bash
./checker.exe < ../out/filename.out
```
If the checker prints `OK` and `Plotting solution to file tmp.png`, the DFA is correct; it also generates a quick visualisation (`tmp.png`).

---

## 3  Batch mode + diagrams (optional)

`make_diagrams.py` automates the whole pipeline:

```bash
python3 make_diagrams.py \
       --checker ../checker.exe \
       --out ../out \
       --dst ../diagrams
```

1. **Iterates** over every `*.inp` in `../instances/`, runs `dfa`, saves answers into `../out/`.
2. **Checks** each answer with `checker.exe`, prints `OK / NO  GOOD / ERROR …` to the terminal.
3. **Moves** generated `tmp.png` into `../diagrams/<instance>.png` so they never overwrite each other.

Default arguments match the folder names above, so the short form is usually enough:
```bash
python3 make_diagrams.py
```

---

## 4  Troubleshooting

| Symptom                               | Fix |
|---------------------------------------|-----|
| `make` fails with *gecode… not found* | Verify that libgecode‑dev (or self‑built Gecode) is installed and headers are in compiler’s include path. |
| `./dfa` silently produces **empty** `.out` | The search did not find a DFA within the 60 s internal timeout → try a faster machine or check if instance files violate format (same word in both sets). |
| `checker.exe: No such file or directory` | Place the official checker binary in the project root or pass `--checker /path/to/checker.exe` to the Python script. |

---

**Enjoy solving automata puzzles!**

