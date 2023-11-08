class Gun:
    def __init__(self):
        self.bullets = 10

    def load_gun(self, bullets):
        self.bullets += bullets

    def shoot(self, bullets):
        print("Shooting with gun")
        self.bullets -= bullets

    def fire_gun(self):
        print("Firing Gun")

    def get_bullets(self):
        return self.bullets

    def __str__(self):
        return "gun"
