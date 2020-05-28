# coding: utf8
import os
import sys
import shutil
import re
import copy
import json
import platform

osName = platform.system()

#是否开启独立白名单
#开启：true ；关闭：false
Independentwhitelist = 'false'
#是否显示流氓信息（加载插件时显示作者信息）
#开启：true ；关闭：false
loadmsg = 'true'
#设置最低权限等级
# 0:guest 1:user 2:helper 3:admin
mal = 1

helpmsg ='''--------MCDR PluginMgr插件--------
!!pmgr help -帮助信息
!!pmgr show -展示插件列表
!!pmgr bshow -展示已禁用的插件列表
!!pmgr r -重载所有插件
!!pmgr ball -禁用除PluginsMgr外的所有插件
!!pmgr pall -启用所有插件
!!pmgr get [URL] -下载这个插件
!!pmgr add [path] -从本地位置添加一个插
!!pmgr ban [name] -禁用一个插件
!!pmgr pardon [name] -取消禁用一个插件
!!pmgr del [name] -删除一个插件
--------------------------------'''

def on_load(server, old_module):
    #加载信息
    if loadmsg == 'true':
        print('[MCDR PluginMgr]插件加载成功，插件作者：白芷AngelicaRoot')
        server.say('[MCDR PluginMgr]插件加载成功，插件作者：白芷AngelicaRoot')

