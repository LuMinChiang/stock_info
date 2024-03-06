#!/bin/bash
export PATH="$PATH:/finance"
cd /finance
python3 /finance/get_data.py check_weekly
python3 /finance/get_data.py recalculate