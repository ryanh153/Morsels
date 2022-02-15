from typing import List
import re


class Bullet:
    def __init__(self, string: str) -> None:
        self.bullet_string = string

    @property
    def text(self) -> str:
        return self.bullet_string[2:]

    def __str__(self) -> str:
        return self.bullet_string


def parse_bullets(string_data: str) -> List[Bullet]:
    parent = None
    bullets = list()

    for bullet_str in string_data.strip().split('\n'):
        # leading_spaces =
        bullets.append(Bullet(bullet_str))

    return bullets
