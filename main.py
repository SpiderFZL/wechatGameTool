import glob
import os
import time
import traceback
import win32api
import win32gui
from datetime import datetime
from threading import Thread

from ScreenTools import findAndClick, findPic, try_find_and_click, click_when_second_image_not_exist, any_pic_exist, \
    sleep, log, click_when_second_image_exist

is_logout = False



def do_chain_operations(image_name1=r"fuben.bmp", image_name2=None, image_name3=None,
                        image_name4=None, image_name5=None, try_times=3, start_y=None, end_y=None, sleep_time=0.3,
                        match_num=0.75):
    ret = findAndClick(imageName=image_name1, match_num=match_num, start_y=start_y, end_y=end_y)
    if ret < 1:
        return 0
    if image_name2 is not None:
        sleep(sleep_time)
        try_find_and_click(image_name2, match_num=0.7)
    if image_name3 is not None:
        sleep(sleep_time)
        try_find_and_click(image_name3, match_num=0.7)
    if image_name4 is not None:
        sleep(sleep_time)
        try_find_and_click(image_name4, match_num=0.7)
    if image_name5 is not None:
        sleep(sleep_time)
        try_find_and_click(image_name=image_name5, try_times=try_times, start_y=start_y, end_y=end_y, match_num=0.7)

    return ret


def pic_is_exists(image_name=None):
    max_loc, max_val, theight, twidth = any_pic_exist(image_name = image_name)
    return max_val


def in_counterpart():
    exist = pic_is_exists(image_name=r"tuichu.bmp|tuichu1.bmp") > 0.75
    must_not_exist = pic_is_exists(image_name=r"sure.bmp|sure1.bmp|home_tips.png") < 0.75
    return exist and must_not_exist


def async_do_assist():
    while True:
        do_assist()


