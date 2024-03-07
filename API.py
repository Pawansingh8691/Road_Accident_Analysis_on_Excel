from flask import Flask, request, jsonify
import urllib.request
import PyPDF2
import pandas as pd
import numpy as np
import pyodbc
import mysql.connector
import sqlalchemy
from sqlalchemy import create_engine, text
from datetime import datetime
from PyPDF2 import PdfReader
# start_time = datetime.datetime.now()
date_format = '%d-%m-%Y'

app = Flask(__name__)
def read_pdf_from_url(url):
    try:
        reader = PdfReader(r'C:\Users\uhf2597\Downloads\technical_report.pdf')

        page = reader.pages[0]

        text = page.extract_text()

        import re

        date = re.findall("Date(.*)",text)[0].strip()

        deal_number = re.findall("Deal Number(.*)",text)[0].strip()

        type_of_loan = re.findall("Type of Loan(.*)",text)[0].strip()

        customer_name = re.findall("Name of the Customer(.*)",text)[0].strip().replace('(s)',"").strip()

        document_details = re.findall("Provided document details(.*)",text)[0].replace("\uf0b7",'').strip()

        property_addres = re.findall("Property address as per site along with Pin(.*)", text)[0].strip()

        legal_address = re.findall("Legal address of property(.*)", text)[0].strip()

        is_tenant = re.findall("Tenant if applicable(.*)", text)[0].strip()

        contact_number = re.findall("Contact no of the owner(.*)",text)[0].strip()[0:10]

        contact_number = int(contact_number)

        land_mark = re.findall("Landmark(.*)",text)[0].strip()

        technical_visit_date = re.findall("Date of technical visit(.*)",text)[0].strip().replace("/","-")

        technical_visit_date = datetime.strptime(technical_visit_date, date_format)

        occupancy = re.findall("Occupancy(.*)", text)[0].strip()

        marketability = re.findall("Marketability(.*)", text)[0].strip()

        colony_occupancy = re.findall("Colony occupancy(.*)", text)[0].strip()

        corporation_limit = re.findall("Corporation Limit (.*)", text)[0].strip()

        no_of_floors = re.findall("No of floors(.*)", text)[0].strip()

        type_of_structure = re.findall("Type of structure(.*)", text)[0].strip()

        configuration = re.findall("Configuration(.*)",text)[0].strip()
        return {'Deal_Number':deal_number, 'Type of Loan': type_of_loan, 'Customer Name':customer_name, 'Document Details':document_details, 'Property Address' : property_addres,
                'Legal Address': legal_address, 'Is Tenant':is_tenant, 'Contact Number':contact_number, 'Land Mark':land_mark, 'Technical Visit Date':technical_visit_date,
                 'Occupancy':occupancy, 'Marketability':marketability, 'Colony Occupancy':colony_occupancy, 'Corporation Limit':corporation_limit, 'No of Floors':no_of_floors,
                  'Type of Structure':type_of_structure}
    except Exception as e:
        return {'error':str(e)}


@app.route('/read_pdf', methods = ['GET'])
def read_pdf():
    url = request.args.get('url')
    if url:
        text = read_pdf_from_url('url')
        return jsonify({'text':text})
    else:
        return jsonify({'error' : 'URL parameter missing, Please provide the correct parameter'}), 400

if __name__ == '__main__':
    app.run(debug=True)