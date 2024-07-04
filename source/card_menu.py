import pygame as pg
import const as c
import data_object


def getSunValueImage(sun_value):
    font = pg.font.Font(c.FONT_PATH, 14)
    font.bold = True
    width = 35
    msg_image = font.render(str(sun_value), True, c.NAVYBLUE, c.LIGHTYELLOW)
    msg_rect = msg_image.get_rect()
    msg_w = msg_rect.width

    image = pg.Surface((width, 17))
    x = width - msg_w

    image.fill(c.LIGHTYELLOW)
    image.blit(msg_image, (x, 0), (0, 0, msg_rect.w, msg_rect.h))
    image.set_colorkey(c.BLACK)
    return image


class Card():
    def __init__(self, x, y, index, scale=0.5):
        self.info = c.PLANT_CARD_INFO[index]
        self.loadFrame(self.info[c.CARD_INDEX], scale)
        self.rect = self.orig_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        font = pg.font.Font(c.FONT_PATH, 12)
        self.sun_cost_img = font.render(str(self.info[c.SUN_INDEX]), True, c.BLACK)
        self.sun_cost_img_rect = self.sun_cost_img.get_rect()
        sun_cost_img_x = 32 - self.sun_cost_img_rect.w
        self.orig_image.blit(self.sun_cost_img,
                             (sun_cost_img_x, 52, self.sun_cost_img_rect.w, self.sun_cost_img_rect.h))

        self.index = index
        self.sun_cost = self.info[c.SUN_INDEX]
        self.frozen_time = self.info[c.FROZEN_TIME_INDEX]
        self.frozen_timer = -self.frozen_time
        self.refresh_timer = 0
        self.clicked = False
        self.image = self.orig_image

    def loadFrame(self, name, scale):
        frame = GFX[name]
        rect = frame.get_rect()
        width, height = rect.w, rect.h

        self.orig_image =  get_image(frame, 0, 0, width, height, c.BLACK, scale)
        self.image = self.orig_image

    def checkMouseClick(self, mouse_pos):
        x, y = mouse_pos
        if (self.rect.x <= x <= self.rect.right and
                self.rect.y <= y <= self.rect.bottom):
            return True
        return False

    def canClick(self, sun_value, current_time):
        if self.sun_cost <= sun_value and (current_time - self.frozen_timer) > self.frozen_time:
            return True
        return False

    def canSelect(self):
        return self.select

    def setSelect(self, can_select):
        self.select = can_select
        if can_select:
            if self.not_recommend % 2:
                self.orig_image.set_alpha(128)
                self.image = pg.Surface((self.rect.w, self.rect.h))  # 黑底
                self.image.blit(self.orig_image, (0, 0), (0, 0, self.rect.w, self.rect.h))
            else:
                self.image = self.orig_image
                self.image.set_alpha(255)
        else:
            self.orig_image.set_alpha(64)
            self.image = pg.Surface((self.rect.w, self.rect.h))  # 黑底
            self.image.blit(self.orig_image, (0, 0), (0, 0, self.rect.w, self.rect.h))

    def setFrozenTime(self, current_time):
        self.frozen_timer = current_time

    def createShowImage(self, sun_value, current_time):
        # 有关是否满足冷却与阳光条件的图片形式
        time = current_time - self.frozen_timer
        if time < self.frozen_time:  # cool down status
            image = pg.Surface((self.rect.w, self.rect.h))  # 黑底
            frozen_image = self.orig_image
            frozen_image.set_alpha(128)
            frozen_height = ((self.frozen_time - time) / self.frozen_time) * self.rect.h

            image.blit(frozen_image, (0, 0), (0, 0, self.rect.w, frozen_height))
            self.orig_image.set_alpha(192)
            image.blit(self.orig_image, (0, frozen_height),
                       (0, frozen_height, self.rect.w, self.rect.h - frozen_height))
        elif self.sun_cost > sun_value:  # disable status
            image = pg.Surface((self.rect.w, self.rect.h))  # 黑底
            self.orig_image.set_alpha(192)
            image.blit(self.orig_image, (0, 0), (0, 0, self.rect.w, self.rect.h))
        elif self.clicked:
            image = pg.Surface((self.rect.w, self.rect.h))  # 黑底
            chosen_image = self.orig_image
            chosen_image.set_alpha(128)

            image.blit(chosen_image, (0, 0), (0, 0, self.rect.w, self.rect.h))
        else:
            image = self.orig_image
            image.set_alpha(255)
        return image

    def update(self, sun_value, current_time):
        if (current_time - self.refresh_timer) >= 250:
            self.image = self.orig_image
            self.refresh_timer = current_time

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class MenuBar():
    def __init__(self, card_list, sun_value):
        self.loadFrame(c.MENUBAR_BACKGROUND)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.sun_value = sun_value
        self.card_offset_x = 26
        self.setupCards(card_list)

    def loadFrame(self, name):
        frame = GFX[name]
        rect = frame.get_rect()
        frame_rect = (rect.x, rect.y, rect.w, rect.h)

        self.image = get_image(GFX[name], *frame_rect, c.WHITE, 1)

    def update(self, current_time):
        self.current_time = current_time
        for card in self.card_list:
            card.update(self.sun_value, self.current_time)

    def updateSunshine(self, new_sunshine):
        self.sun_value = new_sunshine

    def createImage(self, x, y, num):
        if num == 1:
            return
        img = self.image
        rect = self.image.get_rect()
        width = rect.w
        height = rect.h
        self.image = pg.Surface((width * num, height)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        for i in range(num):
            x = i * width
            self.image.blit(img, (x, 0))
        self.image.set_colorkey(c.BLACK)

    def setupCards(self, card_list):
        self.card_list = []
        x = self.card_offset_x
        y = 8
        for index in card_list:
            x += c.BAR_CARD_X_INTERNAL
            self.card_list.append(Card(x, y, index))

    def checkCardClick(self, mouse_pos):
        result = None
        for card in self.card_list:
            if card.checkMouseClick(mouse_pos):
                if card.sun_cost <= self.sun_value:
                    result = (card.index, card)
                break
        return result

    def checkMenuBarClick(self, mouse_pos):
        x, y = mouse_pos
        if (self.rect.x <= x <= self.rect.right and
                self.rect.y <= y <= self.rect.bottom):
            return True
        return False

    def decreaseSunValue(self, value):
        self.sun_value -= value

    def increaseSunValue(self, value):
        self.sun_value += value
        if self.sun_value > 9990:
            self.sun_value = 9990

    def drawSunValue(self):
        self.value_image = getSunValueImage(self.sun_value)
        self.value_rect = self.value_image.get_rect()
        self.value_rect.x = 21
        self.value_rect.y = self.rect.bottom - 24

        self.image.blit(self.value_image, self.value_rect)

    def setCardFrozenTime(self, plant_name):
        for card in self.card_list:
            if c.PLANT_CARD_INFO[card.index][c.PLANT_NAME_INDEX] == plant_name:
                card.setFrozenTime(self.current_time)
                break

    def drawSunValue(self):
        self.value_image = getSunValueImage(self.sun_value)
        self.value_rect = self.value_image.get_rect()
        self.value_rect.x = 21
        self.value_rect.y = self.rect.bottom - 24

        self.image.blit(self.value_image, self.value_rect)

    def draw(self, surface):
        self.drawSunValue()
        surface.blit(self.image, self.rect)
        for card in self.card_list:
            card.draw(surface)
GFX = {
    'sunflower_card': pg.image.load('picture/Cards/card_sunflower.png'),
    'peashooter_card': pg.image.load('picture/Cards/card_peashooter.png'),
    'menu_background': pg.image.load('picture/Screen/ChooserBackground.png')
}

def get_image(sheet, x, y, width, height, colorkey, scale):
    image = pg.Surface([width, height])
    image.blit(sheet, (0, 0), (x, y, width, height))
    image.set_colorkey(colorkey)
    image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
    return image