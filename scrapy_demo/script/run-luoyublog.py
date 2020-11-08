#!/usr/bin/env python3
# _*_ encoding:utf-8 _*_
import os
import re
import shlex
import subprocess
import sys
import tempfile
import time

# 当前文件名
from pip._vendor.distlib.compat import raw_input

_daemon = os.path.basename(__file__)

print ("当前文件名:%s" % _daemon)


class Properties:
    """
    属性文件类
    """

    def __init__(self, file_name):
        """
        构造函数
        :param file_name:
        """
        file_name = file_name
        exist_file(file_name)

        self.file_name = file_name
        self.properties = {}
        try:
            fopen = open(self.file_name, 'r')
            for line in fopen:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=')
                    self.properties[strs[0].strip()] = strs[1].strip()
        except Exception as e:
            raise e
        else:
            fopen.close()

    def has_key(self, key):
        """
        是否存在KEY
        :param key:
        :return:
        """
        return self.properties.has_key(key)

    def get(self, key, default_value=''):
        """
        根据KEY获取
        :param key:
        :param default_value:
        :return:
        """
        if self.properties.has_key(key):
            return self.properties[key]
        return default_value

    def put(self, key, value):
        """
        添加/修改配置文件
        :param key:
        :param value:
        :return:
        """
        self.properties[key] = value
        replace_property(self.file_name, key + '=.*', key + '=' + value, True)

    def get_app_home(self):
        """
        返回jar所在目录
        :return:
        """
        return self.get("APP_HOME")

    def get_jar_name(self):
        """
        返回jar名称
        :return:
        """
        return self.get("JAR_NAME")

    def get_java_home(self):
        """
        返回JAVA指令所在目录
        :return:
        """
        return self.get("JAVA_HOME")

    def get_main_class(self):
        """
        主函数
        :return:
        """
        return self.get("MAIN_CLASS")

    def get_run_command(self):
        """
        获取启动命令
        :return:
        """
        RUN_COMMAND = "nohup " + self.get_java_home() + " " + get_java_options() + " -jar " + self.get_app_home() + "/" + self.get_jar_name() + self.get_server_port() + " >> /dev/null 2>&1 &"
        return RUN_COMMAND

    def get_program(self):
        """
        获取jar以及端口的完整路径
        :return:
        """
        return self.get_app_home() + "/" + self.get_jar_name() + self.get_server_port()

    def getProgramPid(self):
        return self.get("PROGRAM_ID")

    def startProgram(self):
        p_pid = self.getProgramPid()
        if p_pid != '':
            print("The program seems to have been started pid is :%s" % p_pid)
        else:
            print('Starting program.....')
            args = shlex.split(self.get_run_command())
            print
            args
            process = subprocess.Popen(args, shell=False, stdin=None, stdout=None)
            pid = process.pid
            # print ("pid:%s" % pid)
            # 将进程id存入配置文件
            self.put("PROGRAM_ID", str(pid))
            # if os.system(self.get_run_command()) == 0:
            print('Program startup success,pid is %s:' % pid)

    def stopProgram(self):
        """
        停止程序
        :return:
        """
        p_pid = self.getProgramPid()
        if p_pid == '':
            print('%s is not running ...' % self.get_program())
        else:
            os.system('kill ' + p_pid)
            print('程序成功停止......')

    def monitor(self):
        while 1:
            time.sleep(10)
            p_pid = self.getProgramPid()
            if p_pid == '':
                print('It seems this program is not running. Start it now!')
                self.startProgram()

    def getDaemonPid(self):
        """
        获取Python守护进程ID
        :return:
        """
        result = self.get("DAEMON_ID")
        return result

    def startDaemon(self):
        """
        启动守护进程
        :return:
        """
        d_pid = self.getDaemonPid()
        if d_pid != '':
            print('daemon program is running...')
        else:
            print('starting daemon program...')
            daemon_command = "nohup python %s monitor >> /dev/null 2>&1 &" % _daemon
            process = subprocess.Popen(shlex.split(daemon_command), shell=False, stdin=None, stdout=None)
            pid = process.pid
            self.put("DAEMON_ID", str(pid))
            print('Program startup success,pid is %s:' % pid)

    def stopDaemon(self):
        """
        停止Python守护进程
        :return:
        """
        d_pid = self.getDaemonPid()
        if d_pid == '':
            print('Daemon program is not running...')
        else:
            os.system('kill ' + d_pid)
            print('Daemon program was killed......')


