#!/bin/bash -e

source ~/.bash_profile
cd ~/Coverage/code/tests


# if the input is not mock
if [ $1 -eq 0 ]; then 
    echo -n "Welcome! Your non-mock, python script will now run! \n"
    echo -n "Running\n"
    python3 test_embedding.py
    echo -n "Finished!\n"
    cd ../../data/test_data
    anvi-matrix-to-newick embedded_classified_values.txt \
                         -o tree.txt
    
    echo -n "Adjusting embedded data\n"
    echo -n "Running. Be prepared to create a new column titled 'Classification'
            and manually input the training data into the excel spreadsheet. \n"

    cd ~/Coverage/code/tests
    python3 test_embedding_adjust.py

    echo -n "Finished!\n"
    cd ../../data/test_data

    echo -n "Now launching Anvi'o interactive that will ease the process\n"

    anvi-interactive -d embedded_classified_values.txt \
                    -p asdf.db \
                    --title "Practice Run" \
                    --tree tree.txt \
                    --manual

else 
    echo -n "Welcome! Your mock, python script will now run! \n"
    echo -n "Running\n"
    python3 test_mock_embedding.py
    echo -n "Finished!\n"
    cd ../../data/folder
    echo -n "Make sure to run the anvio commands to generate and visualize 
            your tree file :) \n"
fi

