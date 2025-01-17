#!/bin/sh
qemu-system-x86_64 \
    -m 128M \
    -cpu kvm64,+smep \
    -kernel vmlinuz \
    -initrd initramfs.cpio.gz \
    -hdb flag.txt \
    -snapshot \
    -nographic \
    -monitor /dev/null \
    -no-reboot \
    -append "console=ttyS0 nokaslr nosmap nopti quiet panic=1"
