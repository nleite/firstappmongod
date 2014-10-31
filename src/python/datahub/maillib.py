#!/usr/bin/python
# vim: set fileencoding=utf-8 :
from datahub import Account
from bs4 import BeautifulSoup as bs
from datetime import datetime
import imaplib
import email
import re



class GmailParser(object):

    def parse_emailvalue(self, value):
        """
        Returns the full set of all raw and split email
        """
        if value is None:
            return ""
        splited = re.split("[<>]", value)
        if len(splited) == 1:
            return {'raw':value, 'email': splited[0]}
        return {'raw':value, 'name': splited[0].strip(), 'email': splited[1]}

    def parse_payload(self, document):
        if isinstance(document, list):
            l = []    
            for d in document:
                l.append(self.parse_payload(d))
            return l
        else:
            if document.is_multipart():
                return self.parse_payload(document.get_payload())
            else:
                return self.parse_content_type(document)

    def parse_content_type(self, data):
        ct = data.get_content_type()
        if ct == "text/html":
            soup = bs(data.get_payload(decode=True))

            return { ct: soup.get_text().strip() }
        if ct == "text/plain":
            return {ct: data.get_payload(decode=True).decode("utf-8", errors='ignore').strip()}            

        if ct.startswith("image"):
            return {ct: data.get_payload()}
        return {ct: ""}

    def parse_date(self, datestr):
        pass

    def parse(self, document):

        parsed = dict()
        
        parsed['From'] = self.parse_emailvalue(document['From'])
        parsed['To'] = self.parse_emailvalue(document['To'])
        parsed['Subject'] = document['Subject']
        parsed['In-Reply-To'] = document['In-Reply-To']
        #uggly!
        parsed['Date'] =  datetime.fromtimestamp( email.utils.mktime_tz( email.utils.parsedate_tz(document['Date'])))
        parsed['payload'] = self.parse_payload(document)

        return parsed

class Gmail(Account):

    def __init__(self, account_details, parser=GmailParser):
        """
        :account_details - dictionary that contains the internals configuration to connect to gmail account_details
        """
        super(Gmail, self).__init__(parser)
        self.user = account_details['credentials']['user']
        self.pwd = account_details['credentials']['password']
        
        self.imap = account_details['imap']

        self.tls = account_details['tls']
        self.RFC = "(RFC822)"

        self.excluded_folders = account_details.get('blacklist_folders', None)
        self.wlist = account_details.get('whitelist_folders', None)

        self.server = None

    def connect(self):
        self.server = imaplib.IMAP4_SSL(self.imap)
        self.server.login(self.user, self.pwd)

    def get_folders(self):
        """
        Given an account we might want to list all existing folders.
        Returns list of folders or empty in case of connection failure
        """
        res, folders = self.server.list()
        if res == "NO":
            return []

        return folders


    def load_email(self, folder, limit=1, criterion='ALL',):

        if self.server is None:
            self.connect()
        if folder is None:
            
            folders = self.get_folders()
            for element in folders:
                f = element.split(' ')[-1].replace('"', '')
                if f in self.excluded_folders:
                    continue
                if self.wlist is not None and f not in self.wlist:
                    continue    
                for mail in self.load_email(f, limit):
                    yield mail
            return
            
        res, data = self.server.select(folder)

        if res == "NO":
            return
        res, data = self.server.search("UTF-8", 'ALL')
        ids = data[0].split()
        for mid in ids:
            res, data = self.server.fetch(mid, self.RFC)

            parsed = self.parse_document(email.message_from_string(data[0][1]))
            parsed['folder'] = folder
            yield parsed


