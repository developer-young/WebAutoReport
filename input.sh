#! /bin/bash
stty erase ^H

echo '首次运行需要先填写个人表单信息'
read -p '学号:' user

read -p '密码:' password

echo $user > config.txt
echo $password >> config.txt
echo $user >> config.txt
arr=(1 2 3 4 5 6 7 8 9 10 11)
arr[4]='硕士生'
arr[6]='非定向'
read -p '姓名:' arr[0]
read -p '身份证号:' arr[1]
read -p '学院:' arr[2]
read -p '专业:' arr[3]
#read -p '攻读学位(xx生):' arr[4]
read -p '导师:' arr[5]
#read -p '培养类别(非定向):' arr[6]
read -p '宿舍楼(xx校区x号楼):' arr[7]
read -p '宿舍号:' arr[8]
read -p '手机号码:' arr[9]
read -p '紧急联系人电话:' arr[10]

for item in ${arr[*]}
do
  echo $item >> config.txt
done