def on_info(server, info):
    #权限系统
    if info.is_player == 1:
        if info.content.startswith('!!pmgr'):
            if Independentwhitelist == 'true':
                whitelist = []
                with open('./plugins/PluginMgr/whitelist.json') as handle:
                    for line in handle.readlines():
                        whitelist.append(line.replace('\n','').replace('\r',''))
                if info.player in whitelist:
                    permission = 1
                else:
                    permission = 0
            elif Independentwhitelist == 'false':
                if server.get_permission_level(info) >= mal:
                    permission = 1
                else:
                    permission = 0

    #帮助信息
    if info.is_player == 1:
        if info.content.startswith('!!pmgr help'):
            if permission == 1:
                for line in helpmsg.splitlines():
                    server.say(line)
            else:
                server.say('§4你没有使用这个命令的权限！')
        elif info.content.startswith('!!pmgr'):
            if permission == 1:
                if len(info.content) == 6:
                    server.say('§4未知指令，输入"!!pmgr help"以查看帮助列表')
                else:
                    pass
            else:
                server.say('§4你没有使用这个命令的权限！')
                        
    #重载全部插件
    if info.is_player == 1:
        if info.content.startswith('!!pmgr r'):
            if permission == 1:
                server.refresh_all_plugins()
                server.say('§a已重载下列插件：')
                for line in server.get_plugin_list():
                        server.say(line.split('.')[0])
            else:
                server.say('§4你没有使用这个命令的权限！')
    
    #get插件
    if info.is_player == 1:
        if info.content.startswith('!!pmgr get'):
            if permission == 1:
                if(osName == 'Linux'):
                    args = info.content.split(' ')
                    if (len(args) == 1 ):
                        server.say('§4未知指令，输入"!!pmgr help"以查看帮助列表')
                    elif(len(args) == 2 ):
                        server.say('§4未知指令，输入"!!pmgr help"以查看帮助列表')
                    elif (len(args) == 3):
                        result = os.system('cd plugins && wget -N ' + args[2])
                        if result == 0:
                            server.say('§a下载成功!')
                            server.refresh_changed_plugins()
                        else:
                            server.say('§4下载失败！')
                if(osName == 'Windows'):
                    OriginalURL = info.content.split(' ')
                    if (len(OriginalURL) == 1 ):
                        server.say('§4未知指令，输入"!!pmgr help"以查看帮助列表')
                    elif (len(OriginalURL) == 2 ):
                        server.say('§4未知指令，输入"!!pmgr help"以查看帮助列表')
                    elif (len(OriginalURL) == 3 ):
                        slash='\ '[0]
                        URL = OriginalURL[2]
                        filename = URL.split('/')[-1].split('.')[0]+'.py'
                        server.say('[PluginMgr]§4开始下载：'+'§a'+filename)
                        pluginpath = os.getcwd()
                        powershellcommand = 'powershell (new-object Net.WebClient).DownloadFile'
                        os.system('cd /plugins')
                        result = os.system(powershellcommand+"('"+URL+"','"+pluginpath+'\plugins'+slash+filename+"')")
                        if result == 0:
                            server.say('§a下载成功！')
                            server.refresh_changed_plugins()
                        else:
                            server.say('§4下载失败！')
                else:
                    server.say('§4暂不支持该服务器的系统')
            else:
                server.say('§4你没有使用这个命令的权限！')

    #ban插件
    if info.is_player == 1:
        if info.content.startswith('!!pmgr ban'):
            if permission == 1:
                if info.content.split('.')[-1] == 'py':
                    pluginname = info.content.split(' ')[2]
                else:
                    pluginname = info.content.split(' ')[2]+'.py'
                if(len(info.content.split(' ')) == 1):
                    server.say('§4未知指令，输入"!!pmgr help"以查看帮助列表')
                elif (len(info.content.split(' ')) == 2):
                    server.say('§4未知指令，输入"!!pmgr help"以查看帮助列表')
                elif (len(info.content.split(' ')) == 3):
                    server.disable_plugin(pluginname)
                    path = os.getcwd()+'\plugins'
                    name = pluginname+'.disabled'
                    if search(path,name) == -1:
                        server.say('§4插件'+pluginname+'禁用失败 原因：未找该插件')
                    else:
                        server.say('插件'+pluginname+'已被§4禁用')
                        server.refresh_all_plugins()
            else:
                server.say('§4你没有使用这个命令的权限！')

    #pardon插件
    if info.is_player == 1:
        if info.content.startswith('!!pmgr pardon'):
            if permission == 1:
                if info.content.split('.')[-1] == 'py':
                    pluginname = info.content.split(' ')[2]
                else:
                    pluginname = info.content.split(' ')[2]+'.py'
                if(len(info.content.split(' ')) == 1):
                    server.say('§4未知指令，输入"!!pmgr help"以查看帮助列表')
                elif (len(info.content.split(' ')) == 2):
                    server.say('§4未知指令，输入"!!pmgr help"以查看帮助列表')
                elif (len(info.content.split(' ')) == 3):
                    server.enable_plugin(pluginname)
                    path = os.getcwd()+'\plugins'
                    name = pluginname
                    if search(path,name) == -1:
                        server.say('§4插件'+pluginname+'启用失败 原因：未找该插件')
                    else:
                        server.say('插件'+pluginname+'已被§a启用')
                        server.load_plugin(pluginname)                   
            else:
                server.say('§4你没有使用这个命令的权限！')

    #ban全部插件
    if info.is_player == 1:
        if info.content.startswith('!!pmgr ball'):
            if permission == 1:
                if(len(info.content.split(' ')) == 1):
                    server.say('§4未知指令，输入"!!pmgr help"以查看帮助列表')
                elif (len(info.content.split(' ')) == 2):
                    path = os.getcwd()+'\plugins'
                    server.say('已§4禁用§f以下插件：')
                    for pluginname in server.get_plugin_list():
                        name = pluginname+'.disabled'
                        if pluginname != 'PluginMgr.py':
                            server.disable_plugin(pluginname)
                            server.say(pluginname)
                            server.refresh_all_plugins()
                        else:
                            pass                       
            else:
                server.say('§4你没有使用这个命令的权限！')

    #pardon全部插件
    if info.is_player == 1:
        if info.content.startswith('!!pmgr pall'):
            if permission == 1:
                if(len(info.content.split(' ')) == 1):
                    server.say('§4未知指令，输入"!!pmgr help"以查看帮助列表')
                elif (len(info.content.split(' ')) == 2):
                    path = os.getcwd()+'/plugins'
                    file_names = os.listdir(path)
                    server.say('已§a启用§f以下插件:')
                    for name in file_names:
                        if name.split('.')[-1] == 'disabled':
                            server.say(name.split('.')[0])
                            server.enable_plugin(name)
                            server.refresh_all_plugins()
                        else:
                            pass
            else:
                server.say('§4你没有使用这个命令的权限！')

    #show全部插件
    if info.is_player == 1:
        if info.content.startswith('!!pmgr show'):
            if permission == 1:
                if(len(info.content.split(' ')) == 1):
                    server.say('§4未知指令，输入"!!pmgr help"以查看帮助列表')
                elif (len(info.content.split(' ')) == 2):
                    server.say('§a已加载下列插件:')
                    for line in server.get_plugin_list():
                        server.say(line.split('.')[0])
            else:
                server.say('§4你没有使用这个命令的权限！')

    #banshow
    if info.is_player == 1:
        if info.content.startswith('!!pmgr bshow'):
            if permission == 1:
                if(len(info.content.split(' ')) == 1):
                    server.say('§4未知指令，输入"!!pmgr help"以查看帮助列表')
                elif (len(info.content.split(' ')) == 2):
                    path = os.getcwd()+'/plugins'
                    file_names = os.listdir(path)
                    server.say('§4已禁用下列插件:')
                    for name in file_names:
                        if name.split('.')[-1] == 'disabled':
                            server.say(name.split('.')[0])
                        else:
                            pass
            else:
                server.say('§4你没有使用这个命令的权限！')

    #add
    if info.is_player == 1:
        if info.content.startswith('!!pmgr add'):
            if permission == 1:
                if(len(info.content.split(' ')) == 1):
                    server.say('§4未知指令，输入"!!pmgr help"以查看帮助列表')
                elif(len(info.content.split(' ')) == 2):
                    server.say('§4未知指令，输入"!!pmgr help"以查看帮助列表')
                elif(len(info.content.split(' ')) == 3):
                    filepath = info.content.split(' ')[2]
                    path = os.getcwd()+'/plugins'
                    try:
                        shutil.copy(filepath,path)
                    except IOError as e:
                        server.say('§4Unable to copy file. %s' % e)
                    except:
                        server.say('§4Unexpected error:', sys.exc_info())
                    else:
                        slash='\ '[0]
                        server.say('§a成功安装插件：§f'+filepath.split(slash)[-1])
                        server.refresh_all_plugins()

    #del
    if info.is_player == 1:
        if info.content.startswith('!!pmgr del'):
            if permission == 1:
                if(len(info.content.split(' ')) == 1):
                    server.say('§4未知指令，输入"!!pmgr help"以查看帮助列表')
                elif(len(info.content.split(' ')) == 2):
                    server.say('§4未知指令，输入"!!pmgr help"以查看帮助列表')
                elif(len(info.content.split(' ')) == 3):
                    filename = info.content.split(' ')[2] + '.py'
                    path = os.getcwd()+'/plugins/'
                    if os.path.exists(path+filename):
                        os.remove(path+filename)
                        server.refresh_all_plugins()
                        server.say('§a成功删除插件' + filename + '.py')
                    else:
                        server.say('§4未找到文件 '+filename)

#检查文件是否存在
def search(path,name):
    for root, dirs, files in os.walk(path):
        if name in dirs or name in files:
            flag = 1
            root = str(root)
            dirs = str(dirs)
            return os.path.join(root, dirs)
    return -1