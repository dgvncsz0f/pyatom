#!/usr/bin/env python3

import atomac
import random
import time
from atomac import AXKeyCodeConstants

sketch_bundle_id = "com.bohemiancoding.sketch3"

def debug(element):
    for attr in element.getAttributes():
        print((attr, getattr(element, attr)))

def try_until_some(func):
    result = []
    while True:
        result = func()
        if result != []:
            return result
        else:
            time.sleep(1)

def confirm(element):
    try:
        field.Confirm()
    except:
        pass

def focus(field):
    try:
        field.AXFocused = True
    except:
        pass

def press(element):
    try:
        element.Press()
    except:
        pass

def show_menu(element):
    try:
        element.ShowMenu()
    except:
        pass

def launch():
    atomac.launchAppByBundleId(sketch_bundle_id)
    return atomac.getAppRefByBundleId(sketch_bundle_id)

def signin_press(sketch):
    button = try_until_some(lambda: sketch.findAllR(AXRole="AXButton", AXTitle="Sign In…"))[0]
    press(button)

def signin_exec(sketch):
    textfield = try_until_some(lambda: sketch.findAllR(AXRole="AXTextField"))[0]
    focus(textfield)
    sketch.sendKeys("sketch@example.com")

    passwordfield = try_until_some(lambda: sketch.findAllR(AXRole="AXTextField", AXSubrole="AXSecureTextField"))[0]
    focus(passwordfield)
    sketch.sendKeys("12345678")

    button = sketch.findAllR(AXRole="AXButton", AXTitle="Sign In")[0]
    press(button)

    button = try_until_some(lambda: sketch.findAllR(AXRole="AXButton", AXTitle="Get Started"))[0]
    press(button)

def file_new(sketch):
    file_menu = sketch.findAllR(AXRole="AXMenuBarItem", AXTitle="File")[0]
    new_menu = file_menu.findAllR(AXRole="AXMenuItem", AXTitle="New")[0]
    press(new_menu)

def insert_artboard(sketch, name):
    sketch.activate()
    insert_menu = try_until_some(lambda: sketch.findAllR(AXRole="AXMenuBarItem", AXTitle="Insert"))[0]
    artboard_menu = try_until_some(lambda: insert_menu.findAllR(AXRole="AXMenuItem", AXTitle="Artboard"))[0]
    if not artboard_menu.AXMenuItemMarkChar:
        press(artboard_menu)

    artboard_selector = try_until_some(lambda: sketch.findAllR(AXRole="AXPopUpButton"))[0]
    show_menu(artboard_selector)
    web_option = try_until_some(lambda: artboard_selector.findAllR(AXRole="AXMenuItem", AXTitle="Web"))[0]
    press(web_option)

    artboard_button = try_until_some(lambda: sketch.findAllR(AXRole="AXButton", AXTitle=name))[0]
    press(artboard_button)

def select_layer(sketch, artboard_name):
    layer = try_until_some(lambda: sketch.findAllR(AXRole="AXTextField", AXValue=artboard_name))[0]
    sketch.clickMouseButtonLeft(layer.AXPosition)

def artboard_background_color(sketch, hexcolor):
    colorpicker = try_until_some(lambda: sketch.findAllR(AXRole="AXButton", AXIdentifier="colorwell_background_color"))[0]
    press(colorpicker)

    dialog = try_until_some(lambda: sketch.findAllR(AXRole="AXWindow", AXSubrole="AXDialog"))[0]
    colorinput = try_until_some(lambda: dialog.findAllR(AXRole="AXTextField"))[0]
    focus(colorinput)
    sketch.sendKeys(hexcolor)
    sketch.sendKey(AXKeyCodeConstants.RETURN)

def random_hexcolor():
    return "".join(["{:02x}".format(int(random.uniform(0,255))) for _ in range(3)])

def file_save(sketch):
    file_menu = sketch.findAllR(AXRole="AXMenuBarItem", AXTitle="File")[0]
    save_menu = file_menu.findAllR(AXRole="AXMenuItem", AXTitle="Save…")[0]
    press(save_menu)

def save_workspace_file(sketch, filename):
    save_sheet = try_until_some(lambda: sketch.sheetsR())[0]

    button = save_sheet.findAllR(AXRole="AXRadioButton", AXTitle="To a Workspace")[0]
    press(button)

    filename_input = save_sheet.textFieldsR()[0]
    focus(filename_input)
    sketch.sendKeys(filename)

    button = save_sheet.findAllR(AXRole="AXButton", AXTitle="Save")[0]
    press(button)

def main():
    sketch = launch()
    sketch.activate()
    signin_press(sketch)
    signin_exec(sketch)

    file_new(sketch)
    insert_artboard(sketch, "Large, 1600×1080")
    select_layer(sketch, "Large")
    artboard_background_color(sketch, random_hexcolor())

    file_save(sketch)
    save_workspace_file(sketch, "aaa")

    return sketch

if __name__ == "__main__":
   main()