def main_method():
    global is_logout
    pre_do = datetime(2019, 10, 1)
    pre_go_home_time = datetime(2019, 10, 1)
    i = 10000000

    while i > 0:
        try:
            pre_do_time = datetime.now()
            minute = pre_do_time.minute
            hour = pre_do_time.hour
            seconds = pre_do_time.second

            not_exceed_max_time = (datetime.now() - pre_do).total_seconds() < get_login_duration()
            not_exceed_max_in_counterpart_time = (datetime.now() - pre_do).total_seconds() <= 300

            # 副本中
            if in_counterpart() and not_exceed_max_in_counterpart_time:
                log("副本中，不退出")
                time.sleep(1)
                continue

            # 被退出，如果是刚被退出要等一段时间才能继续操作
            if pic_is_exists(image_name=r"unlogin.bmp") > 0.8 and not_exceed_max_time:
                log("not exceed logout max time")
                sleep(1)
                is_logout = True
                continue
            is_logout = False

            i = i - 1
            pre_do = datetime.now()
            # 点击确认按钮
            findAndClick(imageName=r"sure.bmp|sure1.bmp|queren.bmp|queren2.bmp|dianji.bmp|login.bmp")
            # 尝试关闭窗口
            close_window()

            log("find click use time:"+str((datetime.now() - pre_do_time).microseconds))

            # 留给抢龙魂时间
            if minute >= 58 or (minute < 2 and seconds < 30) and hour <= 18:
                # 如果当前不是归属自己，自动攻击
                log("抢龙魂")
                continue

            if minute < 5 and findAndClick(imageName=r"attack.png", end_y=500) > 0:
                log("自动攻击")
                continue

            # # 异域boss
            # add_assist_times = add_assist_times - 1
            # if do_assist() > 0:
            #     add_assist_times = 10
            #     continue
            # # 异域boss，出现过后增加监控时长
            # if add_assist_times > 0:
            #     continue

            if pic_is_exists(image_name=r"home_tips.png") > 0.75:
                findAndClick(imageName=r"tuichu.bmp|tuichu1.bmp")

            findAndClick(imageName=r"activity_home_collecting.png")
            # 三界boss
            if minute <= 1 and (19 > hour > 11 or hour > 21 or hour <= 5):
                log("三界boss")
                do_chain_operations(image_name1=r"boss.bmp", image_name2=r"boss_temple.png",
                                    image_name3=r"three_world_boss.png",
                                    image_name5=r"go_ahead_beat_boss2.bmp",
                                    try_times=8)
                if in_counterpart():
                    continue

            choose = i % 8
           # choose = 4
            # 每日挑战  and choose == 4
            if choose == 4 and (minute < 6 or 40 < minute < 50):
                log("每日挑战")
                do_flag = do_chain_operations(image_name1=r"fuben.bmp", image_name2=r"instance_daily_trials.bmp")
                if do_flag > 0:
                    daily_sweep()
                    continue

            # 奇遇
            if choose == 5 and minute % 10 == 2:
                do_flag = do_chain_operations(image_name1=r"adventure.bmp",
                                              image_name2=r"accept.bmp|go_ahead1.png|"
                                                          r"adventure_jiechu.bmp",
                                              image_name5=r"smelt.png|beat.bmp|seek.bmp|tiaozhan.bmp|"
                                                          r"receive_award.bmp",
                                              try_times=5)
                # try_find_and_click(image_name=r"adventure_du_leave.bmp")
                # try_find_and_click(image_name=r"adventure_du_leave_1.bmp")
                if do_flag > 0 and do_chain_operations(image_name1=r"smile.png", image_name2=r"smile1.png",
                                                       image_name3=r"send_msg.png") > 0:
                    findAndClick(imageName=r"close_chat_window.png")
                    continue

            # 多人副本
            if choose == 6 and (5 <= hour < 6 or 3 < minute <= 8):
                log("多人副本")
                if do_chain_operations(image_name1=r"boss.bmp",
                                       image_name2=r"boss_this_server.bmp|boss_this_server_1.bmp",
                                       image_name3=r"boss_multi_person.bmp", image_name5=r"boss_beat.bmp",
                                       try_times=5) > 0:
                    continue

            # 天降财宝
            if choose == 7 and (30 < minute < 59) and (hour == 11 or hour == 18):
                log("参与天降财宝")
                if do_limit_time_activity() > 0:
                    sleep(2)
                    if try_find_and_click(image_name=r"activity_treasure_collect_chest.png",match_num=0.7) < 1:
                        # 不是天降财宝，尝试仙府活动
                        activity_home()
                if in_counterpart():
                    continue

            # 云梦秘境
            if choose == 7 and (hour == 12 or hour == 21) and minute < 15:
                log("云梦秘境")
                if do_limit_time_activity() > 0:
                    try_find_and_click(image_name=r"activity_go_ahead_immediately.png", try_times=5)
                if in_counterpart():
                    continue
            if choose == 7 and (hour == 12 or hour == 21) and (minute >= 15):
                log("云梦秘境")
                max_loc, max_val, theight, twidth = findPic(imageName=r"activity_secret_area_in.png")
                if max_val > 0:
                    exit_activity()
                    continue

            # 池瑶
            if hour == 19 and minute < 20:
                log("参与池瑶活动")
                do_limit_time_activity()
                sleep(2)
                if in_counterpart():
                    max_click = 1000
                    while max_click > 0:
                        max_click = max_click - 1
                        click_when_second_image_exist(second_image_name=r"activity_limit_time_swim_match.png",
                                                      image_name=r"activity_limit_time_swim_click.png")
                    continue
            # 巅峰斗法
            if hour == 19 and 30 <= minute < 40:
                log("参与巅峰斗法")
                do_flag = do_limit_time_activity()
                if do_flag > 0:
                    findAndClick(imageName=r"activity_auto_match.png")
                    time.sleep(2)
                if in_counterpart():
                    continue

            # 玄火争夺
            if hour == 19 and minute >= 45:
                log("参与玄火争夺")
                do_flag = do_limit_time_activity()
                if do_flag > 0:
                    sleep(2)
                    try_find_and_click(image_name=r"activity_go_ahead_1.png", try_times=5,match_num=0.7)
                    time.sleep(5)
                    while in_counterpart():
                        try_find_and_click(
                            image_name=r"activity_limit_time_search_person.png|activity_limit_time_auto_search.png",
                            match_num=0.7)
                        time.sleep(5)
                    continue
            # 仙魔对决
            if hour == 20 and minute < 20:
                log("参与仙魔对决")
                do_flag = do_limit_time_activity()
                if do_flag > 0:
                    sleep(0.5)
                    do_chain_operations(image_name1=r"activity_limit_time_make_team.png",
                                        image_name2=r"activity_limit_time_team_create.png",
                                        image_name5=r"activity_quit_match.png")
                    try_find_and_click(image_name=r"activity_limit_time_begin_beat.png")
                    continue
            # 九天之巅
            if hour == 20 and 30 > minute >= 20:
                log("参与九天之巅")
                do_flag = do_limit_time_activity()
                if do_flag > 0:
                    sleep(0.5)
                    try_find_and_click(image_name=r"activity_go_ahead_1.png")
                if in_counterpart():
                    continue
            # 仙府事件
            if choose == 7 and (
                    hour == 15 or hour == 18 or hour == 23) and (
                    datetime.now() - pre_go_home_time).total_seconds() > 300 and minute < 50:
                pre_go_home_time = datetime.now()
                log("参与仙府事件")
                do_flag = do_limit_time_activity()
                if do_flag > 0:
                    if activity_home() < 1:
                        # 不是在仙府中，尝试收集财宝
                        findAndClick(r"activity_treasure_collect_chest.png")
                if in_counterpart():
                    continue
            # 仙缘竞技
            if choose == 7 and minute < 10:
                log("仙缘竞技")
                do_chain_operations(image_name1=r"athletics.bmp", image_name2=r"athletics_army.bmp",
                                    image_name3=r"athletics_phantastes.bmp")
                max_count = 3
                while findAndClick(imageName=r"athletics_phantastes_challenge.bmp", start_y=500,
                                   end_y=567) < 1 and max_count > 0:
                    max_count = max_count - 1
                    if findAndClick(imageName=r"athletics_phantastes_refresh.bmp") < 1:
                        break


            # 挂boss之家
            if choose == 23 and hour < 6:
                f = findAndClick(imageName=r"boss_home_refreshed.bmp")
                if f > 0:
                    sleep(18)

            # 自动闯关
            # if choose < 3:
            if choose < 3 and minute % 5 <= 1:
                log("自动闯关")
                findAndClick(imageName=r"zidongchuanguan.bmp", match_num=0.65)
            else:
                log("暂不执行自动闯关")
        except Exception as e:
            log(repr(e))
            traceback.print_exc()


