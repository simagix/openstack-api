#! /bin/bash
if [ -e /dev/vdb ]; then
    if [ ! -e /dev/vdb1 ]; then
        echo -e "o\nn\np\n1\n\n\nw" | /sbin/fdisk /dev/vdb
        /sbin/mkfs.ext4 /dev/vdb1
        mkfs.ext4 /dev/vdb1
    else
        echo "/dev/vdb1 already partitioned"
    fi
    mkdir -p /data
    mount /dev/vdb1 /data
    echo "partition /dev/vdb and mount to /data"
else
    echo "no data partition"
fi

