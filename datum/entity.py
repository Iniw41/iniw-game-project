from datum.items import Item
from generics.levels import (
    calculate_exp_gained_from_enemy_level,
    calculate_level_from_total_exp,
    non_recursively_calculate_total_exp_at_level
)
from pydantic import Field, BaseModel
from typing import Any
from typing_extensions import Annotated

from mediators.actions import Attack


class Entity(BaseModel):
    name: str
    damage: int
    maximum_health: int
    level: int
    current_health: Annotated[int, Field(default=0, init=False)]
    experience: Annotated[float, Field(default=0, init=False)]

    def model_post_init(self, __context: Any) -> None:
        self.current_health = self.maximum_health
        self.experience = non_recursively_calculate_total_exp_at_level(self.level)

    def attack(self, target_mobs: list['Mob']):
        """
        Simulate an attack by this mob on another mob.

        Args:
            target_mobs (Mob): The target mob to attack.

        Returns:
            str: A message describing the attack outcome.
        """
        Attack.execute(self, target_mobs)


    def level_up(self, enemy_level: int):
        self.experience += calculate_exp_gained_from_enemy_level(enemy_level)
        self.level = calculate_level_from_total_exp(self.experience)

    def get_info(self):
        """
        Display information about the mob's health.

        Returns:
            str: A message with current and maximum health.
        """
        return f"{self.name} - Current Level: {self.level} - Current Health: {self.current_health}/{self.maximum_health}"


class Mob(Entity):
    is_target_mob: Annotated[bool, Field(default=False)]


class Player(Entity):
    inventory_id: int
    equipped_items: list[Item]  # TODO: Add Validation If The Item Is In Inventory
    gold_balance: int
