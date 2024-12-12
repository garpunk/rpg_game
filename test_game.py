import pytest
import pygame
import random
from unittest.mock import Mock

pygame.image.load = Mock(return_value=Mock())
pygame.transform.scale = Mock(return_value=Mock())
pygame.time.get_ticks = Mock(return_value=0)




#fighter class
class Fighter():
        def __init__(self, x, y, name, max_hp, strength):
            self.name = name
            self.max_hp = max_hp
            self.hp = max_hp
            self.strength = strength
            self.alive = True
            
            
        
        def attack(self, target):
            #deal damage to enemy
            rand = random.randint(-5, 5)
            damage = self.strength + rand
            target.hp -= damage
        
        def update(self):
             if self.hp <= 0:
                 self.alive = False


#Boss class
class Boss():
        def __init__(self, x, y, name, max_hp, strength):
            self.name = name
            self.max_hp = max_hp
            self.hp = max_hp
            self.strength = strength
            self.alive = True
          
        def attack(self, target):
            #deal damage to enemy
            rand = random.randint(-5, 5)
            damage = self.strength + rand
            target.hp -= damage
            if target.hp < 1:
                target.hp = 0
                target.alive = False

        def update(self):
             if self.hp <= 0:
                 self.alive = False

@pytest.fixture
def setup_game_objects():
    knight = Fighter(400, 330, 'Chrono', 200, 10)
    tyranno = Boss(400, 200, 'Tyranno', 500, 50)
    return knight, tyranno



def test_fighter_attack(setup_game_objects):
    """Test if the fighter's attack correctly reduces the boss's HP."""
    knight, tyranno = setup_game_objects
    initial_hp = tyranno.hp
    knight.attack(tyranno)
    assert tyranno.hp < initial_hp, "Boss HP should decrease after being attacked."
    assert tyranno.hp >= 0, "Boss HP should not be negative."

def test_boss_attack(setup_game_objects):
    """Test if the boss's attack correctly reduces the fighter's HP."""
    knight, tyranno = setup_game_objects
    initial_hp = knight.hp
    tyranno.attack(knight)
    assert knight.hp < initial_hp, "Fighter HP should decrease after being attacked."
    assert knight.hp >= 0, "Fighter HP should not be negative."

def test_fighter_death(setup_game_objects):
    """Test if the fighter's death state is correctly updated when HP reaches 0."""
    knight, tyranno = setup_game_objects
    knight.hp = 0
    knight.update()  # Assume `update` sets alive = False when hp <= 0
    assert not knight.alive, "Fighter should be marked as dead when HP is 0."

def test_boss_death(setup_game_objects):
    """Test if the boss's death state is correctly updated when HP reaches 0."""
    knight, tyranno = setup_game_objects
    tyranno.hp = 0
    tyranno.update()  # Assume `update` sets alive = False when hp <= 0
    assert not tyranno.alive, "Boss should be marked as dead when HP is 0."


    #need to take the classes data, make a dummy class with that data in the test file,
    #then retrieve the function inside of the class (object) and test it