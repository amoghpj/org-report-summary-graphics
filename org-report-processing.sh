PATHTOORG=~/orgs/reports
mkdir $PATHTOORG/csv
grep "NAME" $PATHTOORG/export-report.org | awk '{print $2}' > $PATHTOORG/tags.txt
while read -r tag;
do emacs --batch $PATHTOORG/export-report.org -l $PATHTOORG/export-tables-as-csv.el  --eval '(my-tbl-export '"\"$tag\""')';
done <  $PATHTOORG/tags.txt
mv $PATHTOORG/*.csv $PATHTOORG/csv/
python ~/src/generate-org-report.py
