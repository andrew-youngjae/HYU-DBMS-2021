import json
import time
import argparse
import traceback
import datetime
from helpers.connection import conn

def parse_customer(parser:argparse.ArgumentParser):
    sub_parsers = parser.add_subparsers(dest='command')

    # command = info
    parse_info = sub_parsers.add_parser('info')
    parse_info.add_argument('id', type=int)  # 입력 받을 인자값 등록

    # command = address
    parse_address = sub_parsers.add_parser('address')
    parse_address.add_argument('id', type=int)
    parse_address_option = parse_address.add_mutually_exclusive_group()
    parse_address_option.add_argument('-c', '--create')
    parse_address_option.add_argument('-e', '--edit', nargs=2)
    parse_address_option.add_argument('-r', '--remove', type=int)

    # command = pay
    parse_payment = sub_parsers.add_parser('pay')
    parse_payment.add_argument('id', type=int)
    parse_payment_option = parse_payment.add_mutually_exclusive_group()
    parse_payment_option.add_argument('--add-card', type=str)
    parse_payment_option.add_argument('--add-account', nargs=2)
    parse_payment_option.add_argument('-r', '--remove', type=int)

    # command = search
    parse_search = sub_parsers.add_parser('search')
    parse_search.add_argument('id', type=int)
    parse_search.add_argument('-a', action='store_true')
    parse_search.add_argument('-o', type=int, default=0)
    parse_search.add_argument('-l', type=int, default=10)

    # command = store
    parse_store = sub_parsers.add_parser('store')
    parse_store.add_argument('id', type=int)
    parse_store.add_argument('sid', type=int)

    # command = cart
    parse_cart = sub_parsers.add_parser('cart')
    parse_cart.add_argument('id', type=int)
    parse_cart_option = parse_cart.add_mutually_exclusive_group()
    parse_cart_option.add_argument('-c', nargs='+')
    parse_cart_option.add_argument('-l', action='store_true')
    parse_cart_option.add_argument('-r', action='store_true')
    parse_cart_option.add_argument('-p', type=int)

    # command = list
    parse_list = sub_parsers.add_parser('list')
    parse_list.add_argument('id', type=int)
    parse_list.add_argument("-w", "--waiting", action="store_true", help="Display only delivering orders")

def show_customer_info(args):
    try:
        cur = conn.cursor()
        sql = 'SELECT * FROM "customer" WHERE "customer".id = {cid}'.format(cid=args.id)
        cur.execute(sql)
        customer_info = cur.fetchall()
        display_customer_info(customer_info)
    except Exception:
        traceback.print_exc()

def display_customer_info(customer_info):
    print("---------------------------------")
    print("Information of Customer {id}".format(id = customer_info[0][0]))
    print("---------------------------------")
    print("Name : {name}".format(name = customer_info[0][1]))
    print("Phone Number : {phone}".format(phone = customer_info[0][2]))
    print("email : {local}@{domain}".format(local = customer_info[0][3], domain = customer_info[0][4]))
    print("---------------------------------")

def show_customer_address(args):
    try:
        cur = conn.cursor()
        sql = 'SELECT * FROM "address" WHERE "address".cid = {cid}'.format(cid=args.id)
        cur.execute(sql)
        addr_list = cur.fetchall()
        addr_list = sorted(addr_list)
        display_customer_address(addr_list)
    except Exception:
        traceback.print_exc()

def display_customer_address(addr_list):
    print("---------------------------------")
    print("Address List of Customer {id}".format(id=addr_list[0][2]))
    print("---------------------------------")
    for index in range(len(addr_list)):
        print("{index}. {address}".format(index=addr_list[index][0], address=addr_list[index][1]))
    print("---------------------------------")

def create_customer_address(args):
    try:
        cur = conn.cursor()
        sql = 'INSERT INTO "address" (address, cid) VALUES (\'{info}\', {cid})'.format(info=args.create, cid=args.id)
        result = cur.execute(sql)
        conn.commit()
        print(result)
        print("Create New Address Successfully")
    except Exception:
        traceback.print_exc()

def delete_customer_address(args):
    try:
        cur = conn.cursor()
        sql = 'DELETE FROM "address" WHERE cid = {cid} AND index = {index}'.format(cid=args.id, index=args.remove)
        result = cur.execute(sql)
        conn.commit()
        print(result)
        print("Delete Address Successfully")
    except Exception:
        traceback.print_exc()

