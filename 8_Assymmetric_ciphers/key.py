class Key:
    def __init__(self, ab: int, g: int, p: int):
        self.ab = ab
        self.g = g
        self.p = p
        self.AB = round(self.g ** self.ab % self.p)

    def get_public_key(self) -> list:
        return [self.g, self.p, self.AB]

    def get_private_key(self) -> list:
        return [self.ab]
