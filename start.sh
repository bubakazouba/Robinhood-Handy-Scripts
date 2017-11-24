#!/bin/bash
cd "$(dirname "$0")"
script=$1
pine_option="pine"
sheets_option="sheets"
positions_option="positions"
price_option="price"

USERNAME="FILL IN YOUR USERNAME HERE"
PASSWORD="FILL IN YOUR PASSWORD HERE"

if [[ $script == $pine_option ]]; then
	echo "running pinescript generator"
	python generate_pine_script.py --username "$USERNAME" --password "$PASSWORD" --export-to 'clipboard' $2

elif [[ $script == $sheets_option ]]; then
	echo "running consolidator"
	python consolidate_transactions_into_trades.py --username "$USERNAME" --password "$PASSWORD" --export-to 'clipboard' $2

elif [[ $script == $positions_option ]]; then
	echo "running get positions"	
	python get_current_positions.py --username "$USERNAME" --password "$PASSWORD" --export-to 'clipboard'

elif [[ $script == $price_option ]]; then
	echo "running get price"	
	python get_price.py --username "$USERNAME" --password "$PASSWORD" --export-to 'clipboard' $2
else
	echo "select an option 'pine' or 'sheets' or 'positions' or 'price'"
fi