def edit_customer_address(args):
    try:
        cur = conn.cursor()
        get_address = 'SELECT * FROM "address" WHERE "address".cid = {cid}'.format(cid=args.id)
        cur.execute(get_address)
        addr_list = cur.fetchall()
        addr_list = sorted(addr_list)

        if int(args.edit[0]) >= len(addr_list) or int(args.edit[0])-1 < 0:
            print("There is no such key")
            return

        #addr_index = addr_list[int(args.edit[0])-1][0]
        update_address = 'UPDATE "address" SET address = \'{info}\' WHERE "address".cid = {cid} AND "address".index = {index}'.format(
            info=args.edit[1], cid=args.id, index=args.edit[0]
        )
        result = cur.execute(update_address)
        conn.commit()
        print(result)
        print("Address of Selected Customer is Updated.")
    except Exception:
        traceback.print_exc()

def show_customer_payment(args):
    try:
        cur = conn.cursor()
        sql = 'SELECT "customer".payments FROM "customer" WHERE "customer".id = {cid}'.format(cid=args.id)
        cur.execute(sql)
        payment_list = cur.fetchall()
        payment_list = sorted(payment_list)
        display_customer_payment(payment_list, str(args.id))
    except Exception:
        traceback.print_exc()

def display_customer_payment(payment_list, cid):
    print("------------------------------------------------------------------")
    print("Payment List of Customer {id}".format(id=cid))
    print("------------------------------------------------------------------")
    for index in range(len(payment_list[0][0])):
        print("{index}. {type} | {payment}".format(index=index + 1, type=payment_list[0][0][index]['type'], payment=payment_list[0][0][index]['data']))
    print("------------------------------------------------------------------")

def add_customer_card(args):
    try:
        if len(str(args.add_card)) < 14 or len(str(args.add_card)) > 16:
            print("Card number type is wrong")
            return

        card = {"data":{"card_num":None},"type":"card"}
        (card["data"])["card_num"] = args.add_card

        cur = conn.cursor()
        get_payments = 'SELECT "customer".payments FROM "customer" WHERE "customer".id = {cid}'.format(cid=args.id)
        cur.execute(get_payments)
        payments = cur.fetchall()
        payments = sorted(payments)

        payments[0][0].append(card)

        updated_payments = str(payments[0][0]).replace("\'", "\"")

        update_payments = 'UPDATE "customer" SET payments = \'{payments}\' WHERE "customer".id = {cid}'.format(payments=updated_payments, cid=args.id)
        cur.execute(update_payments)
        conn.commit()
        print("Card Information is Successfully Added")

    except Exception:
        traceback.print_exc()

def add_customer_accounts(args):
    try:
        if int(args.add_account[0]) < 1 or int(args.add_account[0]) > 19:
            print("Account bid Type is Wrong")
            return

        account = {"data":{"bid":None, "acc_num":None},"type":"account"}
        (account["data"])["bid"] = args.add_account[0]
        (account["data"])["acc_num"] = args.add_account[1]

        cur = conn.cursor()
        get_payments = 'SELECT "customer".payments FROM "customer" WHERE "customer".id = {cid}'.format(cid=args.id)
        cur.execute(get_payments)
        payments = cur.fetchall()
        payments = sorted(payments)

        payments[0][0].append(account)

        updated_payments = str(payments[0][0]).replace("\'", "\"")

        update_payments = 'UPDATE "customer" SET payments = \'{payments}\' WHERE "customer".id = {cid}'.format(payments=updated_payments, cid=args.id)
        cur.execute(update_payments)
        conn.commit()
        print("Card Information is Successfully Added")

    except Exception:
        traceback.print_exc()

def remove_customer_payment(args):
    try:
        cur = conn.cursor()
        get_payments = 'SELECT "customer".payments FROM "customer" WHERE "customer".id = {cid}'.format(cid=args.id)
        cur.execute(get_payments)
        payments = cur.fetchall()
        payments = sorted(payments)

        target_index = args.remove

        if target_index <= 0 or target_index > len(payments[0][0]):
            print("There is no such payments information")
            return

        else:
            del payments[0][0][target_index - 1]
            updated_payments = str(payments[0][0]).replace("\'", "\"")
            update_payments = 'UPDATE "customer" SET payments = \'{payments}\' WHERE "customer".id = {cid}'.format(payments=updated_payments, cid=args.id)
            cur.execute(update_payments)
            conn.commit()
            print("Payments Information is Successfully Deleted")

    except Exception:
        traceback.print_exc()

