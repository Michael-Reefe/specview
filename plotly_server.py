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

    st.markdown("# Please enter Spec Object ID: ")
    id = st.number_input('ID: ', 0., float('9'*64), 0., 1., "%d")
    os.system('rm *.html')
    password = os.environ["ARGO_PASSWD"]
    ssh = createSSHClient('argo.orc.gmu.edu', 22, 'mreefe', password)
    scp = SCPClient(ssh.get_transport(), sanitize=lambda x: x, socket_timeout=5*60)

    st.markdown("# Please specify the coronal line and wavelength to consider: ")
    line = st.text_input("Name: ", "Fe VII")
    wave = st.number_input("Wavelength: ", int(0), int(9999), int(6087), int(1), "%d")

    try:
        scp.get(f'/projects/ssatyapa/spectra/mreefe/results.SDSS/{line.replace(" ", "")}_{wave}/*/*/'+str(int(id))+'.spectrum.html',
                local_path='.')
    except Exception as e:
        st.text(f'Spectrum with ID {id} not found in {line.replace(" ", "")}_{wave}!')
        print(e)
    else:
        file = glob.glob(str(int(id))+'.spectrum.html')
        file.sort()
        html = render_plot(file[0])
        components.html(html, height=700, width=700)

if __name__ == '__main__':
    main()