# cosmos-quest-battle-simulator
Simulator of monster battles in http://www.kongregate.com/games/GaiaByte/cosmos-quest

Can simulate battle between given monster teams and compose team within given cost and number of monsters contraints to beat given enemy.

# Usage
Example:
```
$ ./monsters.py compose_team --cost_limit=47826 'W3,E3,W3,E3,W3,E3'
Enemy team:
(Monster: w3 8000/24/18, Monster: e3 7500/16/26, Monster: w3 8000/24/18, Monster: e3 7500/16/26, Monster: w3 8000/24/18, Monster: e3 7500/16/26)

Brute forcing team to win.
Found winning team:
(Monster: a3 8000/12/36, Monster: w3 8000/24/18, Monster: w4 18000/20/36, Monster: f3 8000/8/54)

Battle result:
((Monster: a3 8000/12/-12, Monster: w3 8000/24/-22, Monster: w4 18000/20/-20, Monster: f3 8000/8/6), (Monster: w3 8000/24/0, Monster: e3 7500/16/-10, Monster: w3 8000/24/-6, Monster: e3 7500/16/-14, Monster: w3 8000/24/-2, Monster: e3 7500/16/-10))
```

Note that script is self-documented (try `./monsters.py --help`, `./monsters.py compose_team --help`)

**Monster are always written left-to-right** In other words first monster that gets a turn is written leftmost. Note that this is defferent from monster order in the game, which shows user monsters in reversed order.

# Performance
Defenitely needs tweaking. Current speed measurements:
![Graph of current performance](benchmark/current_performance.svg?raw=true)
apparently running the simulation via `pypy` is preferable.
