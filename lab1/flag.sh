#i /bin/bash
# sudo apt install imagemagick to run code

counter = 0
echo 'Please install imagemagick to check image: sudo apt install imagemagick'
if [ ! -d "./img" ]; then
	mkdir img
fi
for OUTPUT in $(seq 255)
	do
		python3 ex2.py -i flag -o img/flag$counter.png -k $counter -m d
		identify img/flag$counter.png
		let counter++
done
