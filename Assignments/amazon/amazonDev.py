# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import mysql.connector as mySQL
import datetime
import re

""" global MySQL settings """
mysql_user_name = ''
mysql_password = ''
mysql_ip = ''
mysql_db = 'amazon'

def checkCapacity(items, cart_contents, cart_cap):
    """ articles: a dictionary of the items to be loaded into carts: the key is the item id and the value is the item volume """
    """ cart_contents is output expected expected in teh form of a list of lists, where each sub-list is the contents of each cart denoted by item ids  """
    """ cart_cap: capacity of each cart """
    """ This function returns two parameters, the first of which is the number of bins that are within capacity and, the second, the number of overloaded bins """
    
    num_ok = 0
    num_over = 0
    if isinstance(items,dict):
        if isinstance(cart_contents,list):
            item_key_good = True
            for this_cart in cart_contents:
                if isinstance(this_cart,list):
                    load = 0.0
                    for this_item in this_cart:
                        if this_item not in items.keys():
                            item_key_good = False
                        else:
                            load += items[this_item]
                    if item_key_good == False:
                        print("function checkCapacity(), bad item key")
                        return 'bad_key', 'bad_key'
                    elif load <= cart_cap:
                        num_ok += 1
                    else:
                        num_over += 1
                else:
                    print("Data type error: contents of each cart must be in a sub-list")
                    return 'sublist_error','sublist_error'
            return num_ok, num_over
        else:
            print("Data type error: cart_contents must be a list of lists")
            return 'list_needed', 'list_needed'
    else:
        print("Internal error in function checkCapacity(), items argument must be a dictionary")
        return 'dict_needed', 'dict_needed'
        
def checkAllPoints(items, bin_contents):
    """ Check to be sure that all items are packed in exactly one bin """
    
    err_mess = ""
    err_mult= False
    checkit = {}
    for this_cart in bin_contents:
        for item in this_cart:
            checkit[item] = checkit.get(item,0) + 1
    item_count = [(k,v) for k,v in checkit.items()]
    item_count.sort(key = lambda x:x[1], reverse = True)
    if item_count[0][1] > 1:
        err_mult = True
        err_mess += "At least one item is assigned multiple times.  "
                
    err_all = False
    if len(items.keys() - checkit.keys()) > 0:
        err_all = True
        err_mess += "Some items not assigned to carts.  "
    #for key_art in items.keys():
    #    if key_art not in checkit.keys():
    #        err_all = True
    #        err_mess += "Some items not assigned to carts"
            
    return err_mult, err_all, err_mess

def amazon_algo(items,cart_cap):
    """ You write your heuristic bin packing algorithm in this function using the argument values that are passed
             items: a dictionary of the items to be loaded into the bins: the key is the article id and the value is the article volume
             cart_cap: the capacity of each (identical) bin (volume)
    
        Your algorithm must return two values as indicated in the return statement:
             my_username: if this is a team assignment then set this variable equal to an integer representing your team number;
                                     if this is an indivdual assignment then set this variable to a string with you name
             cart_contents: this is a list containing keys (integers) of the items you want to include in the knapsack
                           The integers refer to keys in the items dictionary. 
   """
        
    my_username = "insert_WM_username"    # always return this variable as the first item
    my_nickname = ''   # enter a nickname here if you do not wish your WM username to be shown on the leaderboard
    cart_contents = []    # use this list document the article ids for the contents of 
                         # each cart, the contents of each is to be listed in a sub-list
        
    ''' start your algorithm below this comment '''
    
    
    ''' finish your algorithm code above this comment '''
            
    return my_username, cart_contents, my_nickname       # use this return statement when you have items to load in the knapsack

def getDBDataList():
    cnx = db_connect()
    cursor = cnx.cursor()
    cursor.callproc('spGetProblemIds')
    items = []
    for result in cursor.stored_results():
        for item in result.fetchall():
            items.append(item[0])
        break
    cursor.close()
    cnx.close()
    return items
   
""" db_get_data connects with the database and returns a dictionary with the knapsack items """
def db_get_data(problem_id):
    cnx = db_connect()
    cursor = cnx.cursor()  
    
    cursor.callproc("spGetCartCap", args=[problem_id])
    for result in cursor.stored_results():
        cart_cap = result.fetchall()[0][0]
        break
    cursor.close()
    cursor = cnx.cursor()
    cursor.callproc('spGetData',args=[problem_id])
    items = {}
    for result in cursor.stored_results():
        blank = result.fetchall()
        break
    for row in blank:
        items[row[0]] = row[1]
    cursor.close()
    cnx.close()
    return cart_cap, items
    
def db_connect():
    cnx = mySQL.connect(user=mysql_user_name, passwd=mysql_password,
                        host=mysql_ip, db=mysql_db)
    return cnx

def print_find(f_name):
    #print(__file__)
    f_name = f_name[:]
    f_name = f_name.replace('()','')
    
    with open(__file__, 'r') as f:
        code = f.readlines()
        
    i = 0
    while not re.search('def\s'+f_name,code[i]) and i < len(code) - 1:
        i += 1
    if i == len(code) - 1:
        msg = 'Function %s() is missing from this code' % f_name
    else:
        i += 1
        msg = ''
        while re.search('^\s+', code[i]):
            if not re.search('\s+#', code[i]) and re.search('print\(', code[i]):
                #print('Please remove or comment out the print statement in your function code before submission:', code[i])
                msg += 'Please remove or comment out the print statement in your %s() function code before submission: %s\n' % (f_name, code[i].strip(),)
            i += 1
    
    return msg


if __name__ == '__main__':    
    """ Get, and evaluate solutions based on algorithm """
    problems = getDBDataList() 
    silent_mode = False    # use this variable to turn on/off appropriate messaging depending on student or instructor use
    
    print('\n\nProblem Number/Num. Carts within Capacity/Num. Carts Overcapacity')
    for problem_id in problems:
        cart_cap, items = db_get_data(problem_id)
        errors = False
        response = None
        
        #while finished == False:
        username, response, nickname = amazon_algo(items.copy(),cart_cap)
        #if not isinstance(response,str):
        if isinstance(response,list):
            num_ok, num_over = checkCapacity(items, response, cart_cap)
            if not isinstance(num_ok,int) or not isinstance(num_over,int):
                errors = True
                if silent_mode:
                    status = num_ok
                else:
                    print("P"+str(problem_id)+num_ok+"_")
                    
            err_mult, err_all, err_mess = checkAllPoints(items, response)
            if err_mult or err_all:
                errors = True
                if silent_mode:
                    status += "_" + err_mess
                else:
                    print("Problem "+ str(problem_id) + ': ' + err_mess)
        else:
            errors = True
            if silent_mode:
                status = "Solution is not of the list data type.  Other errors may also exist."
            else:
                print("Problem "+ str(problem_id) + ": Solution is not of the list data type.  Other errors may also exist.")
                
        if errors == False:
            
            if silent_mode:
                status = "Problem "+ str(problem_id) + ": "
                print(status+"; num_ok: " + num_ok + "; num_over: " + num_over)
            else:
                print(('/').join([str(problem_id),str(num_ok),str(num_over)])) 
            
            this_time = datetime.datetime.now()
    
    msg = print_find('amazon_algo')
    if msg:
        print(msg)