# Constraint Programming — project README

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


#### Performance note : on my machine the solver finishes 87 / 100 instances within the 60‑second per‑instance limit.
---

## 3  Batch mode + diagrams

in src library you can also find a file batch_runner.py 

```bash
python3 batch_runner.py
```

1. **Iterates** over every `*.inp` in `../instances/`, runs `dfa`, saves answers into `../out/`.
2. **Checks** each answer with `checker.exe`, prints `OK / NO  GOOD / ERROR …` to the terminal.
3. **Moves** generated `tmp.png` into `../diagrams/<instance>.png` so they never overwrite each other.

---