def search_store_info(args):
    time = datetime.datetime.now()
    today = time.weekday()
    try:
        cur = conn.cursor()
        sql = 'SELECT lat, lng FROM "customer" WHERE "customer".id = {cid}'.format(cid=args.id)
        cur.execute(sql)
        customer_info = cur.fetchall()
        clat = customer_info[0][0]
        clng = customer_info[0][1]
    except Exception:
        traceback.print_exc()
    if(args.a):
        if(args.o != None):
            if(args.o == 0):
                orderby = "ORDER BY sname"
            elif(args.o == 1):
                orderby = "ORDER BY address"
            elif(args.o == 2):
                orderby = "ORDER BY distance"
        try:
            cur = conn.cursor()
            sql = "SELECT * " \
                  "FROM(" \
                  "SELECT *, open_time < (NOW() AT TIME ZONE 'Asia/Seoul')::time AND closed_time > (NOW() AT TIME ZONE 'Asia/Seoul')::time	AS open, " \
                  "(POWER({clat}-lat, 2)+POWER({clng}-lng,2)) AS distance " \
                  "FROM(" \
                  "SELECT id, sname, address, lat, lng, " \
                  "concat(substring(open_info->>'open',1,2),':',substring(open_info->>'open',3,2))::time AS open_time," \
                  "concat(substring(open_info->>'closed',1,2),':',substring(open_info->>'closed',3,2))::time AS closed_time " \
                  "FROM(" \
                  "SELECT id, sname, address, lat, lng, jsonb_array_elements(\"store\".schedules) AS open_info " \
                  "FROM \"store\")store_info " \
                  "WHERE (open_info->>'day')::int={day} AND open_info->>'open' != '[null]' AND open_info->>'closed' != '[null]' " \
                  "AND NOT (open_info->>'open' LIKE '24__') AND NOT (open_info->>'closed' LIKE '24__')" \
                  ")schedule_info " \
                  "WHERE open_time < closed_time" \
                  ")open_or_closed " \
                  "{orderby} " \
                  "LIMIT {limit} ".format(clat=clat, clng=clng, day=today, orderby=orderby, limit=args.l)
            cur.execute(sql)
            store_info = cur.fetchall()
            display_store_info(store_info)
        except Exception:
            traceback.print_exc()

    else:
        if (args.o != None):
            if (args.o == 0):
                orderby = "ORDER BY sname"
            elif (args.o == 1):
                orderby = "ORDER BY address"
            elif (args.o == 2):
                orderby = "ORDER BY distance"
        try:
            cur = conn.cursor()
            sql = "SELECT * " \
                  "FROM(" \
                  "SELECT *, open_time < (NOW() AT TIME ZONE 'Asia/Seoul')::time AND closed_time > (NOW() AT TIME ZONE 'Asia/Seoul')::time	AS open, " \
                  "(POWER({clat}-lat, 2)+POWER({clng}-lng,2)) AS distance " \
                  "FROM(" \
                  "SELECT id, sname, address, lat, lng, " \
                  "concat(substring(open_info->>'open',1,2),':',substring(open_info->>'open',3,2))::time AS open_time," \
                  "concat(substring(open_info->>'closed',1,2),':',substring(open_info->>'closed',3,2))::time AS closed_time " \
                  "FROM(" \
                  "SELECT id, sname, address, lat, lng, jsonb_array_elements(\"store\".schedules) AS open_info " \
                  "FROM \"store\")store_info " \
                  "WHERE (open_info->>'day')::int={day} AND open_info->>'open' != '[null]' AND open_info->>'closed' != '[null]' " \
                  "AND NOT (open_info->>'open' LIKE '24__') AND NOT (open_info->>'closed' LIKE '24__')" \
                  ")schedule_info " \
                  "WHERE open_time < closed_time" \
                  ")open_or_closed " \
                  "WHERE open = 'true' " \
                  "{orderby} " \
                  "LIMIT {limit} ".format(clat=clat, clng=clng, day=today, orderby=orderby, limit=args.l)
            cur.execute(sql)
            store_info = cur.fetchall()
            display_store_info(store_info)
        except Exception:
            traceback.print_exc()

