FILE=$1

URL=https://people.eecs.berkeley.edu/~tinghuiz/projects/pix2pix/datasets/$FILE.tar.gz
TAR_FILE=./$FILE.tar.gz
TARGET_DIR=./$FILE/

wget -N $URL -O $TAR_FILE
mkdir -p $TARGET_DIR
tar -zxvf $TAR_FILE 
rm $TAR_FILE

