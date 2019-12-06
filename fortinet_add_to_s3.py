import boto3

class File_Upload():
    def __init__(self):
        self.ip_list = []
        self.bucket_name = 'name of the bucket'
        self.object_name = 'name of list that is in the AWS bucket'
        self.object_url = 'full url of bucket in AWS'
        self.s3 = boto3.resource("s3")

    def do_work(self):
        '''
        calls the things and gets it done
        :return:
        '''
        self.download_file()
        self.upload_file()

    def upload_file(self):
        '''
        Uploads the file after the new ip is added to the list
        :return:
        '''
        # need to get list objects into a long string to encode it
        ip_list_string = ''
        for ip in self.ip_list:
            ip_list_string += '{ip}\n'.format(ip=ip)
        # then convert to utf-8
        encoded_string = ip_list_string.encode("utf-8")

        s3 = boto3.resource("s3")
        s3.Bucket(self.bucket_name).put_object(Key=self.object_name, Body=encoded_string,
                                               ContentType='text/plain')



    def upload_file(self):
        '''
        Uploads the file after the new ip is added to the list
        :return:
        '''
        # need to get list objects into a long string to encode it
        #self.ip_list = ['1.1.1.1', '2.2.2.0/24']
        ip_list_string = ''
        for ip in self.ip_list:
            ip_list_string += '{ip}\n'.format(ip=ip)
        # then convert to utf-8
        encoded_string = ip_list_string.encode("utf-8")

        self.s3.Bucket(self.bucket_name).put_object(Key=self.object_name, Body=encoded_string,
                                                    ContentType='text/plain')

if __name__ == '__main__':
    s3_client_upload = File_Upload()
    s3_client_upload.do_work()