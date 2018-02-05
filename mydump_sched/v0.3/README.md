docker build -t  mydump_sche:0.3 /.

docker run -itd --name mysql_backup -v /etc/localtime:/etc/localtime -v /etc/hosts:/etc/hosts mydump_sche:0.3