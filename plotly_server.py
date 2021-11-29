# from flask import Flask
import os
import glob
from string import ascii_lowercase
import itertools
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
from joblib import Parallel, delayed

import paramiko
from scp import SCPClient


def load_specnames():
    return np.loadtxt('names.txt', dtype=int)


def render_plot(plot):
    with open(plot, 'rb') as file:
        lines = file.readlines()
    html = b''
    for line in lines:
        html += line
    return html.decode()

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client


def main():
    st.title('Spectra viewer')
    # names = load_specnames()

    id = st.number_input('Please enter Spec Object ID:', 0., float('9'*64), 0., 1., "%d")
    os.system('rm *.html')
    password = os.environ["ARGO_PASSWD"]
    ssh = createSSHClient('argo.orc.gmu.edu', 22, 'mreefe', password)
    scp = SCPClient(ssh.get_transport(), sanitize=lambda x: x, socket_timeout=5*60)
    lines = ['ArX_5533', 'CaV_5309', 'FeVI_5335', 'FeVII_5276', 'FeVII_5720', 'FeVII_6087', 'FeX_6374', 'FeXI_7892', 'FeXIV_5303']
    def search(line):
        try:
            scp.get(f'/projects/ssatyapa/spectra/mreefe/results.SDSS/{line}/*/*/'+str(int(id))+'.spectrum.html',
                    local_path='.')
            return True
        except:
            return False
    results = Parallel(njobs=len(lines))(delayed(search)(l for l in lines))
    if any(results):
        file = glob.glob(str(int(id))+'.spectrum.html')
        file.sort()
        html = render_plot(file[0])
        components.html(html, height=700, width=700)
    else:
        st.text(f'Spectrum with ID {int(id)} not found!')

if __name__ == '__main__':
    main()