def close_window():
    global do_assist_pre
    if (datetime.now() - do_assist_pre).total_seconds() <= 3:
        return
    ff = 1
    while ff > 0:
        ff = click_when_second_image_not_exist(image_name=r"X.bmp",
                                               second_image_name=r"unlogin.bmp|chatting.png|"
                                                                 r"activity_limit_time_match.png|"
                                                                 r"activity_limit_time_match2.png|"
                                                                 r"activity_limit_time_quit.png", matchNum=0.72)


# 仙府事件
def activity_home():
    sleep()
    ff = r"activity_home_collect.png|activity_home_collect_box.png|home_beat_sirdar.png|activity_home_collecting.png"
    ret = click_util_disappear(ff)
    sleep(3)
    # 炼制崖
    if findAndClick(imageName=r"home_3.png") > 0:
        sleep(1)
        click_util_disappear(ff)
    if findAndClick(imageName=r"home_2.png") > 0:
        sleep(1)
        click_util_disappear(ff)
    if findAndClick(imageName=r"home_1.png") > 0:
        sleep(1)
        click_util_disappear(ff)
    exit_activity()
    return ret


def do_limit_time_activity():
    do_chain_operations(image_name1=r"activity_daily.png",
                        image_name2=r"activity_limit_time.png", sleep_time=0.3)
    return try_find_and_click(image_name=r"activity_go_ahead.png", end_y=300)


def click_util_disappear(ff):
    max_times = 30
    while try_find_and_click(image_name=ff, try_times=10, match_num=0.7) > 0 and max_times > 0:
        sleep(1)
        max_times = max_times - 1
    if max_times == 30:
        return 0
    return 1


def daily_sweep():
    max_click = 3
    while max_click > 0:
        max_click = max_click - 1
        ff = try_find_and_click(image_name=r"tiaozhan.bmp|saodang.bmp", try_times=8, end_y=300, match_num=0.7)
        if ff < 1:
            break
        else:
            sleep(0.2)


do_assist_pre_print = datetime.now()
do_assist_pre = datetime.now()


def do_assist(times=50):
    global do_assist_pre_print
    global do_assist_pre
    if is_logout or datetime.now().hour < 6:
        if (datetime.now() - do_assist_pre_print).total_seconds() > 5:
            do_assist_pre_print = datetime.now()
            print("do_assist exit")
        return 0
    # if datetime.now().hour < 5:
    #     return 0
    log("异域boss支援")
    ii = times
    # |assist_gold.png
    while ii > 0:
        ff = findAndClick(imageName=r"assist.png|assist_gold.png", start_y=350, end_y=480, match_num=0.72)
        if ff > 0:
            do_assist_pre = datetime.now()
            try_find_and_click(image_name=r"assist_go.png|assist_gold_go.png", try_times=2)
            return 1
        ii = ii - 1
    return 0


def exit_activity():
    try_find_and_click(r"tuichu.bmp")
    try_find_and_click(r"tuichu1.bmp")


def get_login_duration():
    if datetime.now().hour < 6:
        loginDuration = 120
    elif datetime.now().hour < 10:
        loginDuration = 1200
    elif datetime.now().hour < 18:
        loginDuration = 600
    else:
        loginDuration = 800
    return loginDuration


class assistThread (Thread):
    def __init__(self, threadID, name, delay):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay

    def run(self):
        print("开始线程：" + self.name)
        async_do_assist()
        print("退出线程：" + self.name)

def delete_image():
    for file in glob.glob("my_screenshot_*.png"):
        os.remove(file)
        print("Deleted " + str(file))


dm = win32api.EnumDisplaySettings(None, 0)
dm.PelsHeight = 1080
dm.PelsWidth = 1920
dm.BitsPerPel = 32
dm.DisplayFixedOutput = 0
win32api.ChangeDisplaySettings(dm, 0)
hwnd = win32gui.FindWindow(None, '万剑诀')
win32gui.MoveWindow(hwnd, 20, 20, 488, 932, True)

delete_image()
print("do thread")
assistThread(1, "assistThread", 1).start()
# assist_thread = Thread(target=async_do_assist)
# assist_thread.start()
# time.sleep(1)
print("do main")
while True:
    main_method()
    # pass