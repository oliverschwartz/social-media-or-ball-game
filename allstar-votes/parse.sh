# Make 3 seperate csv files with (player_name, number of votes), one file for each season
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
    # Sort each csv
    sort -k2 -n -t, votes$i.csv > new.csv
    rm votes$i.csv
    cat new.csv > votes$i.csv
    rm new.csv
done

# Make a file called 'players.txt' with all the players from 17-19 seasons (no duplicates)
cat votes17.csv > votes.csv
cat votes18.csv >> votes.csv
cat votes19.csv >> votes.csv
sort -k1 -n -t, votes.csv > new.csv
rm votes.csv
cat new.csv > votes.csv
rm new.csv
sed -r 's/,[0-9]*//g' votes.csv > tmp.txt
rm votes.csv
python players-parse.py < tmp.txt > players.txt
rm tmp.txt