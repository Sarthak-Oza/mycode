class Player:
    def __init__(self, name, initial_energy=100):
        self.name = name
        self.energy = initial_energy
        self.inventory = []

    def energize(self, energy_increase):
        self.energy += energy_increase

    def deenergize(self, energy_decrease):
        self.energy -= energy_decrease

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def get_inventory(self):
        return self.inventory
        # return ", ".join(str(item) for item in self.inventory)

    def get_energy(self):
        return self.energy
    
    def __str__(self):
        inventory_str = ", ".join(str(item) for item in self.inventory)
        return f"Player {self.name} - Energy: {self.energy}, Inventory: [{inventory_str}]"
