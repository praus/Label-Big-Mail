#!/usr/bin/env python

import argparse
import email
import bisect

try:
    from imapclient import IMAPClient
except ImportError:
    import sys
    print >>sys.stderr, """This script requires IMAPClient, a convenient Python IMAP library.
http://imapclient.freshfoo.com/

You can install it using PyPI:
    (sudo) pip install imapclient

or EasyInstall:
    (sudo) easy_install IMAPClient
"""
    sys.exit(1)

parser = argparse.ArgumentParser(description='Big Mail Labeler')

parser.add_argument('username', action="store", help='IMAP username.')
parser.add_argument('-t', '--threshold', action="store", dest="threshold", default=2*1024**2, type=int,
                    help="What constitutes big message, messages bigger than this will be labeled. Units are in bytes, default is 2MB (default: %(default)s)")
parser.add_argument('--print', action="store_true", dest="print_msgs", default=False,
                    help='Prints the big messages. (default: %(default)s)')
parser.add_argument('--no-label', action="store_true", dest="no_label", default=False,
                    help='Disable labeling of messages. Just print them. (default: %(default)s)')
parser.add_argument('-p', '--password', action="store", dest="password",
                    help='IMAP password, if you leave this out, you\'ll be asked by getpass instead.')
parser.add_argument('-l', '--label', action="store", dest="label", default="Big",
                    help='Name of the "big message" label. (default: %(default)s)')
parser.add_argument('-f', '--folder', action="store", dest="folder", default='[Gmail]/All Mail',
                    help='IMAP folder to scan. This should ideally contain all messages, like gmail\'s All Mail. (default: %(default)s)')
parser.add_argument('-s', '--server', action="store", dest="host", default="imap.gmail.com",
                    help='IMAP server name (default: %(default)s)')
parser.add_argument('--nossl', action="store_false", dest="ssl", default=True,
                    help='Do not connect using SSL. (default: %(default)s)')

options = parser.parse_args()

if not options.password:
    import getpass
    options.password = getpass.getpass("Please enter your IMAP password: ")

server = IMAPClient(options.host, ssl=options.ssl, use_uid=True)
print server.login(options.username, options.password)

select_info = server.select_folder(options.folder)
print '%d messages in IMAP folder %s' % (select_info['EXISTS'], options.folder)

print "Fetching message metadata"
messages = server.search(['NOT DELETED'])
response = server.fetch(messages, ['RFC822.HEADER', 'RFC822.SIZE', 'INTERNALDATE'])

print "Messages fetched, sorting..."
by_size = sorted(list(response.viewitems()), key=lambda m: m[1]['RFC822.SIZE'])

sizes = [ m[1]['RFC822.SIZE'] for m in by_size ]
# select msgs that are bigger than threshold
bigger = bisect.bisect_right(sizes, options.threshold) # index of the first message bigger than threshold
big_messages = by_size[bigger:]

print "There are %d messages bigger than %s" % (len(big_messages), options.threshold)

big_uids = [ msg[0] for msg in big_messages ]

def print_messages():
    print "\n--- Messages bigger than {}: ".format(options.threshold).ljust(80, '-')
    print "Format: <date> | <size> | <from> | <subject>"
    for msgid, data in big_messages:
        headers = email.message_from_string(data['RFC822.HEADER'])
        size = data['RFC822.SIZE']
        date = data['INTERNALDATE']
        print "{} | {} | {} | {}".format(date, size, headers['from'], headers['subject'])

if not options.no_label:
    print "Labeling big messages with label %s" % options.label
    server.create_folder(options.label)
    server.copy(big_uids, options.label)
    print "Your messages larger than {} bytes have been labeled with label {}".format(options.threshold, options.label)

if options.print_msgs or options.no_label:
    print_messages()


