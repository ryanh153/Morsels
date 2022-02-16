from collections import defaultdict
from typing import List
import re


leading_spaces = re.compile(r'^(\s*).*')
bullet_text = re.compile(r'\s*- (.*)')
print(len(leading_spaces.search('hey').groups()[0]))


class Bullet:
    def __init__(self, string: str) -> None:
        self.bullet_string = string
        self._children = list()

    @property
    def text(self) -> str:
        return bullet_text.search(self.bullet_string).groups()[0]

    def add_child(self, item):
        self._children.append(item)

    @property
    def children(self):
        return self._children

    def __str__(self) -> str:
        return self.bullet_string


def indent_level(string: str) -> int:
    return int(len(leading_spaces.search(string).groups()[0]) / 4)


def parse_bullets(string_data: str) -> List[Bullet]:
    parents = dict()
    bullets = list()

    for bullet_str in string_data.strip().split('\n'):
        level = indent_level(bullet_str)
        if level == 0:
            bullet = Bullet(bullet_str)
            parents[level] = bullet
            bullets.append(bullet)
        else:
            print(f'Looking for {level-1} in {parents}')
            child = Bullet(bullet_str)
            parents[level-1].add_child(child)
            parents[level] = child

    print([b.text for b in bullets])
    return bullets

##

