while [ 1 ]; do
	python test.py 3 "f" 0
	sleep 2
	python test.py 3 "f" 8
	sleep 1
	python test.py 3 "f" 12
	sleep 1
	python test.py 3 "f" 16
	sleep 3
	python test.py 3 "f" 12
	sleep 1
	python test.py 3 "f" 8
	sleep 1
	python test.py 3 "f" 0
	sleep 3
	python test.py 3 "b" 0
	sleep 2
	python test.py 3 "b" 8
	sleep 1
	python test.py 3 "b" 12
	sleep 1
	python test.py 3 "b" 16
	sleep 3
	python test.py 3 "b" 12
	sleep 1
	python test.py 3 "b" 8
	sleep 1
	python test.py 3 "b" 0
	sleep 3
done
