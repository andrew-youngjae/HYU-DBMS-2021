import time
import argparse
import traceback
from helpers.connection import conn

def parse_store(parser:argparse.ArgumentParser):
    sub_parsers = parser.add_subparsers(dest='command')

    #command = info
    parse_info = sub_parsers.add_parser('info')
    parse_info.add_argument('id', type=int) #입력 받을 인자값 등록

    #command = menu
    parse_menu = sub_parsers.add_parser('menu')
    parse_menu.add_argument('id', type=int)

    #command = add_menu
    parse_addmenu = sub_parsers.add_parser('add_menu')
    parse_addmenu.add_argument('id', type=int)
    parse_addmenu.add_argument('menu', type=str)

    #command = order
    parse_order = sub_parsers.add_parser('order')
    parse_order.add_argument('id', type=int)
    parse_order.add_argument('status', type=str.lower, choices=['0','1','2','pending','delivering','delivered'], nargs='?')

    #command = update_order
    parse_update_order = sub_parsers.add_parser('update_order')
    parse_update_order.add_argument('id', type=int)
    parse_update_order.add_argument('order_id', type=int, nargs=2)

    #command = stat
    parse_stat = sub_parsers.add_parser('stat')
    parse_stat.add_argument('id', type=int)
    parse_stat.add_argument('start_date', type=str)
    parse_stat.add_argument('days_interval', type=int)

    #command = search
    parse_search = sub_parsers.add_parser('search')
    parse_search.add_argument('id', type=int)


def show_store_info(args):
    try:
        cur = conn.cursor()
        sql = 'SELECT * FROM "store" WHERE "store".id = {sid}'.format(sid=args.id)
        cur.execute(sql)
        store_info = cur.fetchall()
        display_store_info(store_info)
    except Exception:
        traceback.print_exc()

def display_store_info(store_info):
    print("---------------------------------")
    print("Information of Store {id}".format(id = store_info[0][0]))
    print("---------------------------------")
    print("Address : {address}".format(address = store_info[0][1]))
    print("Store Name : {sname}".format(sname = store_info[0][2]))
    print("Location : Latitude : {lat}, Longitude : {lng}".format(lat = store_info[0][3], lng = store_info[0][4]))
    print("Phone Number : {phone}".format(phone=store_info[0][5]))
    print("---------------------------------")
    for idx in range(len(store_info[0][6])):
        print("Day : {day}".format(day=store_info[0][6][idx]['day']))
        print("---------------------------------")
        if(store_info[0][6][idx]['holiday']==False):
            print("Open Time : {open}".format(open=store_info[0][6][idx]['open']))
            print("Close Time : {closed}".format(closed=store_info[0][6][idx]['closed']))
            print("===================================")
        elif(store_info[0][6][idx]['holiday']==True):
            print("Holiday")
            print("===================================")
    print("Seller ID : {sid}".format(sid=store_info[0][7]))
    print("---------------------------------")

def show_menu_info(args):
    try:
        cur = conn.cursor()
        sql = 'SELECT * FROM "menu" WHERE "menu".sid = {sid}'.format(sid=args.id)
        cur.execute(sql)
        menu_info = cur.fetchall()
        menu_info = sorted(menu_info)
        display_menu_info(menu_info)
    except Exception:
        traceback.print_exc()

def display_menu_info(menu_info):
    print("---------------------------------")
    print("Menu List of Store {id}".format(id = menu_info[0][2]))
    print("---------------------------------")
    for index in range(len(menu_info)):
        print("{index}. {menu} | ID : {menu_id}".format(index = index + 1, menu = menu_info[index][1], menu_id = menu_info[index][0]))
    print("---------------------------------")

def add_menu(args):
    try:
        cur = conn.cursor()
        sql = 'INSERT INTO "menu" (menu, sid) VALUES (\'{menu}\', {sid})'.format(menu=args.menu, sid=args.id)
        result = cur.execute(sql)  # parameterized query -> dict형으로 넣을수도 있음
        print(result)
        print("Add Menu Successfully")
        conn.commit()  # insert, delete 다음에는 꼭 이거 해줘야됨
    except Exception:
        traceback.print_exc()

