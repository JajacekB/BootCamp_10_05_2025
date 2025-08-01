import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect('test.rebex.net', port=22, username='demo', password='password')

sftp = client.open_sftp()
file_list = sftp.listdir()
print(file_list)

sftp.get('readme.txt', 'readme.txt')

with open('kg.png', "wb") as local_file:
    sftp.getfo('pub/example/KeyGenerator.png', local_file)

sftp.close()
client.close()