def exist_file(file_name):
    """
    判断文件是否存在,不存在则创建
    :param file_name:
    :return:
    """
    if not os.path.exists(file_name):
        os.mknod(file_name)
        os.system("chmod 777  %s" % file_name)
    else:
        print
        "file %s is found" % file_name


def parse(file_name):
    """
    解析文件
    :param file_name:
    :return:
    """
    return Properties(file_name)


def replace_property(file_name, from_regex, to_str, append_on_not_exists=True):
    """
    替换属性
    :param file_name:
    :param from_regex:
    :param to_str:
    :param append_on_not_exists:
    :return:
    """
    file = tempfile.TemporaryFile()  # 创建临时文件

    if os.path.exists(file_name):
        r_open = open(file_name, 'r')
        pattern = re.compile(r'' + from_regex)
        found = None
        for line in r_open:  # 读取原文件
            if pattern.search(line) and not line.strip().startswith('#'):
                found = True
                line = re.sub(from_regex, to_str, line)
            file.write(line)  # 写入临时文件
        if not found and append_on_not_exists:
            file.write('\n' + to_str)
        r_open.close()
        file.seek(0)

        content = file.read()  # 读取临时文件中的所有内容

        if os.path.exists(file_name):
            os.remove(file_name)

        w_open = open(file_name, 'w')
        w_open.write(content)  # 将临时文件中的内容写入原文件
        w_open.close()

        file.close()  # 关闭临时文件，同时也会自动删掉临时文件
    else:
        print
        "file %s not found" % file_name


def get_java_options():
    """
    java启动参数
    :return:
    """
    JAVA_OPTS = "-Xms512m -Xmx512m -XX:MaxPermSize=1024m -Djava.awt.headless=true -XX:-UseGCOverheadLimit"
    return JAVA_OPTS


if __name__ == '__main__':
    _input_file_path = raw_input('输入属性文件名:')
    # file_path = 'demo.properties'
    props = Properties(_input_file_path)  # 读取文件

    # 键入启动的Java环境
    if props.has_key('JAVA_HOME'):
        if props.get('JAVA_HOME') == '':
            _input_java_home = raw_input('输入要启动的JAVA指令目录:')
            props.put('JAVA_HOME', _input_java_home)  # 修改/添加key=value
        else:
            print
            '文件中配置JAVA指令目录:%s' % props.get('JAVA_HOME')
    else:
        _input_java_home = raw_input('输入要启动的JAVA指令目录:')
        props.put('JAVA_HOME', _input_java_home)  # 修改/添加key=value

    # 键入jar目录
    if props.has_key('APP_HOME'):
        if props.get('APP_HOME') == '':
            _input_app_home = raw_input('输入要启动的jar目录:')
            props.put('APP_HOME', _input_app_home)  # 修改/添加key=value
        else:
            print
            '文件中配置启动的jar目录:%s' % props.get('APP_HOME')
    else:
        _input_app_home = raw_input('输入要启动的jar目录:')
        props.put('APP_HOME', _input_app_home)  # 修改/添加key=value

    # 键入启动的jar名称
    if props.has_key('JAR_NAME'):
        if props.get('JAR_NAME') == '':
            _input_jar_name = raw_input('输入要启动的jar包名称:')
            props.put("JAR_NAME", _input_jar_name)
        else:
            print
            '文件中配置启动的jar名称:%s' % props.get('JAR_NAME')
    else:
        _input_jar_name = raw_input('输入要启动的jar包名称:')
        props.put("JAR_NAME", _input_jar_name)

    # 键入网站启动端口
    if props.has_key('SERVER_PORT'):
        if props.get('SERVER_PORT') == '':
            _input_server_port = raw_input('输入网站启动端口:')
            props.put("SERVER_PORT", _input_server_port)
        else:
            print
            '文件中配置启动端口:%s' % props.get('SERVER_PORT')
    else:
        _input_server_port = raw_input('输入网站启动端口:')
        props.put("SERVER_PORT", _input_server_port)

    # print "网站启动命令:%s" % props.get_run_command()

    # 键入指令
    if len(sys.argv) == 2:
        args = sys.argv[1]
    else:
        args = raw_input('输入命令参数: [ start | stop | restart | monitor ]: ')

    if args == 'start':
        props.startProgram()
        props.startDaemon()
    elif args == 'stop':
        props.stopDaemon()
        props.stopProgram()
    elif args == 'restart':
        props.stopDaemon()
        props.stopProgram()
        time.sleep(3)
        props.startProgram()
        props.startDaemon()
    elif args == 'monitor':
        props.monitor()
    else:
        print('nothing to do')
