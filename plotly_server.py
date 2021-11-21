# from flask import Flask
import os
import glob
from string import ascii_lowercase
import itertools
import streamlit as st
import streamlit.components.v1 as components
import numpy as np


def load_specnames():
    return np.loadtxt('names.txt', dtype=int)


def render_plot(plot):
    with open(plot, 'rb') as file:
        lines = file.readlines()
    html = b''
    for line in lines:
        html += line
    return html.decode()


def main():
    st.title('Spectra viewer')
    names = load_specnames()

    id = st.number_input('Please enter Spec Object ID:', 0., float('9'*64), 0., 1., "%d")
    scpcmd = 'scp -i id_rsa mreefe@argo.orc.gmu.edu:/projects/ssatyapa/spectra/mreefe/results.SDSS/FeVII_6087/*/*/'+str(int(id))+'.spectrum.html ./spectra/'
    if not os.path.exists('spectra/'+str(int(id))+'.spectrum.html'):
        try:
            os.system(scpcmd)
        except:
            pass
    try:
        file = glob.glob('spectra/'+str(int(id))+'.spectrum.html')
        file.sort()
        html = render_plot(file[0])
        components.html(html, height=1000, width=1000)
    except:
        st.text(f'Spectrum with ID {id} not found!')

if __name__ == '__main__':
    main()