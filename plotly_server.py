# from flask import Flask
import os
import glob
from string import ascii_lowercase
import itertools
import streamlit as st
import streamlit.components.v1 as components
import numpy as np

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
    scp = SCPClient(ssh.get_transport())
    # try:
    scp.get('/projects/ssatyapa/spectra/mreefe/results.SDSS/*/*/*/'+str(int(id))+'.spectrum.html')
    # except Exception as e:
    # st.text(f'Spectrum with ID {id} not found!')
    # print(e)
    # else:
    file = []
    texts = ['Generating spectrum.', 'Generating spectrum..', 'Generating spectrum...']
    i = 0
    while len(file) == 0:
        file = glob.glob(str(int(id))+'.spectrum.html')
        time.sleep(1)
        st.text(texts[i % 3])
        i += 1
    file.sort()
    html = render_plot(file[0])
    components.html(html, height=700, width=700)

if __name__ == '__main__':
    main()