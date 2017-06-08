#!/usr/bin/python
import copy


WEAKNESSES = {'w': 'a', 'f': 'w', 'e': 'f', 'a': 'e'}

# TODO: implement method vulnerable_to
class Monster(object):
    # __slots__ usage slows down execution with cpython and does not affect pypy
    #__slots__ = ['element', 'rank', 'cost', 'power', 'hp']

    # TODO: for readonly see https://stackoverflow.com/a/4828492

    def __str__(self):
        return self.__repr__()
    def __unicode__(self):
        return unicode(self.__str__())
    def __repr__(self):
        return 'Monster: {0.element}{0.rank} {0.cost}/{0.power}/{0.hp}'.format(self)

    def __bool__(self):
        return self.hp > 0

    # Python2 compatibility
    __nonzero__ = __bool__


class Team(tuple):
    def cost(self):
        return sum(map(lambda x: x.cost, self))

    def __bool__(self):
        for m in self:
            if m:
                return True
        return False

    # Python2 compatibility
    __nonzero__ = __bool__


class AirMonster(Monster):
    element = 'a'


class EarthMonster(Monster):
    element = 'e'


class FireMonster(Monster):
    element = 'f'


class WaterMonster(Monster):
    element = 'w'


class A1(AirMonster):
    rank = 1
    cost = 1000
    power = 8
    hp = 20

class A2(AirMonster):
    rank = 2
    cost = 3900
    power = 6
    hp = 48

class A3(AirMonster):
    rank = 3
    cost = 8000
    power = 12
    hp = 36

class A4(AirMonster):
    rank = 4
    cost = 15000
    power = 26
    hp = 24

class A5(AirMonster):
    rank = 5
    cost = 41000
    power = 20
    hp = 60


class W1(WaterMonster):
    rank = 1
    cost = 1400
    power = 6
    hp = 30

class W2(WaterMonster):
    rank = 2
    cost = 3900
    power = 12
    hp = 24

class W3(WaterMonster):
    rank = 3
    cost = 8000
    power = 24
    hp = 18

class W4(WaterMonster):
    rank = 4
    cost = 18000
    power = 20
    hp = 36

class W5(WaterMonster):
    rank = 5
    cost = 52000
    power = 18
    hp = 78

class E1(EarthMonster):
    rank = 1
    cost = 1300
    power = 4
    hp = 44

class E2(EarthMonster):
    rank = 2
    cost = 2700
    power = 8
    hp = 30

class E3(EarthMonster):
    rank = 3
    cost = 7500
    power = 16
    hp = 26

class E4(EarthMonster):
    rank = 4
    cost = 18000
    power = 10
    hp = 72

class E5(EarthMonster):
    rank = 5
    cost = 54000
    power = 40
    hp = 36

class E6(EarthMonster):
    rank = 6
    cost = 71000
    power = 24
    hp = 72

class F1(FireMonster):
    rank = 1
    cost = 1000
    power = 10
    hp = 16

class F2(FireMonster):
    rank = 2
    cost = 3900
    power = 16
    hp = 18

class F3(FireMonster):
    rank = 3
    cost = 8000
    power = 8
    hp = 54

class F4(FireMonster):
    rank = 4
    cost = 23000
    power = 16
    hp = 52

class F5(FireMonster):
    rank = 5
    cost = 31000
    power = 24
    hp = 42


def power_against(attacker, victim):
    if attacker.element == WEAKNESSES[victim.element]:
        return int(attacker.power*1.5)
    else:
        return attacker.power


def duel(a, b):
    '''Pits two monsters until one is dead'''
    # TODO: unittest for Duel(a,b) == reverse(Duel(b,a))
    # Return instantly if one passed contestant is None
    if not (a and b):
        return
    a_power = power_against(a, b)
    b_power = power_against(b, a)
    while a.hp > 0 and b.hp > 0:
        a.hp -= b_power
        b.hp -= a_power


def battle(team1, team2):
    '''Return copy of teams after battle'''
    t1 = Team(map(lambda x: copy.deepcopy(x), team1))
    t2 = Team(map(lambda x: copy.deepcopy(x), team2))
    i1 = i2 = 0
    while i1 < len(t1) and i2 < len(t2):
        duel(t1[i1], t2[i2])
        if not t1[i1]:
            i1 += 1
        if not t2[i2]:
            i2 += 1
    return (t1, t2)


def compose_team(enemy, cost_limit, max_length, return_first_winner):
    '''Return shortest team that is able to slain enemy team if exists or None'''
    monsters = [A5, W5, E5, F5,
            A4, W4, E4, F4,
            A3, W3, E3, F3,
            A2, W2, E2, F2,
            A1, W1, E1, F1]
    chosen_indices = [0]
    winning_team = None
    while True:
        t = Team([monsters[x]() for x in chosen_indices])
        if t.cost() <= cost_limit:
            t1, e1 = battle(t, enemy)
            if t1:
                winning_team = t
                max_length = len(t)-1
                if (max_length == 0) or return_first_winner:
                    return winning_team
                else:
                    chosen_indices.pop()
                    continue
            elif len(chosen_indices) < max_length:
                chosen_indices.append(0)
                continue
        if chosen_indices[-1] < len(monsters)-1:
            chosen_indices[-1] += 1
            continue
        else:
            last = chosen_indices.pop()
            while (last == len(monsters)-1):
                if chosen_indices:
                    last = chosen_indices.pop()
                else:
                    return winning_team
            chosen_indices.append(last+1)


def compose_team_action(args):
    '''Process "compose_team" action'''
    import re
    enemy_stringlist = re.findall('[AWEF]\d+', args.enemy_team.upper())
    enemy_team = Team([eval(s + '()') for s in enemy_stringlist])
    print('Enemy team:\n%s\n' % str(enemy_team))
    print('Brute forcing team to win.')
    t = compose_team(enemy=enemy_team, cost_limit=args.cost_limit,
            max_length=args.max_length, return_first_winner=args.first)
    if t:
        print('Found winning team:\n%s\n' % str(t))
        print('Battle result:\n%s' % str(battle(t, enemy_team)))
    else:
        exit('Winning is impossible with current constraints')


def parse_args():
    '''Setup argparse'''
    import argparse

    #specifying formatter class did not help to get defaults in help o_O
    parser = argparse.ArgumentParser(description='Cosmos Quest monster battle simulator',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers()
    parser_compose = subparsers.add_parser('compose_team', help='Compose team to beat enemy team')
    parser_compose.add_argument('enemy_team',
            help='Free from string describing enemy team like "F5, A1" or "f3a5e2". Leftmost monster fights first.')
    parser_compose.add_argument('-c', '--cost_limit', type=int, default=10**8,
            help='Maximum allowed cost for composed team (default: %(default)s)')
    parser_compose.add_argument('-f', '--first', action='store_true',
            help="Stop on first found winning team and don't seek for shorter")
    parser_compose.add_argument('-m', '--max_length', type=int,  default=6,
            help='Maximum allowed team length (default: %(default)s)')
    parser_compose.set_defaults(func=compose_team_action)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    args.func(args)
