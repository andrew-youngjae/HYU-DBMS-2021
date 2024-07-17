import time
import argparse
import traceback
from helpers.connection import conn

def parse_delivery(parser:argparse.ArgumentParser):
    sub_parsers = parser.add_subparsers(dest='command')

    # command = status
    parse_status = sub_parsers.add_parser('status')
    parse_status.add_argument('id', help="ID of Delivery")
    parse_status_option = parse_status.add_mutually_exclusive_group()
    parse_status_option.add_argument("-e", type=int)
    parse_status_option.add_argument("-a", "--all", action="store_true", help="Display All orders")
    #parse_status.add_argument("order_id", nargs="?", help="Deliverying order_id for changing to devliered")

def show_delivering_info(args):
    try:
        cur = conn.cursor()
        if(args.all):
            sql = 'SELECT id, status FROM "orders" WHERE did = {did}'.format(did=args.id)
            cur.execute(sql)
            delivering_info = cur.fetchall()
            print("Show all information")
            print("=======================================================")
            print("Delivery Information of Deliveryman {did}".format(did=args.id))
            print("=======================================================")
            display_delivering_info(delivering_info)

        elif(not args.all):
            sql = 'SELECT id, status FROM "orders" WHERE did = {did} AND status = \'delivering\''.format(did=args.id)
            cur.execute(sql)
            delivering_info = cur.fetchall()
            print("Show only delivering information")
            print("=======================================================")
            print("Delivery Information of Deliveryman {did}".format(did=args.id))
            print("=======================================================")
            display_delivering_info(delivering_info)
    except Exception:
        traceback.print_exc()

def display_delivering_info(delivering_info):
    for records in delivering_info:
        print("Order ID : {oid} | {status}".format(oid=records[0], status=records[1]))
        print("-------------------------------------------------------")

def deliver_complete(args):
    try:
        cur = conn.cursor()
        sql = 'UPDATE "orders" SET status = \'delivered\', delivery_time = (NOW() AT TIME ZONE \'Asia/Seoul\') ' \
              'WHERE did = {did} AND id = {oid}'.format(did=args.id, oid=args.e)
        cur.execute(sql)
        conn.commit()

        reduce_stock = 'UPDATE "delivery" SET stock = stock - 1 WHERE id = {did}'.format(did=args.id)
        cur.execute(reduce_stock)
        conn.commit()

        print("Delivery Complete")

    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser()
    parse_delivery(parser)
    args = parser.parse_args()

    if(args.command == 'status'):
        if(args.e == None):
            show_delivering_info(args)

        elif(args.e != None):
            deliver_complete(args)

        else:
            parser.print_help()

    else:
        parser.print_help()

    print("Running Time: ", end="")
    print(time.time() - start)
