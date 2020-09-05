import sys
import time

import win32api
import win32con
import win32gui
from PIL import Image, ImageGrab

from dependence.utils.keyboard_util import KeyboardAction
from log import logger
import global_configs
from dependence.utils.image_process_util import crop_screenshot_by_tuple, image_diff, rgb2grey
from dependence.utils.mouse_util import MouseAction
from dependence.utils.screenshot_util import take_screenshot_of_program_using_win32api, \
    take_screenshot_of_desktop_using_PIL
from gui.hwnd_select_gui import show_all_hwnd_select_gui


def run():
    win32gui.SetForegroundWindow(global_configs.hwnd)
    time.sleep(global_configs.Alberta_inner_wait_time)
    # compare image to know whether to use F11 or not
    # TODO: Add function to compare
    # mouse move to the top
    # TODO: Move mouse to the top

    # Click to throw
    MouseAction.left_long_click(200, 200, global_configs.Alberta_floating_throwing_time)
    # Wait a few seconds
    time.sleep(global_configs.Alberta_floating_after_throwing_waiting_time)
    # Limited the fishing line
    MouseAction.left_long_click(200, 200, global_configs.Alberta_floating_straining_line_time)

    x = global_configs.windows_x
    y = global_configs.windows_y

    # Check if suitable for the line to fish
    # Too easy to throw more than 10m
    too_far_flag = True
    while too_far_flag:
        maxes = 0
        index = 0
        for i in range(0, 3):
            image = take_screenshot_of_desktop_using_PIL(window_x=x, window_y=y,
                                                         relative_crop_box=(1031, 652, 1031 + 34, 652 + 49))
            grey_image = rgb2grey(image)
            diff_list = [image_diff(grey_image, global_configs.digit_0_image, function="phash"),
                         image_diff(grey_image, global_configs.digit_1_image, function="phash"),
                         image_diff(grey_image, global_configs.digit_2_image, function="phash"),
                         image_diff(grey_image, global_configs.digit_3_image, function="phash"),
                         image_diff(grey_image, global_configs.digit_4_image, function="phash"),
                         image_diff(grey_image, global_configs.digit_5_image, function="phash"),
                         image_diff(grey_image, global_configs.digit_6_image, function="phash"),
                         image_diff(grey_image, global_configs.digit_7_image, function="phash"),
                         image_diff(grey_image, global_configs.digit_8_image, function="phash"),
                         image_diff(grey_image, global_configs.digit_9_image, function="phash")]
            logger.info("{}th Compare meter digit result:{}".format(i + 1, diff_list))
            for k in range(0, len(diff_list)):
                if diff_list[k] > maxes:
                    index = k
                    maxes = diff_list[k]
        if maxes < 0.7:
            logger.debug("Seems be water, no meter indicator found.")
            continue
        else:
            logger.info("Meter: {}, possibility:{}".format(index, maxes))

        if index < 6 and index != 1:
            # Meter not good ,release
            MouseAction.left_long_click(200, 200, 4)
            time.sleep(5)
            too_far_flag = False
            return
        elif index == 8:
            # A little long
            MouseAction.left_long_click(200, 200, 0.2)
            too_far_flag = False
            time.sleep(1)
        elif index == 9:
            # More longer
            MouseAction.left_long_click(200, 200, 0.5)
            too_far_flag = False
            time.sleep(1)
        elif index == 1:
            MouseAction.left_long_click(200, 200, 1)
            time.sleep(1)
        elif index == 7 or index == 6:
            # perfect
            too_far_flag = False

    # jump flag
    jump_flag = False

    max_time = global_configs.Alberta_max_waiting_time / 0.2
    # Waiting the fish to get in
    while max_time > 0:

        # Get the image of the wheel
        image = take_screenshot_of_desktop_using_PIL(window_x=x, window_y=y, relative_crop_box=(1214, 560, 1238, 566))

        # Compare with the blue line
        d = image_diff(image, global_configs.wheel_image)
        # logger.debug("Image diff result for wheel:{}.".format(d))
        if d > 0.5:

            # Lift the rod
            logger.debug("Catch fish.")
            MouseAction.hold_on_right_then_left(200, 200, right_hold_time=global_configs.Alberta_floating_lift_rod_time,
                                                both_hold_time=global_configs.Alberta_floating_lift_fish_time)
            logger.info("Catch fish finish.")
            break
        else:
            time.sleep(0.2)
            max_time -= 1

    # Wait for too long, abandon this fish rod
    if max_time == 0:
        logger.info("Too long time pass, re-throw the rod.")
        MouseAction.left_long_click(200, 200, 6)
        return

    # Check if success
    time.sleep(8)
    logger.info("Check the result.")

    image = take_screenshot_of_desktop_using_PIL(window_x=x, window_y=y,
                                                 relative_crop_box=(670, 633, 670 + 160, 633 + 40))

    d = image_diff(global_configs.get_image, image)
    if d > 0.5:

        # Catch the fish
        time.sleep(3)
        logger.debug("Image diff result for catch:{}.".format(d))
        logger.debug("Set cursor in {}, {}.".format(x + 700, y + 650))
        MouseAction.click_with_delay(x + 700, y + 650)
        logger.debug("Finish click.")
    else:

        # The fish caught but full
        f = image_diff(global_configs.full_image, image)
        logger.debug("Image diff result for full:{}.".format(f))
        if f > 0.5:
            logger.info("Full! Jump time.")
            jump_flag = True
            logger.debug("Set cursor in {}, {}.".format(x + 570, y + 650))
            MouseAction.click_with_delay(x + 570, y + 650)
            logger.debug("Finish click.")
            time.sleep(4)
        # else:
        #     logger.debug("Await for command.")
        #     sys.exit(1)

    # Check special event
    time.sleep(4)
    image = take_screenshot_of_desktop_using_PIL(window_x=x, window_y=y,
                                                 relative_crop_box=(257, 527, 257 + 200, 527 + 50))
    f = image_diff(global_configs.special_event_image, image)
    logger.debug("Image diff result for special events:{}.".format(f))
    if f > 0.5:
        # Have special event
        logger.info("Trigger special event.")
        logger.debug("Set cursor in {}, {}.".format(x + 350, y + 550))
        MouseAction.click_with_delay(x + 350, y + 550)
        logger.debug("Finish click.")
        time.sleep(4)
    else:
        logger.info("No special event.")

    # Check level up event
    image = take_screenshot_of_desktop_using_PIL(window_x=x, window_y=y,
                                                 relative_crop_box=(355, 616, 355 + 200, 616 + 50))
    f = image_diff(global_configs.special_event_image, image)
    logger.debug("Image diff result for special events:{}.".format(f))
    if f > 0.7:
        logger.info("Trigger level UP.")
        # Have special event
        logger.debug("Set cursor in {}, {}.".format(x + 425, y + 640))
        MouseAction.click_with_delay(x + 425, y + 640)
        logger.debug("Finish click.")
        time.sleep(4)
    else:
        logger.info("Continue level.")

    # Jump time
    if jump_flag:
        logger.info("Jump time start.")
        KeyboardAction.press_and_release(0x54)
        logger.info("Press T.")
        time.sleep(2)
        logger.debug("Set cursor in {}, {}.".format(x + 650, y + 530))
        MouseAction.click_with_delay(x + 650, y + 530)
        logger.debug("Finish click.")
        logger.info("Click center.")
        time.sleep(2)
        logger.debug("Set cursor in {}, {}.".format(x + 525, y + 485))
        MouseAction.click_with_delay(x + 525, y + 485)
        logger.debug("Finish click.")
        logger.info("Click continue.")
        time.sleep(2)
        logger.debug("Set cursor in {}, {}.".format(x + 600, y + 600))
        MouseAction.click_with_delay(x + 600, y + 600)
        logger.debug("Finish click.")
        logger.info("Click confirm button.")
        time.sleep(5)
        logger.info("Continue Fishing.")
        jump_flag = False

