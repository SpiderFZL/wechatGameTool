import time
from datetime import datetime
from threading import current_thread
import cv2
import pyautogui
import win32api
import win32con
from background_capture import capture
from PIL import ImageGrab


class ScreenTools:
    # 屏幕缩放系数 mac缩放是2 windows一般是1
    screenScale = 1


def findAndClick(imageName=r"zidongchuanguan.bmp", match_num=0.75, start_y=None, end_y=None):
    max_loc, max_val, theight, twidth = any_pic_exist(image_name=imageName, match_num=match_num, start_y=start_y,
                                                      end_y=end_y)
    tagCenterX, tagCenterY = convertPosition(max_loc, theight, twidth)
    if max_val >= match_num:
        log(imageName + "匹配值：" + str(tagCenterX) + "-" + str(tagCenterY) + ",match:" + str(
            max_val))
        # 计算出中心点
        click_with_max_loc(tagCenterX, tagCenterY)
        log("click " + imageName)
        return 1
    return 0


def click_with_max_loc(tagCenterX, tagCenterY):
    # 左键点击屏幕上的这个位置
    click(tagCenterX, tagCenterY)


def convertPosition(max_loc, theight, twidth):
    top_left = max_loc
    # bottom_right = (top_left[0] + twidth, top_left[1] + theight)
    tagHalfW = int(twidth / 2)
    tagHalfH = int(theight / 2)
    tagCenterX = top_left[0] + tagHalfW
    tagCenterY = top_left[1] + tagHalfH
    return tagCenterX, tagCenterY


def click_when_second_image_not_exist(image_name=r"zidongchuanguan.bmp",second_image_name=None, matchNum=0.8):
    max_loc, max_val, theight, twidth = find_pic_when_no_match(second_image_name, image_name)
    if (max_val >= matchNum):
        # 计算出中心点
        top_left = max_loc
        bottom_right = (top_left[0] + twidth, top_left[1] + theight)
        tagHalfW = int(twidth / 2)
        tagHalfH = int(theight / 2)
        tagCenterX = top_left[0] + tagHalfW
        tagCenterY = top_left[1] + tagHalfH
        # 左键点击屏幕上的这个位置
        click(tagCenterX, tagCenterY)
        # sleep(0.3)
        print("click " + image_name + " x=" + str(tagCenterX) + ",y=" + str(tagCenterY))
        return 1
    # sleep(0.5)
    return 0


def click_when_second_image_exist(image_name=r"zidongchuanguan.bmp",second_image_name=None, matchNum=0.8):
    max_loc, max_val, theight, twidth = find_pic_when_match(second_image_name, image_name)
    if (max_val >= matchNum):
        # 计算出中心点
        top_left = max_loc
        bottom_right = (top_left[0] + twidth, top_left[1] + theight)
        tagHalfW = int(twidth / 2)
        tagHalfH = int(theight / 2)
        tagCenterX = top_left[0] + tagHalfW
        tagCenterY = top_left[1] + tagHalfH
        # 左键点击屏幕上的这个位置
        click(tagCenterX, tagCenterY)
        # sleep(0.3)
        print("click " + image_name + " x=" + str(tagCenterX) + ",y=" + str(tagCenterY))
        return 1
    else:
        log("没找到 " + image_name)
    # sleep(0.5)
    return 0
def log(msg):
    print(str(datetime.now()) + ": " + msg)


def click(tagCenterX, tagCenterY):
    x, y = pyautogui.position()
    pyautogui.click(tagCenterX, tagCenterY, button='left')  # 点击
    print("click x=" + str(tagCenterX) + ",y=" + str(tagCenterY))
    # sleep(0.1)
    pyautogui.moveTo(x, y)


def findPic(imageName):
    # 先截图
    x, y, w, h = capture_window()
    # screenshot(bbox=None, img="my_screenshot.png")
    # grab_screen(filename="my_screenshot.png")

    # 读取图片 灰色会快
    max_loc, max_val, theight, twidth = match_image(imageName, base_image_name=get_screenshot_name())

    return (x + max_loc[0], y + max_loc[1]), max_val, theight, twidth



