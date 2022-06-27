import sys, requests
sys.path.append('../..')
import go
import plugins.groupadmin.main as groupadmin
import tools

def checkFriendList(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    print('start checking group...')
    dataa = requests.get(url=meta_data.get('botSettings').get('httpurl')+'/get_friend_list')
    datajson = dataa.json().get('data')
    
    for i in datajson:
        if meta_data.get('isGlobalBanned') != 404:
            go.send(meta_data, '检测到黑名单：'+str(i.get('nickname'))+' 即将删除好友！')
            groupadmin.delete_friend(uid, gid, i.get('user_id'))
    go.send(meta_data, '扫描完毕！')

def checkGroupMember(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    print('start checking group...')
    dataa = requests.get(url=meta_data.get('botSettings').get('httpurl')+'/get_group_member_list?group_id={0}'.format(gid))
    datajson = dataa.json().get('data')
    print(datajson)
    for i in datajson:
        if findObject('qn', i, quanjing).get('object') != 404:
            go.send(meta_data, '检测到黑名单：'+str(i.get('nickname'))+' 即将踢出！')
            
            meta_data['message'] = '[CQ:at,qq='+str(i.get('user_id'))+']'
            groupadmin.kick(meta_data)
    go.send(meta_data, '扫描完毕！')

def addWeijin(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    if uid == meta_data.get('botSettings').get('owner'):
        sql = 'INSERT INTO `botWeijin` (`content`, `state`) VALUES ("'+message+'", 0)'
    else:
        sql = 'INSERT INTO `botWeijin` (`content`, `state`) VALUES ("'+message+'", 1)'
    go.commonx(sql)
    tools.loadConfig(meta_data)
    go.send(meta_data, '[CQ:face,id=161] 插入成功，等待审核！')
    
def bWj(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    vKwList = go.selectx('SELECT * FROM `botWeijin` WHERE `state`=2')
    message = '[CQ:face,id=151] 小猪比机器人-违禁词垃圾箱'
    for i in vKwList:
        message += '\n[CQ:face,id=161] 违禁词：'+str(i.get('content'))+'\n      ID：'+str(i.get('id'))
    go.send(meta_data, message)
    
def vWj(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    vKwList = go.selectx('SELECT * FROM `botWeijin` WHERE `state`=1')
    message = '[CQ:face,id=151] 小猪比机器人-违禁词审核列表'
    for i in vKwList:
        message += '\n[CQ:face,id=161] 违禁词：'+str(i.get('content'))+'\n      ID：'+str(i.get('id'))
    go.send(meta_data, message)
    
def dvWj(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    vKwList = go.selectx('SELECT * FROM `botWeijin` WHERE `state`=3')
    message = '[CQ:face,id=151] 小猪比机器人-违禁词删除列表'
    for i in vKwList:
        message += '\n[CQ:face,id=161] 违禁词：'+str(i.get('content'))+'\n      ID：'+str(i.get('id'))
    go.send(meta_data, message)
    
def tWj(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    message1 = message.split(' ')
    kwid = message1[0]
    iff = message1[1]
    if iff == '通过':
        state = 0
        message = '[CQ:face,id=161] 已通过！'
    else:
        state = 2
        message = '[CQ:face,id=161] 已移至回收站！'
    go.commonx('UPDATE `botWeijin` SET `state`='+str(state)+' WHERE `id`='+str(kwid))
    tools.loadConfig(meta_data)
    go.send(meta_data, message)
    
def delWeijin(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    if uid == meta_data.get('botSettings').get('owner'):
        sql = 'UPDATE `botWeijin` SET `state`=2 WHERE `content`="'+str(message)+'"'
    else:
        sql = 'UPDATE `botWeijin` SET `state`=3 WHERE `content`="'+str(message)+'"'
    go.commonx(sql)
    tools.loadConfig(meta_data)
    go.send(meta_data, '[CQ:face,id=161] 已提交申请，等待审核！')

def listQuanjing(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    message = '[CQ:face,id=189] 小猪比机器人-全局拉黑列表'
    quanjing = go.selectx("SELECT * FROM `botQuanping` WHERE `uuid` = '{0}'".format(meta_data.get('uuid')))
    for i in quanjing:
        message += '\n[CQ:face,id=161] 用户：'+str(i.get('qn'))+'\n     原因：'+str(i.get('reason'))
    go.send(meta_data, message)
    
def deleteQuanjing(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    go.commonx("DELETE FROM `botQuanping` WHERE `uuid`='{0}' and `qn`={1}".format(meta_data.get('uuid'), message))
    tools.loadConfig(meta_data)
    go.send(meta_data, '[CQ:face,id=161] 删除成功！')

def addQuanjing(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    message1 = message.split(' ')
    qn = message1[0]
    reason = message1[1]
    go.commonx("INSERT INTO `botQuanping` (`qn`, `reason`, `uuid`) VALUES ("+str(qn)+", '"+str(reason)+"', '"+str(meta_data.get('uuid')+"')"))
    tools.loadConfig(meta_data)
    go.send(meta_data, '[CQ:face,id=161] 添加成功！')