cd pages
for file in `ls`; do
    egrep '[A-Z].*[a-z]+[A-Z]*[a-z]*.*, [A-Z].*[A-Z]*.*[a-z]*.*' $file > $file'-parsed'
    grep 'wisbb_selected' $file >> $file'-parsed'
    sed -i -e 's/<span>//g' $file'-parsed'
    sed -i -e 's/<\/span>//g' $file'-parsed'
    sed -i -e 's/<\/a>//g' $file'-parsed'
    sed -i -e 's/<td class="wisbb_selected">//g' $file'-parsed'
    sed -i -e 's/<\/td>//g' $file'-parsed'



done