def get_screenshot_name():
    return r'my_screenshot_' + str(current_thread().ident) + '.png'


def any_pic_exist(image_name=None, match_num=0.75, start_y=None, end_y=None):
    x, y, w, h = capture_window(start_y, end_y)
    image_arr = image_name.split("|")
    for image in image_arr:
        max_loc, max_val, theight, twidth = match_image(image, base_image_name=get_screenshot_name())
        if max_val >= match_num:
            return (x + max_loc[0], y + max_loc[1]), max_val, theight, twidth
    return (0, 0), 0, 0, 0


def find_pic_when_no_match(no_match_imageName, imageName, start_y=None, end_y=None):
    # 先截图
    x, y, w, h = capture_window(start_y, end_y)  # 读取图片 灰色会快
    no_match_image_arr = no_match_imageName.split("|")
    for image in no_match_image_arr:
        max_loc, max_val, theight, twidth = match_image(image, base_image_name=get_screenshot_name())
        if max_val > 0.8:
            return (0, 0), 0, 0, 0

    max_loc, max_val, theight, twidth = match_image(imageName, base_image_name=get_screenshot_name())
    return (x + max_loc[0], y + max_loc[1]), max_val, theight, twidth


def find_pic_when_match(match_imageName, imageName):
    # 先截图
    x, y, w, h = capture_window()    # 读取图片 灰色会快
    max_loc, max_val, theight, twidth = match_image(match_imageName, base_image_name=get_screenshot_name())
    if max_val < 0.8:
        return (0, 0), 0, 0, 0

    max_loc, max_val, theight, twidth = match_image(imageName, base_image_name=get_screenshot_name())
    return (x + max_loc[0], y + max_loc[1]), max_val, theight, twidth


def capture_window(start_y=None, end_y=None):
    return capture(start_y, end_y, save_name=get_screenshot_name())


def match_image(target_image_name, base_image_name):
    # return find_template_1(base_image_name, targetImageName)
    return find_template(im_search_path=target_image_name, im_source_path=base_image_name)



def find_template_1(base_image_name, targetImageName):
    pre = datetime.now()
    base_image_name = cv2.imread(base_image_name, cv2.IMREAD_GRAYSCALE)
    # base_image_name = cv2.imread(base_image_name)
    tempheight, tempwidth = base_image_name.shape[:2]
    # print(targetImageName + "模板图宽高：" + str(tempwidth) + "-" + str(tempheight))
    # 事先读取按钮截图
    target = cv2.imread(r"./image/%s" % targetImageName, cv2.IMREAD_GRAYSCALE)
    theight, twidth = target.shape[:2]
    # print(targetImageName + "目标图宽高：" + str(twidth) + "-" + str(theight))
    # 先缩放屏幕截图 INTER_LINEAR INTER_AREA
    scaleTemp = cv2.resize(base_image_name,
                           (int(tempwidth / ScreenTools.screenScale), int(tempheight / ScreenTools.screenScale)))
    # stempheight, stempwidth = scaleTemp.shape[:2]
    # print(targetImageName + "缩放后模板图宽高：" + str(stempwidth) + "-" + str(stempheight))
    # 匹配图片
    res = cv2.matchTemplate(scaleTemp, target, cv2.TM_CCOEFF_NORMED)
    mn_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val >= 0.8:
        print(targetImageName + "匹配值：" + str(max_val) + "," + str(max_loc) + "-" + str(theight) + "-" + str(
            twidth) + " use time=" + str((datetime.now() - pre).microseconds))
    return max_loc, max_val, theight, twidth


def imread(filename):
    '''
    Like cv2.imread
    This function will make sure filename exists
    '''
    # s_filename = r"./image/%s" % filename
    im = cv2.imread(filename)
    if im is None:
        raise RuntimeError("file: '%s' not exists" % filename)
    return im


