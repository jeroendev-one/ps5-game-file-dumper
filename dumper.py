#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Requirements
from ftplib import FTP
import argparse
import subprocess
import os

## Argparse
parser = argparse.ArgumentParser()
parser.add_argument("PS5_IP", help="PS5 IP address")
parser.add_argument("FTP_PORT", type=int, help="FTP Port")
parser.add_argument("PPSA", help="PPSA code to dump")
args = parser.parse_args()

## Variables
PS5_IP = args.PS5_IP
FTP_PORT = args.FTP_PORT
PPSA = args.PPSA
info_msg = 'INFO::'
error_msg = 'ERROR::'

# Directory names to create
dirs_to_create = ['dumps']

# Create directories if they don't exist
for directory in dirs_to_create:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Start FTP connection
ftp = FTP()
ftp.connect(PS5_IP, FTP_PORT, timeout=30)
ftp.login(user='username', passwd = 'password')

def download_ftp_directory(ftp, remote_dir, local_dir, PPSA, is_subdirectory=False):
    try:
        # Change to the remote directory
        ftp.cwd(remote_dir)

        # Create the local directory if it doesn't exist
        if not is_subdirectory:
            local_dir = os.path.join(local_dir, f'{PPSA}-app0', 'sce_sys')
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)

        # List the files and subdirectories in the remote directory using retrlines
        listings = []
        ftp.retrlines('LIST', lambda x: listings.append(x))

        # Download each file and handle subdirectories recursively
        for listing in listings:
            # Extract file/folder information
            info = listing.split()
            file_name = info[-1]

            # Exclude '.' and '..' directories
            if file_name in ('.', '..'):
                continue

            local_path = os.path.join(local_dir, file_name)
            remote_path = os.path.join(remote_dir, file_name)

            # Check if it's a subdirectory
            if info[0].startswith('d'):
                # Create the corresponding local subdirectory
                local_subdir = os.path.join(local_dir, file_name)
                if not os.path.exists(local_subdir):
                    os.makedirs(local_subdir)

                # Recursive call for subdirectories
                download_ftp_directory(ftp, remote_path, local_subdir, PPSA, is_subdirectory=True)
            else:
                try:
                    with open(local_path, 'wb') as local_file:
                        ftp.retrbinary(f"RETR {remote_path}", local_file.write)
                    print(f"Downloaded: {file_name}")
                except Exception as e:
                    print(f"Error downloading {remote_path}: {e}")

        print(f"Downloaded files from {remote_dir} to {local_dir}")
    except Exception as e:
        print(f"Error: {e}")

# Download directories
download_ftp_directory(ftp, f'/user/appmeta/{PPSA}', 'dumps', PPSA)
download_ftp_directory(ftp, f'/system_data/priv/appmeta/{PPSA}', 'dumps', PPSA)

 # Open the binary file in binary mode
npbind_path = os.path.join('dumps', f'{PPSA}-app0', 'sce_sys', 'trophy2', 'npbind.dat')
with open(npbind_path, 'rb') as file:
    # Read the content of the file
    content = file.read()

# Find the index of the bytes corresponding to "NPWR"
npwr_index = content.find(b'NPWR')

# If "NPWR" is found, extract the value after it and remove the last two characters
if npwr_index != -1:
    npwr_value = content[npwr_index + 4: npwr_index + 4 + 10].decode('utf-8')[:-2]
    print(f'NPWR value: {npwr_value}')

    # Example usage to download uds00.ucp and trophy00.ucp
    uds_remote_path = f'/user/np_uds/nobackup/conf/NPWR{npwr_value}/uds.ucp'
    uds_local_path = os.path.join('dumps', f'{PPSA}-app0', 'sce_sys', 'uds', 'uds00.ucp')
    trophy_remote_path = f'/user/trophy2/nobackup/conf/NPWR{npwr_value}/TROPHY.UCP'
    trophy_local_path = os.path.join('dumps', f'{PPSA}-app0', 'sce_sys', 'trophy2', 'trophy00.ucp')

    try:
        # Download uds00.ucp
        with open(uds_local_path, 'wb') as local_file:
            ftp.retrbinary(f"RETR {uds_remote_path}", local_file.write)
        print(f"Downloaded: uds00.ucp")

        # Download trophy00.ucp
        with open(trophy_local_path, 'wb') as local_file:
            ftp.retrbinary(f"RETR {trophy_remote_path}", local_file.write)
        print(f"Downloaded: trophy00.ucp")

    except Exception as e:
        print(f"Error downloading files: {e}")
else:
    print('NPWR not found in the file.')
