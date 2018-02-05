# build 
docker build -t  mydump_sche:0.3 ./
 
# run with default mapping dir
docker run -itd --name mysql_backup -v /etc/localtime:/etc/localtime -v /etc/hosts:/etc/hosts mydump_sche:0.3

# run with cus mappping dir
docker run -itd --name mysql_backup -v /etc/localtime:/etc/localtime -v /etc/hosts:/etc/hosts -v /cloud/m_backup:/cloud/mysql_backup/ mydump_sche:0.3