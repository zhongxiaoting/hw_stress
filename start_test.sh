if [ $# == 0 ]; then
    python ./launch.py
elif [ $# == 1 ]; then
    python ./launch.py $1
elif [ $# == 2 ]; then
    python ./launch.py $1 $2
else
    echo 'How to start the project:'
    echo '1. do all entire test input: ./start_test.sh'
    echo '2. do station test input: ./start_test.sh 2'
    echo '3. do single intem test input: ./ start_test.sh 1 2' 
fi
