import argparse
import os
import socket
from datetime import datetime, timedelta
import time


def _check_port(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, int(port)))
    except socket.error:
        return False
    print "%s:%s is available." % (host, port)
    return True


def check_port(host, port):
    yield _check_port(host, port)


def wait_port(host, port):
    while not _check_port(host, port):
        yield False
    yield True


def _check_file(filepath):
    if os.path.exists(filepath):
        print "%s exists." % filepath
        return True
    else:
        return False


def check_file(filepath):
    yield _check_file(filepath)


def wait_file(filepath):
    while not _check_file(filepath):
        yield False
    yield True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check and/or wait for application dependencies.")
    parser.add_argument("--wait-secs", default="30", type=int,
                        help="Number of seconds to wait.")
    parser.add_argument("--interval-secs", default="5", type=int,
                        help="Number of seconds to wait in between checks.")
    parser.add_argument("--port", action="append", default=[],
                        help="Check that port is open. Format is host:port.")
    parser.add_argument("--port-wait", action="append", default=[],
                        help="Wait for port to open. Format is host:port.")
    parser.add_argument("--file", action="append", default=[],
                        help="Check that file exists.")
    parser.add_argument("--file-wait", action="append", default=[],
                        help="Wait for file to exist.")

    args = parser.parse_args()

    iter_dict = {}
    for f in args.file:
        iter_dict[check_file(f)] = "%s does not exist." % f

    for f in args.file_wait:
        iter_dict[wait_file(f)] = "%s does not exist after wait." % f

    for p in args.port:
        (host, port) = p.split(":")
        iter_dict[check_port(host, port)] = "%s not available." % p

    for p in args.port_wait:
        (host, port) = p.split(":")
        iter_dict[wait_port(host, port)] = "%s not available after wait." % p


    iters = iter_dict.keys()
    start = datetime.now()
    end = start + timedelta(seconds=args.wait_secs)
    count = 0
    while iters and datetime.now() < end:
        count += 1
        print "Check %s" % count
        remove_iters = []
        for check_iter in iters:
            try:
                if next(check_iter):
                    #Remove from iter_dict
                    del iter_dict[check_iter]
            except StopIteration:
                remove_iters.append(check_iter)
        for remove_iter in remove_iters:
            iters.remove(remove_iter)
        if iters and count > 1:
            #Wait
            time.sleep(args.interval_secs)

    for result in iter_dict.values():
        print result

    if iter_dict:
        exit(1)
    else:
        exit(0)