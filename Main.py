import netmiko
import xlrd
from getpass import getpass

class Main():

    def __init__(self):
        '''
        initialize the class
        '''
        self.file = 'fortinet_node_list.xls'
        self.host_list = []
        self.username = input('enter a username\n')
        self.password = getpass('enter a password\n')

    def doWork(self):
        '''
        do work and return output
        :return:
        '''
        # go through the list that self.getHost method created for us
        for device in self.host_list:
            # define these to shorten amount of things that need typed later
            ip_address = device['ip_address']
            hostname = device['hostname']

            fortinet = {
                'device_type': 'terminal_server',
                'host': ip_address,
                'username': self.username,
                'password': self.password
            }

            # need to catch any auth failures that happen
            try:
                # time to connect
                print('connecting to {hostname} at IP address {ip}'.format(ip=ip_address,
                                                                           hostname=hostname))
                connection = netmiko.ConnectHandler(**fortinet)
                # send an 'a' to accept the prompt, basically we enter an a with a newline then change device type
                connection.write_channel('a\n')
                # redispatch will change the device type
                netmiko.redispatch(connection, device_type='fortinet')
                # get the output
                results = connection.send_command('get system status').split('\n')
                # print the results
                print(results[0])
                # once we're done lets disconnect and be proper
                connection.disconnect()

            except(netmiko.NetmikoAuthError):
                print('authentication failed to {hostname} at IP address {ip}'.format(ip=ip_address,
                                                                           hostname=hostname))
            except(netmiko.NetMikoTimeoutException):
                print('connection timeout to {hostname} at IP address {ip}'.format(ip=ip_address,
                                                                           hostname=hostname))

    def getHost(self):
        '''
        get ip info from the xls
        :return:
        '''
        # open the xls file
        workbook = xlrd.open_workbook(self.file)
        # open up the right sheet
        sheet = workbook.sheet_by_name('sheet2')

        # iterate through the hosts
        for i in range (sheet.nrows):
            # first row is just the column headers
            if i == 0:
                continue
            else:
                # go through the xls and add a dictinary for each host into the list
                self.host_list.append({'hostname':sheet.row_values(i)[1],
                                       'ip_address': sheet.row_values(i)[0]})



if __name__ == '__main__':
    worker = Main()
    worker.getHost()
    worker.doWork()