def display_store_info(store_info):
    print("-------------------------------------------------------------------------------------")
    print("Information of {num} Stores".format(num=len(store_info)))
    print("-------------------------------------------------------------------------------------")
    for i in range(len(store_info)):
        if store_info[i][7] == True:
            state = 'open'
        else:
            state = 'closed'
        print("| {id} | {sname} | {address} | {open}".format(id=store_info[i][0],sname=store_info[i][1],address=store_info[i][2], open=state))

def select_store(args):
    try:
        cur = conn.cursor()
        sql = 'UPDATE "customer" SET ordering = {sid} WHERE "customer".id = {cid}'.format(sid=args.sid, cid=args.id)
        cur.execute(sql)
        conn.commit()
        print("Store is Selected!")
    except Exception:
        traceback.print_exc()

def show_menu_info(args):
    try:
        cur = conn.cursor()
        get_store = 'SELECT ordering FROM "customer" WHERE "customer".id = {cid}'.format(cid=args.id)
        cur.execute(get_store)
        current_ordering = cur.fetchall()
        if (current_ordering[0][0] == None):
            print("You must select store first")
            return
        sql = 'SELECT * FROM "menu" WHERE "menu".sid = {sid}'.format(sid=current_ordering[0][0])
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
    print("Choose Menu")
    print("---------------------------------")

def add_cart(args):
    if(len(args.c)%2 != 0):
        print("Please Input Menu Index, Amount Pair")
        return
    try:
        cur = conn.cursor()
        get_store = 'SELECT ordering FROM "customer" WHERE "customer".id = {cid}'.format(cid=args.id)
        cur.execute(get_store)
        current_ordering = cur.fetchall()
        if(current_ordering[0][0] == None):
            print("You must select store first")
            return
        get_menu = 'SELECT * FROM "menu" WHERE "menu".sid = {sid}'.format(sid=current_ordering[0][0])
        cur.execute(get_menu)
        menu_info = cur.fetchall()
        for i in range(0, len(args.c), 2):
            add_to_cart = "INSERT INTO \"cart\" (mname, amount, cid, sid, mid) " \
                        "VALUES ( \'{menu}\', \'{amt}\', \'{cid}\', \'{sid}\', \'{mid}\' )".format(
                menu=menu_info[(int(args.c[i])-1)][1], amt=args.c[i+1], cid=args.id, sid=current_ordering[0][0], mid=menu_info[(int(args.c[i])-1)][0]
            )
            cur.execute(add_to_cart)
            conn.commit()
        print("Add your menu into cart successfully")
    except Exception:
        traceback.print_exc()

def show_cart(args):
    try:
        cur = conn.cursor()
        sql = 'SELECT * FROM "cart" WHERE "cart".cid = {cid} AND ordered = FALSE'.format(cid=args.id)
        cur.execute(sql)
        cart_info = cur.fetchall()
        #cart_info = sorted(cart_info)
        display_cart_info(cart_info)
    except Exception:
        traceback.print_exc()

def display_cart_info(cart_info):
    print("---------------------------------")
    print("Order List of Customer {id}".format(id=args.id))
    print("---------------------------------")
    for index in range(len(cart_info)):
        print("{index}. {menu} | {amount}".format(index=index + 1, menu=cart_info[index][0], amount=cart_info[index][1]))
    print("---------------------------------")

def remove_cart(args):
    try:
        cur = conn.cursor()
        sql = 'DELETE FROM "cart" WHERE cid = {cid}'.format(cid=args.id)
        result = cur.execute(sql)
        conn.commit()
        print(result)
        print("Delete Cart Successfully")
    except Exception:
        traceback.print_exc()

