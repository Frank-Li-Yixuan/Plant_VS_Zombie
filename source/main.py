import pygame
import pygame as py
import sys
from pygame.locals import *

py.init()
py.mixer.init()

import image
import const as c
from game import *
import objectBase
import zombieBase
import peaBullet
import sunshine
import plantBase
import card_menu

Win = py.display.set_mode(c.GAME_SIZE)
game1 = Game(Win)


selected_card = None
plant_index = None
plant_shadow = None
shadow_pos = None

while True:
    mouse_pos = py.mouse.get_pos()
    mouse_click = py.mouse.get_pressed()
    clicked_sun = game1.checkPick(mouse_pos)
    clicked_cards_or_map = False

    for event in py.event.get():
        if event.type == QUIT:
            py.quit()
            sys.exit()
        elif event.type == py.MOUSEBUTTONDOWN:
            if game1.menu_bar.checkMenuBarClick(mouse_pos):
                result = game1.menu_bar.checkCardClick(mouse_pos)
                if result:
                    plant_index, selected_card = result
                    plant_shadow = card_menu.Card(mouse_pos[0], mouse_pos[1], selected_card.index, 1)
                    plant_shadow.clicked = True
                    clicked_cards_or_map = True
            else:
                if selected_card:
                    game1.addPlant(plant_index, mouse_pos)
                    game1.menu_bar.decreaseSunValue(selected_card.sun_cost)
                    selected_card = None
                    plant_index = None
                    plant_shadow = None
                    clicked_cards_or_map = True
                else:
                    clicked_sun = game1.checkPick(mouse_pos)

        elif event.type == py.MOUSEMOTION:
            if selected_card and plant_shadow.clicked:
                shadow_pos = mouse_pos
                plant_shadow.rect.topleft = shadow_pos

        elif event.type == py.MOUSEBUTTONUP:
            if selected_card and plant_shadow:
                game1.addPlant(plant_index, mouse_pos)
                game1.menu_bar.decreaseSunValue(selected_card.sun_cost)
                selected_card = None
                plant_index = None
                plant_shadow = None

    if not selected_card and mouse_pos and mouse_click[0] and not clicked_sun:
        result = game1.menu_bar.checkCardClick(mouse_pos)
        if result:
            plant_index, selected_card = result
            plant_shadow = card_menu.Card(mouse_pos[0], mouse_pos[1], selected_card.index, 1)
            plant_shadow.clicked = True
            clicked_cards_or_map = True
        elif selected_card:
            if mouse_click[1]:  # 右键取消
                reset_selection()
            elif mouse_click[0]:
                if menu_bar.checkMenuBarClick(mouse_pos):  # 点击菜单栏取消
                    reset_selection()
                else:
                    game1.addPlant(plant_index, mouse_pos)  # 在指定位置种植
                    menu_bar.decreaseSunValue(selected_card.sun_cost)
                    reset_selection()
            elif mouse_pos is None:
                plant_shadow.rect.topleft = (0, 0)  # 设置阴影位置为原点

    game1.draw()
    game1.update()
    game1.menu_bar.update(py.time.get_ticks())
    game1.menu_bar.draw(Win)
    pygame.display.update()
    if plant_shadow:
        plant_shadow.draw(Win)
    py.display.update()

if __name__ == '__main__':
    main()