def show_orders(args):
    try:
        cur = conn.cursor()
        if(args.status == None):
            print("Search for all orders")
            print("=======================================================")
            print("All Order Information of Store {sid}".format(sid=args.id))
            print("=======================================================")
            get_orders = "SELECT * FROM \"orders\" WHERE sid = {sid}".format(sid=args.id)
        elif(args.status == '0')or(args.status == 'pending'):
            print("Search for pending orders")
            print("=======================================================")
            print("Pending Order Information of Store {sid}".format(sid=args.id))
            print("=======================================================")
            get_orders = "SELECT * FROM \"orders\" WHERE sid = {sid} AND status = \'pending\'".format(sid=args.id)
        elif (args.status == '1') or (args.status == 'delivering'):
            print("Search for delivering orders")
            print("=======================================================")
            print("Delivering Order Information of Store {sid}".format(sid=args.id))
            print("=======================================================")
            get_orders = "SELECT * FROM \"orders\" WHERE sid = {sid} AND status = \'delivering\'".format(sid=args.id)
        elif (args.status == '2') or (args.status == 'delivered'):
            print("Search for delivered orders")
            print("=======================================================")
            print("Delivered Order Information of Store {sid}".format(sid=args.id))
            print("=======================================================")
            get_orders = "SELECT * FROM \"orders\" WHERE sid = {sid} AND status = \'delivered\'".format(sid=args.id)
        else:
            print("Searching Failed")
            return
        cur.execute(get_orders)
        all_orders = cur.fetchall()
        display_orders(all_orders)

    except Exception:
        traceback.print_exc()

def display_orders(orders_info):
    for records in orders_info:
        print("-------------------------------------------------------")
        print("Status : {status}".format(status=records[9]))
        print("-------------------------------------------------------")
        print("Order ID : {oid}".format(oid=records[0]))
        print("Store ID : {sid}".format(sid=records[1]))
        print("Customer ID : {cid}".format(cid=records[2]))
        for i in range(len(records[4])):
            print("{index}. {menu} | {amount}".format(index=i+1,menu=records[4][i]['menu'],amount=records[4][i]['amount']))
        print("Payment : {payment}".format(payment=records[5]))
        print("Ordered Time : {otime}".format(otime=records[6]))
        print("Delivered Time : {dtime}".format(dtime=records[7]))
        print("Customer Phone : {phone}".format(phone=records[8]))
        print("-------------------------------------------------------")

def update_order(args):
    if(args.order_id[1] == 0):
        status = 'pending'
    elif(args.order_id[1] == 1):
        status = 'delivering'
    elif(args.order_id[1] == 2):
        status = 'delivered'
    else:
        print("You must choose in [0 : pending, 1 : delivering, 2 : delivered]")
        return
    try:
        cur = conn.cursor()
        if(args.order_id[1] == 1):
            #get store location info
            get_store_loc = 'SELECT lat, lng FROM "store" WHERE "store".id = {sid}'.format(sid=args.id)
            cur.execute(get_store_loc)
            store_loc = cur.fetchall()
            store_lat = store_loc[0][0]
            store_lng = store_loc[0][1]

            #select near deliveryman
            select_deliveryman = "SELECT * " \
                                "FROM(" \
                                "SELECT did, stock, (POWER({s_lat}-d_lat, 2)+POWER({s_lng}-d_lng,2)) AS distance " \
                                "FROM(" \
                                "SELECT id AS did, lng AS d_lng, lat AS d_lat, stock " \
                                "FROM delivery)delivery_info " \
                                ")near_dman " \
                                "WHERE stock <= 4 " \
                                "ORDER BY distance " \
                                "LIMIT 1".format(s_lat=store_lat, s_lng=store_lng)
            cur.execute(select_deliveryman)
            dman_info = cur.fetchall()
            did = dman_info[0][0]

            update_order_table = 'UPDATE "orders" SET did = {did}, status = \'{status}\' WHERE id = {oid} AND sid = {sid}'.format(
                did=did, status=status, oid=args.order_id[0], sid=args.id
            )
            cur.execute(update_order_table)
            conn.commit()

            update_dman_stock = 'UPDATE "delivery" SET stock = stock + 1 WHERE id = {did}'.format(did=did)
            cur.execute(update_dman_stock)
            conn.commit()

            print("Delivery Started | Deliveryman Id : {did}".format(did=did))

        else:
            update_order_table = 'UPDATE "orders" SET status = \'{status}\' WHERE id = {oid} AND sid = {sid}'.format(
                status=status, oid=args.order_id[0], sid=args.id
            )
            cur.execute(update_order_table)
            conn.commit()
            print("Order Status is Updated to \'{status}\'".format(status=status))

    except Exception:
        traceback.print_exc()

