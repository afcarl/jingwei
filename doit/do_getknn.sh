rootpath=$SURVEY_DATA
codepath=$SURVEY_CODE

if [ "$#" -ne 6 ]; then
    echo "Usage: $0 trainCollection testCollection feature uu numjobs job"
    exit
fi

trainCollection=$1
testCollection=$2
feature=$3

if [ "$feature" = "color64+dsift" ]; then
    distance=l1
elif [ "$feature" = "vgg-verydeep-16-fc7relu" ]; then 
    distance=cosine
else
    echo "unknown feature $feature"
    exit
fi 
uniqueUser=$4
numjobs=$5
job=$6

python $codepath/instance_based/getknn.py  $trainCollection $testCollection $feature --distance $distance --uu $uniqueUser --numjobs $numjobs --job $job

