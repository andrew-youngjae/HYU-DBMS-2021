import time
import argparse
import traceback
from helpers.connection import conn

def parse_seller(parser:argparse.ArgumentParser):
    sub_parsers = parser.add_subparsers(dest='command')

    # command = info
    parse_info = sub_parsers.add_parser('info')
    parse_info.add_argument('id', type=int)  # 입력 받을 인자값 등록

    # command = upadate
    parse_update = sub_parsers.add_parser('update')
    parse_update.add_argument('id', type=int)
    parse_update.add_argument('column', type=str)
    parse_update.add_argument('value', type=str)

def show_seller_info(args):
    try:
        cur = conn.cursor()
        sql = 'SELECT * FROM "seller" WHERE "seller".id = {id}'.format(id=args.id)
        cur.execute(sql)
        seller_info = cur.fetchall()
        display_seller_info(seller_info)
    except Exception:
        traceback.print_exc()

def display_seller_info(seller_info):
    print("---------------------------------")
    print("Information of Seller {id}".format(id = seller_info[0][0]))
    print("---------------------------------")
    print("Name : {name}".format(name = seller_info[0][1]))
    print("Phone Number : {phone}".format(phone = seller_info[0][2]))
    print("email : {local}@{domain}".format(local = seller_info[0][3], domain = seller_info[0][4]))
    print("---------------------------------")

def update_seller_name(args):
    try:
        cur = conn.cursor()
        sql = 'UPDATE "seller" SET name = \'{name}\' WHERE "seller".id = {id}'.format(name=args.value, id=args.id)
        result = cur.execute(sql)  # parameterized query -> dict형으로 넣을수도 있음
        print(result)
        conn.commit()
        print("Update Seller's Name Successfully")
    except Exception:
        traceback.print_exc()

def update_seller_phone(args):
    try:
        cur = conn.cursor()
        sql = 'UPDATE "seller" SET phone = \'{phone}\' WHERE "seller".id = {id}'.format(phone=args.value, id=args.id)
        result = cur.execute(sql)  # parameterized query -> dict형으로 넣을수도 있음
        print(result)
        conn.commit()
        print("Update Seller's Phone Number Successfully")
    except Exception:
        traceback.print_exc()

def update_seller_local(args):
    try:
        cur = conn.cursor()
        sql = 'UPDATE "seller" SET local = {local} WHERE "seller".id = {id}'.format(local=args.value, id=args.id)
        result = cur.execute(sql)  # parameterized query -> dict형으로 넣을수도 있음
        print(result)
        conn.commit()
        print("Update Seller's email-ID Successfully")
    except Exception:
        traceback.print_exc()

def update_seller_domain(args):
    try:
        cur = conn.cursor()
        sql = 'UPDATE "seller" SET domain = {domain} WHERE "seller".id = {id}'.format(domain=args.value, id=args.id)
        result = cur.execute(sql)  # parameterized query -> dict형으로 넣을수도 있음
        print(result)
        conn.commit()
        print("Update Seller's email-Domain Successfully")
    except Exception:
        traceback.print_exc()

def update_seller_passwd(args):
    try:
        cur = conn.cursor()
        sql = 'UPDATE "seller" SET passwd = {passwd} WHERE "seller".id = {id}'.format(passwd=args.value, id=args.id)
        result = cur.execute(sql)  # parameterized query -> dict형으로 넣을수도 있음
        print(result)
        conn.commit()
        print("Update Seller's Password Successfully")
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser() #인자값을 받을 수 있는 인스턴스 생성
    parse_seller(parser)
    args = parser.parse_args() #입력받은 인자값을 args에 저장

    if args.command == 'info':
        show_seller_info(args)

    elif args.command == 'update':
        if args.column == 'name':
            update_seller_name(args)
        elif args.column == 'phone':
            update_seller_phone(args)
        elif args.column == 'local':
            update_seller_local(args)
        elif args.column == 'domain':
            update_seller_domain(args)
        elif args.column == 'passwd':
            update_seller_passwd(args)
        else:
            parser.print_help()

    else:
        parser.print_help()


    #main(args)
    print("Running Time: ", end="")
    print(time.time() - start)
"""
def main(args):
    # TODO
    try:
        cur = conn.cursor()
        sql = "SELECT * FROM seller WHERE id=%(id)s;"
        cur.execute(sql, {"id": 2})
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception as err:
        print(err)
    print(args)
    pass


if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="ID of Seller")
    parser.add_argument("property", nargs=argparse.REMAINDER, help="Property to Change")
    args = parser.parse_args()
    main(args)
    print("Running Time: ", end="")
    print(time.time() - start)
"""