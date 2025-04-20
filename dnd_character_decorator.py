from abc import ABC, abstractmethod


class Character(ABC):
    @abstractmethod
    def get_power(self): pass

    @abstractmethod
    def get_armor(self): pass

    @abstractmethod
    def get_skills(self): pass

    @abstractmethod
    def get_description(self): pass

    @abstractmethod
    def get_level(self): pass

    @abstractmethod
    def get_equipment(self): pass


class Fighter(Character):
    def __init__(self):
        self.level = 1
        self.power = 12
        self.armor = 6
        self.skills = ["Extra Attack", "Action Surge"]
        self.equipment = []

    def get_power(self): return self.power
    def get_armor(self): return self.armor
    def get_skills(self): return self.skills
    def get_description(self): return "Fighter"
    def get_level(self): return self.level
    def get_equipment(self): return self.equipment

class Ranger(Character):
    def __init__(self):
        self.level = 1
        self.power = 10
        self.armor = 4
        self.skills = ["Survival", "Longstrider"]
        self.equipment = []

    def get_power(self): return self.power
    def get_armor(self): return self.armor
    def get_skills(self): return self.skills
    def get_description(self): return "Ranger"
    def get_level(self): return self.level
    def get_equipment(self): return self.equipment

class Sorcerer(Character):
    def __init__(self):
        self.level = 1
        self.power = 6
        self.armor = 2
        self.skills = ["Sacred Flame", "Light", "Paison Spray"]
        self.equipment = []

    def get_power(self): return self.power
    def get_armor(self): return self.armor
    def get_skills(self): return self.skills
    def get_description(self): return "Sorcerer"
    def get_level(self): return self.level
    def get_equipment(self): return self.equipment

class CharacterDecorator(Character):
    def __init__(self, character):
        self.character = character

    def get_power(self): return self.character.get_power()
    def get_armor(self): return self.character.get_armor()
    def get_skills(self): return self.character.get_skills()
    def get_description(self): return self.character.get_description()
    def get_level(self): return self.character.get_level()
    def get_equipment(self): return self.character.get_equipment()

class LevelUp(CharacterDecorator):
    def __init__(self, character, bonus):
        super().__init__(character)
        self.bonus = bonus

    def get_power(self):
        return self.character.get_power() + self.bonus

    def get_level(self):
        return self.character.get_level() + 1

class BattleMaster(CharacterDecorator):
    def get_power(self): return self.character.get_power() + 8
    def get_skills(self): return self.character.get_skills() + ["Precision Attack"]
    def get_description(self): return self.character.get_description() + " + Battle Master"

class EldritchKnight(CharacterDecorator):
    def get_power(self): return self.character.get_power() + 6
    def get_skills(self): return self.character.get_skills() + ["Mage Armour"]
    def get_description(self): return self.character.get_description() + " + Eldritch Knight"

class Champion(CharacterDecorator):
    def get_power(self): return self.character.get_power() + 8
    def get_skills(self): return self.character.get_skills() + ["Improved Critical Hit"]
    def get_description(self): return self.character.get_description() + " + Champion"

class ArcaneArcher(CharacterDecorator):
    def get_power(self): return self.character.get_power() + 6
    def get_skills(self): return self.character.get_skills() + ["Arcane Shoot"]
    def get_description(self): return self.character.get_description() + " + Arcane Archer"

class BeastMaster(CharacterDecorator):
    def get_power(self): return self.character.get_power() + 6
    def get_skills(self): return self.character.get_skills() + ["Animal Handling"]
    def get_description(self): return self.character.get_description() + " + Beast Master"

class Hunter(CharacterDecorator):
    def get_power(self): return self.character.get_power() + 8
    def get_skills(self): return self.character.get_skills() + ["True Strike"]
    def get_description(self): return self.character.get_description() + " + Hunter"

class GloomStalker(CharacterDecorator):
    def get_power(self): return self.character.get_power() + 8
    def get_skills(self): return self.character.get_skills() + ["Dread Ambusher"]
    def get_description(self): return self.character.get_description() + " + Gloom Stalker"

class Swarmkeeper(CharacterDecorator):
    def get_power(self): return self.character.get_power() + 6
    def get_skills(self): return self.character.get_skills() + ["Legion of Bees"]
    def get_description(self): return self.character.get_description() + " + Swarmkeeper"

class DraconicBloodline(CharacterDecorator):
    def get_power(self): return self.character.get_power() + 8
    def get_skills(self): return self.character.get_skills() + ["Dragon Ancestry", "Fly"]
    def get_description(self): return self.character.get_description() + " + Draconic Bloodline"

class WildMagic(CharacterDecorator):
    def get_power(self): return self.character.get_power() + 8
    def get_skills(self): return self.character.get_skills() + ["Kontrollu Kaos", "Bend Luck"]
    def get_description(self): return self.character.get_description() + " + Wild Magic"

class StormSorcery(CharacterDecorator):
    def get_power(self): return self.character.get_power() + 8
    def get_skills(self): return self.character.get_skills() + ["Heart of the Storm", "Gust of Wind"]
    def get_description(self): return self.character.get_description() + " + Storm Sorcery"

class ShadowMagic(CharacterDecorator):
    def get_power(self): return self.character.get_power() + 8
    def get_skills(self): return self.character.get_skills() + ["Superior Darkvision", "Shadow Walk"]
    def get_description(self): return self.character.get_description() + " + Shadow Magic"

class Sword(CharacterDecorator):
    def get_power(self): return self.character.get_power() + 6
    def get_equipment(self): return self.character.get_equipment() + ["Sword"]

class Bow(CharacterDecorator):
    def get_power(self): return self.character.get_power() + 6
    def get_equipment(self): return self.character.get_equipment() + ["Bow"]

class Dagger(CharacterDecorator):
    def get_power(self): return self.character.get_power() + 4
    def get_equipment(self): return self.character.get_equipment() + ["Dagger"]

class Axe(CharacterDecorator):
    def get_power(self): return self.character.get_power() + 8
    def get_equipment(self): return self.character.get_equipment() + ["Axe"]

class Staff(CharacterDecorator):
    def get_power(self): return self.character.get_power() + 4
    def get_equipment(self): return self.character.get_equipment() + ["Staff"]

class Hat(CharacterDecorator):
    def get_armor(self): return self.character.get_armor() + 2
    def get_equipment(self): return self.character.get_equipment() + ["Hat"]

class Helmet(CharacterDecorator):
    def get_armor(self): return self.character.get_armor() + 4
    def get_equipment(self): return self.character.get_equipment() + ["Helmet"]

class ChainArmor(CharacterDecorator):
    def get_armor(self): return self.character.get_armor() + 6
    def get_equipment(self): return self.character.get_equipment() + ["Chain Armor"]

class KnightArmor(CharacterDecorator):
    def get_armor(self): return self.character.get_armor() + 12
    def get_equipment(self): return self.character.get_equipment() + ["Knight Armor"]

class LeatherBoots(CharacterDecorator):
    def get_armor(self): return self.character.get_armor() + 2
    def get_equipment(self): return self.character.get_equipment() + ["Leather Boots"]

class PlateBoots(CharacterDecorator):
    def get_armor(self): return self.character.get_armor() + 6
    def get_equipment(self): return self.character.get_equipment() + ["Plate Boots"]