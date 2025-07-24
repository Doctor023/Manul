import os
import getpass
import start_page
import ssh_connection

server = start_page.account_message()
ssh_connection.connect_ssh(server)