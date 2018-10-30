rapydscript -b -p -m math_example.py > math_example.js
sed -i.bu 's/ՐՏ/rs/g' math_example.js
