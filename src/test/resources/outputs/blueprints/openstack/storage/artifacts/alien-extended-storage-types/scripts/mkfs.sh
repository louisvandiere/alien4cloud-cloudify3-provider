#!/bin/bash -e

# use_external_resource=$(ctx node properties use_external_resource)
fs_type=${FS_TYPE}
filesys=${PARTITION_NAME}

(eval $(blkid $DEV | awk ' { print $3 } '); echo $TYPE)

if [ -z "${use_external_resource}" ]; then
    mkfs_executable=''
    case ${fs_type} in
        ext2 | ext3 | ext4 | fat | ntfs )
         mkfs_executable='mkfs.'${fs_type};;
        swap )
         mkfs_executable='mkswap';;
        * )
         echo "File system type is not supported."
         exit 1;;
    esac

    echo "Creating ${fs_type} file system using ${mkfs_executable}"
    sudo ${mkfs_executable} ${filesys}
else
    echo "Not making a filesystem since 'use_external_resource' is set to true"
fi