def make_order(args):
    try:
        cur = conn.cursor()
        get_customer_info = 'SELECT payments, ordering, phone FROM "customer" WHERE "customer".id = {cid}'.format(cid=args.id)
        cur.execute(get_customer_info)
        ordering = cur.fetchall()
        ordering = sorted(ordering)
        if(ordering[0][0][(int(args.p)-1)]['type']=='card'):
            pay_type = 'Card'
            pay_info = 'Card Number : ' + str(ordering[0][0][(int(args.p)-1)]['data']['card_num'])
        elif(ordering[0][0][(int(args.p)-1)]['type']=='account'):
            pay_type = 'Account'
            pay_info = 'Account Number : ' + str(ordering[0][0][(int(args.p) - 1)]['data']['acc_num'])
        else:
            print("Invalid Payment")
            return
        payment = "{type} | {data}".format(type=pay_type, data=pay_info)
        store_id = ordering[0][1]
        customer_phone = ordering[0][2]

        order_list = list()
        order_list_record = {'menu':None, 'amount':None}

        get_cart_info = 'SELECT * FROM "cart" WHERE "cart".cid = {cid} AND ordered = FALSE'.format(cid=args.id)
        cur.execute(get_cart_info)
        cart_menu = cur.fetchall()
        for records in cart_menu:
            menu_records = order_list_record.copy()
            menu_records['menu'] = records[0]
            menu_records['amount'] = records[1]
            order_list.append(menu_records)

        update_order_table = "INSERT INTO \"orders\" (sid, cid, menu_info, payment, customer_phone) " \
                            "VALUES ({sid}, {cid}, \'{menu_info}\', \'{payment}\', \'{customer_phone}\')".format(
            sid=store_id, cid=args.id, menu_info=str(json.dumps(order_list)), payment=payment, customer_phone=customer_phone
        )
        cur.execute(update_order_table)
        conn.commit()
        print("Your Order is Successfully Received")

        finish_cart = 'UPDATE "cart" SET ordered = TRUE WHERE cid = {cid} AND sid = {sid}'.format(cid=args.id, sid=store_id)
        cur.execute(finish_cart)
        conn.commit()

    except Exception:
        traceback.print_exc()

def show_orders(args):
    try:
        cur = conn.cursor()
        if(not args.waiting):
            sql = 'SELECT sname, order_time, status FROM "orders" NATURAL JOIN "store" WHERE cid = {cid}'.format(cid=args.id)
            cur.execute(sql)
            order_info = cur.fetchall()
            print("Show all ordered information")
            print("=======================================================")
            print("All Order Information of Customer {cid}".format(cid=args.id))
            print("=======================================================")
            display_order_info(order_info)

        elif(args.waiting):
            sql = 'SELECT sname, order_time, status FROM "orders" NATURAL JOIN "store" WHERE did = {did} AND status = \'delivering\''.format(did=args.id)
            cur.execute(sql)
            order_info = cur.fetchall()
            print("Show only delivering information")
            print("=======================================================")
            print("Delivering Order Information of Customer {cid}".format(cid=args.id))
            print("=======================================================")
            display_order_info(order_info)
    except Exception:
        traceback.print_exc()

def display_order_info(order_info):
    for records in order_info:
        print("Store : {sname} | Order Time : {otime} | {status}".format(sname=records[0], otime=records[1], status=records[2]))
        print("-------------------------------------------------------")

if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser()
    parse_customer(parser)
    args = parser.parse_args()

    if args.command == 'info':
        print("Show Information of the Selected Customer")
        show_customer_info(args)

    elif args.command == 'address':
        if(args.create == None)and(args.edit == None)and(args.remove == None):
            print("Show Address of the Selected Customer")
            show_customer_address(args)
        elif(args.create != None):
            print("Create New Address of the Selected Customer")
            create_customer_address(args)
        elif(args.edit != None):
            print("Edit Address of the Selected Customer")
            edit_customer_address(args)
        elif(args.remove != None):
            print("Remove Address of the Selected Customer")
            delete_customer_address(args)
        else:
            parser.print_help()

    elif args.command == 'pay':
        if(args.add_card == None)and(args.add_account == None)and(args.remove == None):
            print("Show Payments of the Selected Customer")
            show_customer_payment(args)
        elif(args.add_card != None):
            print("Add Card Information of the Selected Customer")
            add_customer_card(args)
        elif(args.add_account != None):
            print("Add Accounts Information of the Selected Customer")
            add_customer_accounts(args)
        elif(args.remove != None):
            print("Remove Payments of the Selected Customer")
            remove_customer_payment(args)
        else:
            parser.print_help()

    elif args.command == 'search':
        search_store_info(args)

    elif args.command == 'store':
        select_store(args)

    elif args.command == 'cart':
        if(args.c == None)and(not args.l)and(not args.r)and(args.p == None):
            show_menu_info(args)
        elif(args.c != None):
            add_cart(args)
        elif(args.l):
            show_cart(args)
        elif(args.r):
            remove_cart(args)
        elif(args.p != None):
            make_order(args)
        else:
            parser.print_help()

    elif args.command == 'list':
        show_orders(args)

    else:
        parser.print_help()

    #main(args)
    print("Running Time: ", end="")
    print(time.time() - start)

"""
def main(args):
    # TODO
    pass
"""