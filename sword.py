class Sword:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage
        
    def strike(self):
        print(f"{self.name} deals {self.damage} damage!")
        
    def upgrade(self):
        self.damage += 10
        print(f"{self.name} was upgraded! New damage: {self.damage}")
        
    def can_strike(self, min_damage):
        return self.damage >= min_damage

# Test code
excalibur = Sword("Excalibur", 50)
excalibur.strike()
excalibur.upgrade()
excalibur.strike()
print(f"Can strike with min damage 40? {excalibur.can_strike(40)}")
print(f"Can strike with min damage 70? {excalibur.can_strike(70)}")
