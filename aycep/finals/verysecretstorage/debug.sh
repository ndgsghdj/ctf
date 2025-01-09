#!/bin/sh

pid=$$
cp ./initramfs.cpio.gz "./${pid}chall.cpio.gz"
cp ./flag.txt "./${pid}chall.txt"

qemu-system-x86_64 -s -S\
    -kernel ./bzImage \
    -cpu qemu64,+smep,+smap \
    -m 4G \
    -smp 2 \
    -initrd "./${pid}chall.cpio.gz" \
    -append "console=ttyS0 quiet loglevel=3 kaslr kpti=1" \
    -hdb "./${pid}chall.txt" \
    -monitor /dev/null \
    -nographic \
    -no-reboot \

rm "./${pid}chall.cpio.gz"
rm "./${pid}chall.txt"
