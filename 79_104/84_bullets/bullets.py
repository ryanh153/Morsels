import re


leading_spaces = re.compile(r'^(\s*).*')
bullet_text = re.compile(r'\s*- (.*)')


class Bullet:
    def __init__(self, string: str, parent=None) -> None:
        self.bullet_string = string
        self._children = BulletList()
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

    def filter(self, string):
        if not self.children:
            return self.no_child_filter(string)
        return self.with_child_filter(string)

    def no_child_filter(self, string):
        """If we have no children just check ourselves"""
        if string in str(self).lower():
            return self
        return None

    def with_child_filter(self, string):
        """Otherwise, return a copy of ourselves with only children that match"""
        copy = Bullet(self.bullet_string, parent=self.parent)
        for child in self.children:
            if filtered_child := child.filter(string):
                copy.add_child(filtered_child)
        if string in self.bullet_string.lower() or len(copy.children):
            return copy
        return None

    def __str__(self) -> str:
        string = self.bullet_string.strip()
        if self.children:
            string += '\n' + '\n'.join(f'    {line}' for child in self.children for line in str(child).split('\n'))
        return string


class BulletList:

    def __init__(self):
        self.bullets = list()

    def __len__(self):
        return len(self.bullets)

    def __getitem__(self, index):
        return self.bullets[index]

    def __str__(self):
        return '\n'.join(str(bullet) for bullet in self)

    def append(self, item):
        self.bullets.append(item)

    def filter(self, string):
        results = BulletList()
        for bullet in self:
            if result := bullet.filter(string):
                results.append(result)
        return results


def indent_level(string: str) -> int:
    return int(len(leading_spaces.search(string).groups()[0]) / 4)


def parse_bullets(string_data: str) -> BulletList:
    parents = dict()
    bullets = BulletList()

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
