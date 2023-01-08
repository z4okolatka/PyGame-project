class FloatCords:
    @property
    def left(self):
        return self.x

    @left.setter
    def left(self, n):
        self.x = n

    @property
    def right(self):
        return self.x + self.rect.width

    @right.setter
    def right(self, n):
        self.x = n - self.rect.width

    @property
    def top(self):
        return self.y

    @top.setter
    def top(self, n):
        self.y = n

    @property
    def bottom(self):
        return self.y + self.rect.height

    @bottom.setter
    def bottom(self, n):
        self.y = n - self.rect.height

    @property
    def center(self):
        return self.x + self.rect.width / 2, self.y + self.rect.height / 2

    @center.setter
    def center(self, xy):
        x, y = xy
        self.x = x - self.rect.width / 2
        self.y = y - self.rect.height / 2

    @property
    def centerx(self):
        return self.x + self.rect.width / 2

    @centerx.setter
    def centerx(self, n):
        self.x = n - self.rect.width / 2

    @property
    def centery(self):
        return self.y + self.rect.height / 2

    @centery.setter
    def centery(self, n):
        self.y = n - self.rect.height / 2

    @property
    def width(self):
        return self.rect.width

    @property
    def height(self):
        return self.rect.height

    @property
    def topleft(self):
        return self.x, self.y
