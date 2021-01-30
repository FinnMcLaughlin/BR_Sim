class Weapon:
    def __init__(self, _name, _type, _power, _crit_multiplier, _attk_speed, _recover_speed, _ammo):
        self.name = _name
        self.type = _type
        self.power = _power
        self.crit_multiplier = _crit_multiplier
        self.attk_speed = _attk_speed
        self.recover_speed = _recover_speed
        self.ammo = _ammo

    def get_type(self):
        return self.type

    def get_power(self):
        return self.power

    def get_critical_multiplier(self):
        return self.crit_multiplier

    def get_attack_speed(self):
        return self.attk_speed

    def get_recovery_speed(self):
        return self.recover_speed

    def get_ammo(self):
        return self.ammo

    def upgrade_weapon_power(self, additional_power):
        print("Upgrading: " + self.name)
        self.power += additional_power

    def upgrade_weapon_critical_multiplier(self, additional_multiplier):
        self.crit_multiplier += additional_multiplier