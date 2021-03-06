# Label Big Mail

This simple script connects to your IMAP mailbox, searches through the given
IMAP folder (usually one that contains all messages, but it does not have to)
and uses IMAP COPY command to label them. In Gmail (and Google Apps of course)
this command actually causes a label to be added to those messages.

You can then conveniently click on the label and see just the big messages and
decide which ones are important and which ones are weird photos in BMP from
your very distant relative.

Note that for regular, non-gmail IMAP mailboxes, you might want to use
`--no-label` flag to avoid copying emails.

This script requires IMAPClient, a convenient Python IMAP library.
http://imapclient.freshfoo.com/

You can install it using PyPI: `(sudo) pip install imapclient` or EasyInstall: `(sudo) easy_install IMAPClient`
    
Basic usage is like this (with threshold 2MB, which is the default):
    `big_mail_labeler.py your_account@gmail.com -t 2097152`

-----

```
usage: big_mail_labeler.py [-h] [-t THRESHOLD] [--print] [--no-label]
                           [-p PASSWORD] [-l LABEL] [-f FOLDER] [-s HOST]
                           [--nossl] username

positional arguments:
  username              IMAP username.

optional arguments:
  -h, --help            show this help message and exit
  -t THRESHOLD, --threshold THRESHOLD
                        What constitutes big message, messages bigger than
                        this will be labeled. (default: 2097152)
  --print               Prints the big messages. (default: False)
  --no-label            Disable labeling of messages. Just print them.
                        (default: False)
  -p PASSWORD, --password PASSWORD
                        IMAP password, if you leave this out, you'll be asked
                        by getpass instead.
  -l LABEL, --label LABEL
                        Name of the "big message" label. (default: Big)
  -f FOLDER, --folder FOLDER
                        IMAP folder to scan. This should ideally contain all
                        messages, like gmail's All Mail. (default: [Gmail]/All
                        Mail)
  -s HOST, --server HOST
                        IMAP server name (default: imap.gmail.com)
  --nossl               Do not connect using SSL. (default: True)
```
