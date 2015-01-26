#!/bin/sh

function generate_data_and_plots {
    NAME=$1
    INPUT_FILE="data/bala_${NAME}_call.json"
    OUTPUT_FILE="sim_results/bala_${NAME}_call.csv"
    python simulation.py -i "${INPUT_FILE}" > "${OUTPUT_FILE}"
    python generate_results.py -i "${OUTPUT_FILE}" --file_suffix "_${NAME}"
}

generate_data_and_plots "random"
generate_data_and_plots "all"