def stat_order(args):
    try:
        cur = conn.cursor()
        year, month, day = (args.start_date).split('/')
        sql = "SELECT order_time::date AS date, COUNT(*) AS orders " \
            "FROM \"orders\" " \
            "WHERE sid = {sid} AND order_time::date >= \'{year}/{month}/{day}\'::date " \
            "AND order_time::date < \'{year}/{month}/{day}\'::date + interval \'{interval} day\' " \
            "GROUP BY order_time::date;".format(sid=args.id, year=year, month=month, day=day, interval=args.days_interval)
        cur.execute(sql)
        stat_info = cur.fetchall()
        print("=======================================================")
        print("Orders by Date of Store {sid}".format(sid=args.id))
        print("=======================================================")
        display_stat(stat_info)

    except Exception:
        traceback.print_exc()

def display_stat(stat_info):
    for records in stat_info:
        print("{date} | {orders}".format(date=records[0], orders=records[1]))
        print("-------------------------------------------------------")

def search_vip(args):
    try:
        cur = conn.cursor()
        sql = \
            "SELECT DISTINCT cid, name " \
            "FROM ( " \
            "SELECT * FROM " \
            "( " \
            "SELECT DISTINCT cid, mid FROM cart WHERE mid IN (SELECT id FROM menu WHERE sid={sid}) " \
            ")x " \
            "WHERE NOT EXISTS ( " \
            "(SELECT y.id FROM (SELECT id FROM menu WHERE sid={sid})y) " \
            "EXCEPT " \
            "(SELECT z.mid FROM ( " \
            "SELECT DISTINCT cid, mid FROM cart WHERE mid IN (SELECT id FROM menu WHERE sid={sid}) " \
            ")z " \
            "WHERE z.cid = x.cid " \
            ") " \
            ") " \
            ")vip, customer AS c " \
            "WHERE c.id = vip.cid".format(sid=args.id)
        cur.execute(sql)
        vip = cur.fetchall()
        print("=======================================================")
        print("Customer who ordered all menu")
        print("=======================================================")
        for records in vip:
            print("Customer ID : {cid} | Customer Name : {name}".format(cid=records[0], name=records[1]))
            print("-------------------------------------------------------")

    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser() #인자값을 받을 수 있는 인스턴스 생성
    parse_store(parser)
    args = parser.parse_args() #입력받은 인자값을 args에 저장

    if args.command == 'info':
        show_store_info(args)

    elif args.command == 'menu':
        show_menu_info(args)

    elif args.command == 'add_menu':
        if(args.menu != None):
            add_menu(args)

    elif args.command == 'order':
        show_orders(args)

    elif args.command == 'update_order':
        update_order(args)

    elif args.command == 'stat':
        stat_order(args)

    elif args.command == 'search':
        search_vip(args)

    else:
        parser.print_help()

    #main(args)
    print("Running Time: ", end="")
    print(time.time() - start)

"""   
def main(args):
    if args.command =='info':
        val_id = parser.parse_info.id

    pass


"""