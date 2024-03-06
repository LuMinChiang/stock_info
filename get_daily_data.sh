#!/bin/bash
export PATH="$PATH:/finance"
cd /finance
python3 /finance/get_data.py company_data
python3 /finance/get_data.py daily