def find_template(im_search_path, im_source_path, rgb=True, bgremove=False):
    tmp_pre_time = datetime.now()
    im_source = imread(im_source_path)
    s_im_search_path = r"./image/%s" % im_search_path
    im_search = imread(s_im_search_path)
    ScreenTools.screenScale = 486 / im_source.shape[1]
    w, h = im_search.shape[1] / ScreenTools.screenScale, im_search.shape[0] / ScreenTools.screenScale
    if ScreenTools.screenScale != 1:
        # 先缩放屏幕截图 INTER_LINEAR INTER_AREA
        im_search = cv2.resize(im_search, (int(w), int(h)))

    '''
    Locate image position with cv2.templateFind

    Use pixel match to find pictures.

    Args:
        im_source(string): 图像、素材
        im_search(string): 需要查找的图片
        threshold: 阈值，当相识度小于该阈值的时候，就忽略掉

    Returns:
        A tuple of found [(point, score), ...]

    Raises:
        IOError: when file read error
    '''
    # method = cv2.TM_CCORR_NORMED
    # method = cv2.TM_SQDIFF_NORMED
    method = cv2.TM_CCOEFF_NORMED

    if rgb:
        s_bgr = cv2.split(im_search) # Blue Green Red
        i_bgr = cv2.split(im_source)
        weight = (0.3, 0.3, 0.4)
        resbgr = [0, 0, 0]
        for i in range(3): # bgr
            resbgr[i] = cv2.matchTemplate(i_bgr[i], s_bgr[i], method)
        res = resbgr[0]*weight[0] + resbgr[1]*weight[1] + resbgr[2]*weight[2]
    else:
        s_gray = cv2.cvtColor(im_search, cv2.COLOR_BGR2GRAY)
        i_gray = cv2.cvtColor(im_source, cv2.COLOR_BGR2GRAY)
        # 边界提取(来实现背景去除的功能)
        if bgremove:
            s_gray = cv2.Canny(s_gray, 100, 200)
            i_gray = cv2.Canny(i_gray, 100, 200)

        res = cv2.matchTemplate(i_gray, s_gray, method)

    theight, twidth = im_source.shape[:2]
    result = []
    # while True:
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
    #     top_left = min_loc
    # else:
    #     top_left = max_loc
    # if DEBUG:
    #     print('templmatch_value(thresh:%.1f) = %.3f' %(threshold, max_val)) # not show debug
    # if max_val < threshold:
    #     break
    # calculator middle point
    # middle_point = (top_left[0]+w/2, top_left[1]+h/2)
    # result.append(dict(
    #     result=middle_point,
    #     rectangle=(top_left, (top_left[0], top_left[1] + h), (top_left[0] + w, top_left[1]), (top_left[0] + w, top_left[1] + h)),
    #     confidence=max_val
    # ))
        # if maxcnt and len(result) >= maxcnt:
        #     break
        # # floodfill the already found area
        # cv2.floodFill(res, None, max_loc, (-1000,), max_val-threshold+0.1, 1, flags=cv2.FLOODFILL_FIXED_RANGE)
    # print("match use time" + str((datetime.now() - tmp_pre_time).total_seconds()))
    return max_loc, max_val, h, w


def screenshot(bbox=None, img=''):

    im = ImageGrab.grab(bbox)
    im.save(img)
    sleep(0.3)


def grab_screen(filename):
    im = ImageGrab.grabclipboard()
    while True:
        win32api.keybd_event(win32con.VK_SNAPSHOT, 0, 0, 0)
        sleep(1)
        win32api.keybd_event(win32con.VK_SNAPSHOT, 0, win32con.KEYEVENTF_KEYUP, 0)
        sleep(5)
        im = ImageGrab.grabclipboard()
        if im is None:
            print('===>is None ')
        else:
            print('===>' + str(im.size))
            break
        print('===>get ' + str(im.size))
        # rect = (left, top, right, bottom)
        # im = im.crop(rect)
        im.save(filename, 'PNG')
        return im
    #im.show()


def try_find_and_click(image_name, try_times=3, start_y=None, end_y=None, match_num=0.75):
    image_arr = image_name.split("|")
    for image in image_arr:
        k = 0
        while k <= try_times:
            if findAndClick(imageName=image, start_y=start_y, end_y=end_y, match_num=match_num) > 0:
                # sleep(0.5)
                return 1
            else:
                k = k + 1
    return 0


def sleep(sleep_time=0.5):
    print("sleep:" + str(sleep_time))
    time.sleep(sleep_time)
