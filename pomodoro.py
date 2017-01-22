#!/usr/bin/env python3

import sys
import os
import datetime, time


class Pomodoro(object):
    """
    Represents a pomodoro timer.
    """


    # def __init__():
    #     """
    #     Creates a default pomodoro.
    #     """
    #     self.file = os.path.expanduser('~/.config/pomodoro/default')


    def __init__(self, name = 'default', work_time = 25, break_time = 5):
        """
        Creates a pomodoro. It doesn't start it. though.
        """
        self.name = name
        self.work_time = datetime.timedelta(work_time)
        self.break_time = datetime.timedelta(break_time)
        self.file = os.path.expanduser('~/.config/pomodoro/'+name)


    def status(self):
        """
        Returns the time of the current work/break period. The format is "W
        mm:ss" or "B mm:ss" for the work timer and break timer, respectively.
        """
        if os.path.exists(self.file):
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(self.file))
            running = datetime.datetime.today() - mtime
            left = self.work_time - running
            prefix = ''
            if left.total_seconds() < 0:
                left = left + self.break_time
                prefix = 'B'
            else:
                prefix = 'W'
            if not (os.stat(self.file).st_size == 0):
                prefix = 'P' + prefix
            return prefix + time.strftime('%M%S', time.gmtime(left.total_seconds()))
        else:
            return '--:--'


    def start(self):
        """
        Starts a pomodoro. Technically it creates an empty file. If a timer is
        already running, this function doesn't create a file but instead prints
        a message saying that a timer is already running.
        """
        if os.path.exists(self.file):
            print('A timer is already running.')
        else:
            os.makedirs(name=os.path.dirname(self.file), exist_ok=True)
            with open(self.file, 'w'):
                        os.utime(self.file, None)


    def stop(self):
        """
        Stops a pomodoro. Technically it deletes the file.
        """
        if os.path.exists(self.file):
            try:
                os.remove(self.file)
            except:
                print('Could not stop the current timer.'
                      ' The file is probably opened.')


    def pause(self):
        """
        Pauses an existing timer. Technically it inserts a time string into the
        formerly empty file. If the file doesn't exist it doesn't do anything
        but print a message to the user that no timer is currently running.
        """
        if not os.path.exists(self.file):
            print('No timer is currently running.')
        elif not (os.stat(self.file).st_size == 0):
            print('The timer is already paused')
        else:
            with open(self.file, 'w') as f:
                f.write(time.strftime('%M:%S', time.gmtime()))


    def resume(self):
        """
        Resume a paused timer. Technically it replaces the file and sets the
        modification time accordingly.
        """
        mtime = ''
        if os.path.exists(self.file):
            with open(self.file) as f:
                for line in f:
                    mtime = line
            try:
                os.remove(self.file)
            except:
                print('Could not resume the current timer.'
                      ' The file is probably opened.')
                return
        if not mtime == '':
            with open(self.file, 'w'):
                mtime = datetime.datetime.today() - time.strptime(mtime, '%M:%S')
                os.utime(self.file, (mtime, mtime))


def main(argv):
    """
    Implements a simple pomodoro timer.
    """
    print(argv)
    pomodoro = Pomodoro()
    # pomodoro.start()
    pomodoro.pause()
    pomodoro.resume()
    print(pomodoro.status())
    # pomodoro.stop()


if __name__ == "__main__":
    main(sys.argv)
