import os
import sys
import time
from main import get_account, Zlapp

class Runner(Zlapp):

    Path = '/root/pafd/log/'
    zlapp_login = 'https://uis.fudan.edu.cn/authserver/login?' \
                'service=https://zlapp.fudan.edu.cn/site/ncov/fudanDaily'
    code_url = "https://zlapp.fudan.edu.cn/backend/default/code"

    def __init__(self, run_time):
        self.run_time = self.check_time(run_time)


    def check_time(self, time_str):
        """ 
        Check if self.run_time is "%H:%M:%S" format.
         """
        try:
            time.strptime(time_str, "%H:%M:%S")
        except ValueError as e:
            print("Wrong time format, should be %H:%M:%S")
            raise e
        return time_str

    def get_today(self, format="%Y-%m-%d"):
        """ 
        Return string of today in "%Y-%m-%d" format.
         """
        return time.strftime(format, time.localtime())
    
    def get_tomorrow(self):
        """ 
        Return string of tomorrow in "%Y-%m-%d" format.
         """
        return time.strftime("%Y-%m-%d", time.localtime(time.time() + 86400))
    
    def get_time_delta(self, current, target):
        """ 
        For given time, calculates how many seconds to reach the target time.
        """
        return time.mktime(target) - time.mktime(current)

    def get_future_run_time(self):
        """ 
        Return the time when the script should be run next.
        """
        now = time.localtime()
        today_run_time = time.strptime(self.get_today() + " " + self.run_time, "%Y-%m-%d %H:%M:%S")
        tomorrow_run_time = time.strptime(self.get_tomorrow() + " " + self.run_time, "%Y-%m-%d %H:%M:%S")
        if now < today_run_time:
            return self.get_time_delta(now, today_run_time)
        else:
            return self.get_time_delta(now, tomorrow_run_time)
    
    def runScript(self):
        """ 
        Run daily_fudan.checkin() every day at given time.
         """
        while(1):
            DateStamp = self.get_today(format="%Y-%m-%d %H:%M:%S")
            LogFileName = self.Path + DateStamp + '.log'
            with open(LogFileName, "w+") as f:
                origin = sys.stdout
                sys.stdout = f
                uid, psw, code_id, code_psw = get_account()
                daily_fudan = Zlapp(uid, psw, code_id, code_psw,
                            url_login=self.zlapp_login, url_code=self.code_url)
                daily_fudan.login()
                if daily_fudan.check() == 0:
                    daily_fudan.checkin()
                    daily_fudan.check()
                    daily_fudan.close(1)

                sleep_secs = self.get_future_run_time()
                print("\n\n===> sleeping for %.2f hours." %(sleep_secs/3600))

                sys.stdout = origin
            
            time.sleep(sleep_secs)


if __name__ == '__main__':

    runner = Runner("10:30:00")
    runner.runScript()

# nohup python3 -u script.py > script.log 2>&1 &