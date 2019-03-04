for i in 17 18 19; do
    for j in *$i.html; do
        grep -o "html\">[A-Za-z]* [A-Za-z]*</a></td><td class=\"right \" data-stat=\"fan_votes\">.*fan_rank" $j > parsed
        sed "s/html\">//g" parsed > parsed1
        sed -r "s/<.*fan_votes\">/,/g" parsed1 > parsed2
        sed -r "s/<.*fan_rank//g" parsed2 > parsed3
        sed -r "s/,//g" parsed3 > parsed4
        python parse.py < parsed4 > parsed5
        cat parsed5 >> votes$i.csv
        rm parsed? parsed
    done
done