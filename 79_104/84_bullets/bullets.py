from typing import List
import re


leading_spaces = re.compile(r'^(\s*).*')
bullet_text = re.compile(r'\s*- (.*)')


class Bullet:
    def __init__(self, string: str, parent=None) -> None:
        self.bullet_string = string
        self._children = list()
        self._parent = parent

    @property
    def text(self) -> str:
        return bullet_text.search(self.bullet_string).groups()[0]

    def add_child(self, item):
        self._children.append(item)

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    def __str__(self) -> str:
        string = self.bullet_string.strip()
        if self.children:
            string += '\n' + '\n'.join(f'    {line}' for child in self.children for line in str(child).split('\n'))
        return string


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
            child = Bullet(bullet_str, parent=parents[level-1])
            parents[level-1].add_child(child)
            parents[level] = child

    return bullets
